class Point:
    def __init__(self, x: float or tuple or list, y: float = None):
        """
        Создает точку плоскости.
        :param x: Позиция точки по X (может принимать значения точки в виде итерируемого объекта).
        :param y: Позиция точки по Y.
        """
        if y is not None:
            self.x = x
            self.y = x
        else:
            try:
                if (type(x[0]) == int or type(x[0]) == float) and (type(x[1]) == int or type(x[1]) == float):
                    self.x = x[0]
                    self.y = x[1]
            except:
                raise TypeError("Incorrect input type. Type is not iterable.")

    # +
    def __add__(self, other: tuple or float):
        if type(other) == Point:
            x = self.x + other.x
            y = self.y + other.y
        elif type(other) == int or type(other) == float:
            x = self.x + other
            y = self.y + other
        else:
            try:
                x = self.x + other[0]
                y = self.y + other[1]
            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    # -
    def __sub__(self, other: tuple or float):
        if type(other) == Point:
            x = self.x - other.x
            y = self.y - other.y
        elif type(other) == int or type(other) == float:
            x = self.x - other
            y = self.y - other
        else:
            try:
                x = self.x - other[0]
                y = self.y - other[1]
            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    #  /
    def __truediv__(self, other: tuple or float):
        if type(other) == Point:
            x = self.x / other.x
            y = self.y / other.y
        elif type(other) == int or type(other) == float:
            x = self.x / other
            y = self.y / other
        else:
            try:
                x = self.x / other[0]
                y = self.y / other[1]
            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    # *
    def __mul__(self, other: tuple or float):
        if type(other) == Point:
            x = self.x * other.x
            y = self.y * other.y
        elif type(other) == int or type(other) == float:
            x = self.x * other
            y = self.y * other
        else:
            try:
                x = self.x * other[0]
                y = self.y * other[1]
            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    def __eq__(self, other):
        other = Point.check_Point(other)
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return f"({self.x}, {self.y})"

    def tuple_format(self) -> tuple:
        """
        :return: Значения точки в виде кортежа.
        """
        return tuple([self.x, self.y])

    def list_format(self) -> list:
        """
        :return: Значения точки в виде листа.
        """
        return [self.x, self.y]

    def to_int(self):
        """
        Преобразует значения точеки к целочисленному формату.
        :return: Копию точки.
        """
        self.x = int(self.x)
        self.y = int(self.y)
        return Point(self.x, self.y)

    def copy(self):
        """
        :return: Копию точки.
        """
        return Point(self.x, self.y)

    @classmethod
    def check_Point(cls, obj):
        """
        :param obj: Любое значение, которое ожидается в виде объекта класса Point.
        :return: Коррекный объект класса Point.
        """
        if type(obj) == Point:
            return Point(obj.x, obj.y)
        else:
            try:
                if (type(obj[0]) == int and type(obj[1]) == int) or (type(obj[0]) == float and type(obj[1]) == float):
                    return Point(obj)
            except:
                raise TypeError("Object can not be Point!")
