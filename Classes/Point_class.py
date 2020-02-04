class Point:
    def __init__(self, x: float or tuple or list, y: float = None, z: float = None):
        """
        Создает точку плоскости.
        :param x: Позиция точки по X (может принимать значения точки в виде итерируемого объекта).
        :param y: Позиция точки по Y.
        :param z: Позиция точки по Z.
        """
        if y is not None:
            self.x = x
            self.y = x
            self.z = z
        else:
            try:
                if (type(x[0]) == int or type(x[0]) == float) and (type(x[1]) == int or type(x[1]) == float):
                    self.x = x[0]
                    self.y = x[1]
                    if (len(x) >= 3) and (type(x[2]) == int or type(x[2])):
                        self.z = x[2]
            except:
                raise TypeError("Incorrect input type. Type is not iterable.")

    # +
    def __add__(self, other: tuple or float):
        z = None
        if type(other) == Point:
            x = self.x + other.x
            y = self.y + other.y
            if other.z is not None:
                if self.z is None:
                    z = other.z
                else:
                    z = self.z + other.z
        elif type(other) == int or type(other) == float:
            x = self.x + other
            y = self.y + other
            if self.z is None:
                z = other
            else:
                z = self.z + other
        else:
            try:
                x = self.x + other[0]
                y = self.y + other[1]
                if len(other) > 2:
                    if self.z is None:
                        z = other[2]
                    else:
                        z = self.z + other[2]

            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y, z)

    # -
    def __sub__(self, other: tuple or float):
        z = None
        if type(other) == Point:
            x = self.x - other.x
            y = self.y - other.y
            if other.z is not None:
                if self.z is None:
                    z = - other.z
                else:
                    z = self.z - other.z
        elif type(other) == int or type(other) == float:
            x = self.x - other
            y = self.y - other
            if self.z is None:
                z = - other
            else:
                z = self.z - other
        else:
            try:
                x = self.x - other[0]
                y = self.y - other[1]
                if len(other) > 2:
                    if self.z is None:
                        z = other[2]
                    else:
                        z = self.z - other[2]

            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y, z)

    #  /
    def __truediv__(self, other: tuple or float):
        z = None
        if type(other) == Point:
            x = self.x / other.x
            y = self.y / other.y
            if other.z is not None:
                if self.z is not None:
                    z = self.z / other.z
        elif type(other) == int or type(other) == float:
            x = self.x / other
            y = self.y / other
            if self.z is not None:
                z = self.z / other
        else:
            try:
                x = self.x / other[0]
                y = self.y / other[1]
                if len(other) > 2 and self.z is not None:
                    z = self.z / other[2]

            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y, z)

    # *
    def __mul__(self, other: tuple or float):
        z = None
        if type(other) == Point:
            x = self.x * other.x
            y = self.y * other.y
            if other.z is not None:
                if self.z is not None:
                    z = self.z * other.z
        elif type(other) == int or type(other) == float:
            x = self.x * other
            y = self.y * other
            if self.z is not None:
                z = self.z * other
        else:
            try:
                x = self.x * other[0]
                y = self.y * other[1]
                if len(other) > 2 and self.z is not None:
                    z = self.z * other[2]

            except:
                raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y, z)

    def __eq__(self, other):
        other = Point.check_Point(other)
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    def __str__(self):
        if self.z is not None:
            return f"({self.x}, {self.y}, {self.z})"
        else:
            return f"({self.x}, {self.y})"

    def tuple_format(self) -> tuple:
        """
        :return: Значения точки в виде кортежа.
        """
        if self.z is not None:
            return tuple([self.x, self.y, self.z])
        else:
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
            return Point(obj.x, obj.y, obj.z)
        else:
            try:
                if (type(obj[0]) == int and type(obj[1]) == int) or (type(obj[0]) == float and type(obj[1]) == float):
                    if len(obj) > 2:
                        if type(obj[2]) == int or type(obj[2]) == float:
                            return Point(obj)
                        else:
                            raise TypeError("Object can not be Point!")
                    return Point(obj)
            except:
                raise TypeError("Object can not be Point!")
