class Point:
    def __init__(self, x: float or tuple or list, y: float = None):
        if y is not None:
            self.x = x
            self.y = x
        else:
            try:
                self.x = x[0]
                self.y = x[1]
            except:
                raise TypeError("Incorrect input type. Type is not iterable.")

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