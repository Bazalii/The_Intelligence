from __future__ import annotations
from Classes.Point_class import Point
from typing import Iterable
from math import acos


class Vector:
    def __init__(self, point1: Point or Iterable, point2: Point or Iterable = None):
        """
        Создает вектор плоскости. Если дана только одна точка, то вектор счетается радиус-вектором(начало в (0,0)).
        :param point1: Точка начала вектора относительно С.О.
        :param point2: Точка конца вектора относительно С.О.
        """
        point1 = Point.check_Point(point1)

        if type(point2) is None:
            if point1.z is None:
                self.start_point: Point = Point(0, 0)
            else:
                self.start_point: Point = Point(0, 0, 0)
            self.end_point: Point = point1
        else:
            point2 = Point.check_Point(point2)
            if (point1.z is None and point2.z is None) or (point1.z is not None and point2.z is not None):
                self.start_point: Point = point1
                self.end_point: Point = point2
            else:
                raise TypeError("Flat and 3D points used in one Vector obj.")

    def length(self) -> float:
        """
        :return: Длину вектора.
        """
        if self.start_point.z is None:
            return ((self.start_point.x - self.end_point.x) ** 2 + (self.start_point.y - self.end_point.y) ** 2) ** 0.5
        else:
            return ((self.start_point.x - self.end_point.x) ** 2
                    + (self.start_point.y - self.end_point.y) ** 2
                    + (self.start_point.z - self.end_point.z) ** 2) ** 0.5

    def move_to_point(self, new_start_point: Point or Iterable) -> None:
        """
        Перемещает начало вектора к заданной точке.
        :param new_start_point: Точка куда необходимо перенести вектор.
        """
        new_start_point = Point.check_Point(new_start_point)
        dif_val = self.start_point - new_start_point
        self.start_point -= dif_val
        self.end_point -= dif_val

    def radius_vector(self) -> Point:
        """
        :return: Радиус вектор в виде точки.
        """
        return self.end_point - self.start_point

    def move_along_vector(self, vector: Vector) -> None:
        """
        Перемещает существующий вектор вдоль другого вектора.
        :param vector: Вектор вдоль которого необходимо перемещать.
        """
        if type(vector) == Vector:
            vector = vector.copy()
            vector.move_to_point(self.start_point)
            self.move_to_point(vector.end_point)
        else:
            raise TypeError("Incorrect input of vector.")

    def copy(self) -> Vector:
        """
        :return: Копию вектора.
        """
        return Vector(self.start_point, self.end_point)

    def set_length(self, new_len: float or int) -> None:
        """
        Устанавливает новую длинну вектора, сохраняя направление вектора.
        Не изменяет положение начальной точки!!!
        :param new_len: новая длина вектора.
        """
        rad = self.radius_vector()
        cof = new_len / self.length()
        rad *= cof
        vec = Vector(Point(0,0), rad)
        vec.move_to_point(self.start_point)
        # self.start_point *= cof
        self.end_point = vec.end_point

    # +
    def __add__(self, other: Point or Iterable or Vector) -> Vector:
        if type(other) == Vector:
            return Vector(self.start_point + other.start_point, self.end_point + other.end_point)
        other = Point.check_Point(other)
        start = self.start_point + other
        end = self.end_point + other
        return Vector(start, end)

    # -
    def __sub__(self, other: Point or Iterable or Vector):
        if type(other) == Vector:
            return Vector(self.start_point - other.start_point, self.end_point - other.end_point)
        other = Point.check_Point(other)
        start = self.start_point - other
        end = self.end_point - other
        return Vector(start, end)

    # /
    def __truediv__(self, other: Point or Iterable or Vector):
        if type(other) == Vector:
            return Vector(self.start_point / other.start_point, self.end_point / other.end_point)
        other = Point.check_Point(other)
        start = self.start_point / other
        end = self.end_point / other
        return Vector(start, end)

    # *
    def __mul__(self, other: Point or Iterable or Vector):
        if type(other) == Vector:
            return Vector(self.start_point * other.start_point, self.end_point * other.end_point)
        other = Point.check_Point(other)
        start = self.start_point * other
        end = self.end_point * other
        return Vector(start, end)

    # ==
    def __eq__(self, other: Vector) -> bool:
        """
        Вектора равны, если их радиус-вектора равны.
        :param other: Вектор с которым идет сравнение.
        :return: True или False.
        """
        if other.radius_vector() == self.radius_vector():
            return True
        else:
            return False

    def __getitem__(self, item: int) -> Point:
        if item == 0:
            return self.start_point
        elif item == 1:
            return self.end_point
        else:
            raise IndexError("Index out of range.")

    def __str__(self) -> str:
        return f"Start point: {str(self.start_point)}" \
               f"\nEnd point: {str(self.end_point)}"


def find_collinear_coefficients(what: Vector, i_fv: Vector, j_fv: Vector):
    """
    Раскладывает плоский вектор на 2 коллинеарных вектора. Возвращает 2 коэффициента разложения на которые необходимо
     домножить 2 коллинеарных вектора, чтобы при их суммировании получить исходный вектор разложения.
    :param what: Какой вектор раскладывать.
    :param i_fv: Первый вектор для разложения.
    :param j_fv: Второй вектор для разложения.
    :return: 2 коэффициента.
    """
    # fv - flat vector
    # p - point
    # c - coefficient
    # rv - radius vector
    what_rv = what.radius_vector()
    i_rv = i_fv.radius_vector()
    j_rv = j_fv.radius_vector()

    j_c = (what_rv.y * i_rv.x - i_rv.y * what_rv.x) / (j_rv.y * i_rv.x - j_rv.x * i_rv.y)
    i_c = (what_rv.x - j_rv.x * j_c) / i_rv.x
    return i_c, j_c

def angle_between_two_angels(vec1: Vector, vec2: Vector):
    vec_1 = vec1.copy()
    vec_2 = vec2.copy()
    param2 = vec_1.length()*vec_2.length()
    vec_1 = vec_1.radius_vector()
    vec_2 = vec_2.radius_vector()
    if vec_1.z is None or vec_2.z is None:
        param1 = vec_1.x*vec_2.x + vec_1.y*vec_2.y
    else:
        param1 = vec_1.x*vec_2.x + vec_1.y*vec_2.y + vec_1.z*vec_2.z
    return acos(param1/param2)
