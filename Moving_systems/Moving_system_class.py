from abc import ABC, abstractmethod
from Classes.Point_class import Point


class MovingSystem(ABC):
    """
    Абстракционный класс для различный систем перемещения.
    """
    @abstractmethod
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
        pass

    @abstractmethod
    def set_zero(self):
        """
        Аппаратная установка точки начала отсчета
        """
        pass

    @abstractmethod
    def set_program_zero(self):
        """
        Программная установка положения точки начала отсчета
        """
        pass


