from threading import Thread
from time import sleep

import serial
import serial.tools.list_ports

functions_sequence = [[], [], []]


def synchronize_in_thread(function):
    global functions_sequence

    def wrapper(*args, **kwargs):
        functions_sequence[0].append(function)
        functions_sequence[1].append(args)
        functions_sequence[2].append(kwargs)
        return None

    return wrapper


class GripSuspension(Thread):

    def __init__(self, port: str = None, baudrate: int = None, **kwargs):
        Thread.__init__(self)
        self.run_available = False
        self.data_buffer_len = 5
        self.sleep_time = 0.05
        self.buffer = []

        if (port is not None) and (baudrate is not None):
            self.serial = serial.Serial(port, baudrate, timeout=0.2)
        else:
            self.serial = None
        if kwargs.get("data_buffer", False):
            self.data_buffer_len = kwargs["data_buffer"]
        if kwargs.get("sleep_time", False):
            self.sleep_time = kwargs["sleep_time"]

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
                            data.replace("$", '')
                            data.replace(";", '')
                            parse = data.split(" ")
                            if len(self.buffer) == self.data_buffer_len:
                                self.buffer.pop(0)
                                self.buffer.append({"+x": parse[0][2:], "-x": parse[1][2:],
                                                    "+y": parse[2][2:], "-y": parse[3][2:]})

                    except:
                        Exception("")
                        return None


@synchronize_in_thread
def connect(self, port: str, baudrate: int):
    try:
        self.serial = serial.Serial(port, baudrate, timeout=0.2)
    except serial.SerialException:
        print("Can not connect to serial port.")
        print("Available ports:")
        for port in list(d.device for d in serial.tools.list_ports.comports()):
            print(port)


@synchronize_in_thread
def disconnect(self):
    if self.serial is not None:
        self.serial.close()
        self.serial = None


@synchronize_in_thread
def send_to_serial(self, information: str):
    if self.serial is not None:
        if not self.serial.is_open:
            self.serial.open()
        self.serial.write((information + "\n").encode("utf-8"))
        self.serial.reset_input_buffer()
    else:
        Exception("Error sending to Serial.")


def terminate_thread(self):
    self.disconnect()
    self.run_available = False
