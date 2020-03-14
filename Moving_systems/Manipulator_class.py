import telnetlib as tn

from Classes.Vector_class import Vector
from Moving_systems.Moving_system_class import MovingSystem
from Classes.Point_class import Point


class Manipulator(MovingSystem):

    def __init__(self, host: str, telnet_username: str, telnet_password: str):
        """
        :param host: локальный хост севера Telnet
        :param telnet_username: имя пользователя на сервере
        :param telnet_password: пароль пользователя
        :param moving_speed: начальная скорость перемещения по всем осям.
        """
        self.__host = host
        self.__user_name = telnet_username
        self.__password = telnet_password
        self.current_position = Point(0, 0, 0)
        self.program_zero = Point(0, 0, 0)

        self.telnet_host = tn.Telnet(self.__host)
        self.telnet_host.read_until(b"login: ")
        self.telnet_host.write(self.__user_name.encode('ascii') + b"\n")
        self.telnet_host.read_until(b"Password: ")
        self.telnet_host.write(self.__password.encode('ascii') + b"\n")
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
        if type(x) == Point:
            print(f"Moving to point -> {x}")
            self.current_position = x
        else:
            print(f"Moving to point -> ({x}, {y}, {z})")
            position = Point((0, 0, 0))
            if x is not None:
                position.x = x + self.program_zero.x
            else:
                position.x = self.current_position.x + self.program_zero.x
            if y is not None:
                position.y = y + self.program_zero.y
            else:
                position.y = self.current_position.y + self.program_zero.y
            if z is not None:
                position.z = z + self.program_zero.z
            else:
                position.z = self.current_position.z - self.program_zero.z
            self.current_position = position
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
    def set_custom_angle(self):
        """
        Отклонение на нужный нам угол
        """
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

    def set_speed(self, **kwargs):
        """
        Установка скоростей перемещения по осям.
        :param kwargs:
        :key x_speed - новая скорость перемещения по OX
        :key y_speed - новая скорость перемещения по OY
        :key z_speed - новая скорость перемещения по OZ
        :return:
        """
        if kwargs.get("x_speed", False):
            self.x_speed = kwargs["x_speed"]
        if kwargs.get("y_speed", False):
            self.y_speed = kwargs["y_speed"]
        if kwargs.get("z_speed", False):
            self.z_speed = kwargs["z_speed"]
    def move_by_vector(self, point: Point or Vector):
        """
        Смещение на вектор
        """
        