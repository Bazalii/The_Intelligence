import telnetlib as tn

from Classes.Vector_class import Vector
from Moving_systems.Moving_system_class import MovingSystem
from Classes.Point_class import Point


class Manipulator(MovingSystem):

    def __init__(self, host: str, telnet_username: str, telnet_password: str, telnet_port: int):
        """
        :param host: локальный хост севера Telnet
        :param telnet_username: имя пользователя на сервере
        :param telnet_password: пароль пользователя
        :param moving_speed: начальная скорость перемещения по всем осям.
        """
        self.tx = 0
        self.ty = 0
        self.tz = 0
        self.__host = host
        self.__user_name = telnet_username
        self.__password = telnet_password
        self.port = telnet_port
        self.current_position = Point(0, 0, 0)
        self.program_zero = Point(0, 0, 0)

        self.telnet_host = tn.Telnet(self.__host, self.port)
        self.telnet_host.read_all()
        self.telnet_host.write(self.__user_name.encode() + b"\n" + b"\n")
        self.telnet_host.read_all()
        self.telnet_host.write(b"\n" + b"\n")
        self.telnet_host.read_all()
        print("Manipulator initialisation")

    def move_to_point(self, x: float or Point = None, y: float = None, z: float = None,
                      tx: float = None, ty: float = None, tz: float = None):
        """
        Метод перемешения "головы" в звданную точку.
        :param x: Координата по X
        :param y: Координата по Y
        :param z: Координата по Z
        :param tx: Угол отклонения от оси OX
        :param ty: Угол отклонения от оси OY
        :param tz: Угол отклонения от оси OZ
        :return:
        """
        if type(x) is Point:
            command = "point a"
            self.telnet_host.write(command.encode() + b"\n")
            command = f"{x.x},{x.y},{x.z},0,180,-90"
            self.telnet_host.write(command.encode() + b"\n" + b"\n")
            command = f"do jmove a"
            self.telnet_host.write(command.encode() + b"\n")
        else:
            command = "point a"
            self.telnet_host.write(command.encode() + b"\n")
            command = f"{x},{y},{x},0,180,-90"
            self.telnet_host.write(command.encode() + b"\n" + b"\n")
            command = f"do jmove a"
            self.telnet_host.write(command.encode() + b"\n")
        # if type(x) == Point:
        #     print(f"Moving to point -> {x}")
        #     self.current_position = x
        # else:
        #     print(f"Moving to point -> ({x}, {y}, {z})")
        #     position = Point((0, 0, 0))
        #     if x is not None:
        #         position.x = x + self.program_zero.x
        #     else:
        #         position.x = self.current_position.x + self.program_zero.x
        #     if y is not None:
        #         position.y = y + self.program_zero.y
        #     else:
        #         position.y = self.current_position.y + self.program_zero.y
        #     if z is not None:
        #         position.z = z + self.program_zero.z
        #     else:
        #         position.z = self.current_position.z - self.program_zero.z
        #     self.current_position = position

    def send_command(self, command):
        """
        отправка команды через телнет
        """
        # command1 = "point a"
        # command2 = "0,700,-400,90,180,0"
        # command3 = "do jmove a"
        # self.telnet_host.write(command1.encode() + b"\n")
        # self.telnet_host.write(command2.encode() + b"\n" + b"\n")
        self.telnet_host.write(command.encode() + b"\n")

    def set_start_height(self):
        """
        Аппаратная установка высоты работы
        """

    def pick(self):
        """
        Реализация захвата детали (опустились, зажали, подняли)
        """

    def setup(self):
        """
        Реализация установки детали
        """

    def set_custom_angle(self, angle):
        """
        Отклонение на нужный нам угол
        """
        self.get_current_position()
        command = "point a"
        self.telnet_host.write(command.encode() + b"\n")
        command = f"{self.x},{self.y},{self.z},0,180,{angle}"
        self.telnet_host.write(command.encode() + b"\n" + b"\n")
        command = f"do jmove a"
        self.telnet_host.write(command.encode() + b"\n")

    def set_default_angle(self):
        """
        Задается начальный угол(параллельное столу положение)
        """

    def set_zero(self):
        """
        Аппаратная установка точки начала отсчета
        """
        # something to set zero position on manipulator
        self.current_position = Point(0, 0, 0)
        print("Set zero.")

    def set_program_zero(self):
        """
        Программная установка положения точки начала отсчета
        """
        self.program_zero = self.current_position.copy()
        print("Set zero.")

    def move_by_vector(self, point: Point or Vector):
        """
        Смещение на вектор
        """

    def get_current_position(self):
        """
        получить текущую позицию
        """
        command = "point a = here"
        self.telnet_host.write(command.encode() + b"\n")
        input_data = (self.telnet_host.read_until(b'Change')).split()
        x = input_data[6]
        y = input_data[7]
        z = input_data[8]
        self.x = x
        self.y = y
        self.z = z
        self.tx = input_data[9]
        self.ty = input_data[10]
        self.tz = input_data[11]
        return Point(x, y, z)
