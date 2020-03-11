from threading import Thread
from time import sleep

import serial
import serial.tools.list_ports

from Gripper_suspension.Force_graph import ForceGraph
from Classes.Vector_class import Vector
from Gripper_suspension.KalmanFilter_class import KalmanFilter

functions_sequence = [[], [], []]


def synchronize_in_thread(function):
    """
    Декоратор для синхронизации выполнения функций внутри потока обработчика Serial порта.
    Функция не должна ничего возвращать и может иметь любое количество входных параметров.
    :param function: функция, которую нужно выполнить в потоке.
    """
    global functions_sequence

    def wrapper(*args, **kwargs):
        functions_sequence[0].append(function)
        functions_sequence[1].append(args)
        functions_sequence[2].append(kwargs)
        return None

    return wrapper


class GripSuspension(Thread):

    def __init__(self, port: str = None, baudrate: int = None, **kwargs):
        """
        Инициализатор потока трекинга Serial порта по которому будет происходить передача данных с подвеса гриппера.
        :param port: наименование Serial порта по которому будет происходить передача данных.
        :param baudrate: скорость установленная на шине по которой будет происходить обмен данными.(кол-во бод)
        :param kwargs: реализация дополнительных параметров и функционала.
        "data_buffer" - устанавливает размер буфера записи входных данных.
        "sleep_time" - время сна между циклами прочтения.
        "graph" - графическая визуализация входных параметров.
        """
        Thread.__init__(self)
        self.run_available = False
        self.data_buffer_len = 5
        self.sleep_time = 0.1
        self.buffer = []
        self.graph = None

        self.plus_x_filter = KalmanFilter(1e-3, 0.0025)
        self.minus_x_filter = KalmanFilter(1e-3, 0.0025)
        self.plus_y_filter = KalmanFilter(1e-3, 0.0025)
        self.minus_y_filter = KalmanFilter(1e-3, 0.0025)

        self.plus_x_cof = 0
        self.minus_x_cof = 0
        self.plus_y_cof = 0
        self.minus_y_cof = 0

        self.writing_in_buffer_flag = False
        self.serial = None
        if (port is not None) and (baudrate is not None):
            self.connect(port, baudrate)
        if kwargs.get("data_buffer", False):
            self.data_buffer_len = kwargs["data_buffer"]
        if kwargs.get("sleep_time", False):
            self.sleep_time = kwargs["sleep_time"]
        if kwargs.get("graph", False):
            self.graph = ForceGraph()

        self.start()

    def run(self) -> None:
        global functions_sequence

        self.run_available = True

        while self.run_available:
            sleep(self.sleep_time)

            if len(functions_sequence[0]) > 0:
                function = functions_sequence[0].pop(0)
                arguments = functions_sequence[1].pop(0)
                key_word_arguments = functions_sequence[2].pop(0)
                function(*arguments, **key_word_arguments)

            if self.serial is not None:
                if not self.serial.is_open:
                    self.serial.open()

                while self.serial.in_waiting:
                    try:
                        data: bytes = self.serial.readline()

                        if type(data) == bytes:
                            data: str = data.decode('utf-8').strip()

                        if data != "":
                            data = data.replace('$', '')
                            data = data.replace(';', '')
                            data = data.strip()
                            parse = data.split()
                            parse = {"+x": self.plus_x_filter.latest_noisy_measurement(float(parse[0][2:]))
                                           - self.plus_x_cof,
                                     "-x": self.minus_x_filter.latest_noisy_measurement(float(parse[1][2:]))
                                           - self.minus_x_cof,
                                     "+y": self.plus_y_filter.latest_noisy_measurement(float(parse[2][2:]))
                                           - self.plus_y_cof,
                                     "-y": self.minus_y_filter.latest_noisy_measurement(float(parse[3][2:]))
                                           - self.minus_y_cof}
                            vec1 = Vector((0, 0, 0), (-parse['-x'], 0, parse['-x']))
                            vec2 = Vector((0, 0, 0), (parse['+x'], 0, parse['+x']))
                            vec3 = Vector((0, 0, 0), (0, -parse['-y'], parse['-y']))
                            vec4 = Vector((0, 0, 0), (0, parse['+y'], parse['+y']))

                            sum_vec = vec1 + vec2 + vec3 + vec4
                            sum_vec.set_length(abs(parse['-x']) + abs(parse['+x'])
                                               + abs(parse['-y']) + abs(parse['+y']))

                            if len(self.buffer) >= self.data_buffer_len:
                                self.writing_in_buffer_flag = True
                                self.buffer.append((sum_vec, parse))
                                self.buffer.pop(0)
                                self.writing_in_buffer_flag = False
                            else:
                                self.writing_in_buffer_flag = True
                                self.buffer.append((sum_vec, parse))
                                self.writing_in_buffer_flag = False

                            if self.graph is not None:
                                self.graph.add_to_buffer((sum_vec, parse))
                    except:
                        pass

    @synchronize_in_thread
    def connect(self, port: str, baudrate: int):
        """
        Присоединяется к устройству по Serial.
        :param port: наименование Serial порта по которому будет происходить передача данных.
        :param baudrate: скорость установленная на шине по которой будет происходить обмен данными.(кол-во бод)
        """
        try:
            self.serial = serial.Serial(port, baudrate, timeout=0.2)
        except serial.SerialException:
            print("Can not connect to serial port.")
            print("Available ports:")
            for port in list(d.device for d in serial.tools.list_ports.comports()):
                print(port)

    @synchronize_in_thread
    def disconnect(self):
        """
        Отсоединяется от устройства.
        :return:
        """
        if self.serial is not None:
            self.serial.close()
            self.serial = None

    @synchronize_in_thread
    def send_to_serial(self, information: str):
        """
        Отправляет информацию устройству по Serial.
        :param information: информация, которую необходимо передать.
        """
        if self.serial is not None:
            if not self.serial.is_open:
                self.serial.open()
            self.serial.write((information + "\n").encode("utf-8"))
            self.serial.reset_input_buffer()
        else:
            Exception("Error sending to Serial.")

    def terminate_thread(self):
        """
        Останавливает поток.
        """
        self.disconnect()
        if self.graph is not None:
            self.graph.terminate_thread()
        self.run_available = False
        self.graph.join()
        self.join()

    def latest_val(self):
        """
        :return: последнее значение из буфера значений.
        """
        while self.writing_in_buffer_flag:
            pass
        return self.buffer[-1]

    def set_zero(self):
        """
        Програмно устанавливает входные значения равными 0.
        :return:
        """
        if len(self.buffer) <= 0:
            self.plus_x_cof = 0
            self.minus_x_cof = 0
            self.plus_y_cof = 0
            self.minus_y_cof = 0
        else:
            while self.writing_in_buffer_flag:
                pass
            val = self.latest_val()
            self.plus_x_cof = val[1]['+x'] + self.plus_x_cof
            self.minus_x_cof = val[1]['-x'] + self.minus_x_cof
            self.plus_y_cof = val[1]['+y'] + self.plus_y_cof
            self.minus_y_cof = val[1]['-y'] + self.minus_y_cof

    def no_zero(self):
        """
        Отменяет программное онулирование входных параметров.
        :return:
        """
        self.plus_x_cof = 0
        self.minus_x_cof = 0
        self.plus_y_cof = 0
        self.minus_y_cof = 0
