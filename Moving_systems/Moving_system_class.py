from abc import ABC, abstractmethod
from Classes.Point_class import Point


class MovingSystem(ABC):
    @abstractmethod
    def move_to_point(self, x: float or Point = None, y: float = None, z: float = None,
                      tx: float = None, ty: float = None, tz: float = None):
        pass

    @abstractmethod
    def set_zero(self):
        pass

    @abstractmethod
    def set_program_zero(self):
        pass

    @abstractmethod
    def set_speed(self, **kwargs):
        pass
