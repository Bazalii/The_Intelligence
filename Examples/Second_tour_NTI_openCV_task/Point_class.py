from numpy import ndarray

class Point:
    def __init__(self, x: float or tuple or list, y: float = None) -> None:
        if type(x) == tuple or type(x) == list:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    # +
    def __add__(self, other: tuple or float):
        if type(other) == tuple or type(other) == list:
            x = self.x + other[0]
            y = self.y + other[1]
        elif type(other) == Point:
            x = self.x + other.x
            y = self.y + other.y
        elif type(other) == int or type(other) == float:
            x = self.x + other
            y = self.y + other
        else:
            raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    # -
    def __sub__(self, other: tuple or float):
        if type(other) == tuple or type(other) == list:
            x = self.x - other[0]
            y = self.y - other[1]
        elif type(other) == Point:
            x = self.x - other.x
            y = self.y - other.y
        elif type(other) == int or type(other) == float:
            x = self.x - other
            y = self.y - other
        else:
            raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    #  /
    def __truediv__(self, other: tuple or float):
        if type(other) == tuple or type(other) == list:
            x = self.x / other[0]
            y = self.y / other[1]
        elif type(other) == Point:
            x = self.x / other.x
            y = self.y / other.y
        elif type(other) == int or type(other) == float:
            x = self.x / other
            y = self.y / other
        else:
            raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    # *
    def __mul__(self, other: tuple or float):
        if type(other) == tuple or type(other) == list:
            x = self.x * other[0]
            y = self.y * other[1]
        elif type(other) == Point:
            x = self.x * other.x
            y = self.y * other.y
        elif type(other) == int or type(other) == float:
            x = self.x * other
            y = self.y * other
        else:
            raise TypeError("Incorrect input type to sum with Point class object!")
        return Point(x, y)

    def __eq__(self, other):
        other = Point.check_Point(other)
        if (self.x == other.x and self.y == other.y):
            return True
        else:
            return False

    def to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        return Point(self.x, self.y)

    def tuple_format(self) -> tuple:
        return tuple([self.x, self.y])

    def list_format(self) -> list:
        return [self.x, self.y]

    def __str__(self):
        return f"({self.x}, {self.y})"

    @classmethod
    def is_Point(cls, obj):
        if type(obj) == Point:
            return True
        elif type(obj) == tuple or type(obj) == list:
            return False

    @classmethod
    def check_Point(cls, obj):
        if type(obj) == tuple or type(obj) == list:
            return Point(obj)
        elif type(obj) == ndarray:
            return Point(obj[0], obj[1])
        elif type(obj) != Point:
            return Point(obj.x, obj.y)
        else:
            try:
                return Point(obj.x, obj.y)
            except:
                raise TypeError("Object can not be Point!")


def distance_between_two_point(point1, point2):
    point1 = Point.check_Point(point1)
    point2 = Point.check_Point(point2)
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5
