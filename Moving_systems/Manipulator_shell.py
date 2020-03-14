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
        print(f'Move to point:({x}, {y}, {z})')

    def set_start_height(self):
        """
        Аппаратная установка высоты работы
        """
        pass

    def pick(self):
        """
        Реализация захвата детали (опустились, зажали, подняли)
        """
        pass

    def setup(self):
        """
        Реализация установки детали
        """
        pass

    def set_custom_angle(self):
        """
        Отклонение на нужный нам угол
        """

    def set_default_angle(self):
        """
        Задается начальный угол(параллельное столу положение)
        """
        pass

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
        print(f"Move")

    def get_pos(self) -> Point:
        pass

