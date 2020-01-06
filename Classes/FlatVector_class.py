from Classes.Point_class import Point


class FlatVector:
    def __init__(self, point1: Point, point2: Point = None):
        point1 = Point.check_Point(point1)

        if type(point2) is None:
            self.start_point: Point = Point(0, 0)
            self.end_point: Point = point1
        else:
            point2 = Point.check_Point(point2)
            self.start_point: Point = point1
            self.end_point: Point = point2

    def length(self) -> float:
        return ((self.start_point.x - self.end_point.x) ** 2 + (self.start_point.y - self.end_point.y) ** 2) ** 0.5

    def move_to_point(self, new_start_point: Point or tuple):
        new_start_point = Point.check_Point(new_start_point)
        dif_val = self.start_point - new_start_point
        self.start_point -= dif_val
        self.end_point -= dif_val

    def radius_vector(self) -> Point:
        return self.end_point - self.start_point

    def move_along_vector(self, vector):
        if type(vector) == FlatVector:
            vector.move_to_point(self.start_point)
            self.move_to_point(vector.end_point)
        else:
            raise TypeError("Incorrect input of vector.")

    def copy(self):
        return FlatVector(self.start_point, self.end_point)

    # +
    def __add__(self, other: Point or tuple or list):
        if type(other) == FlatVector:
            return FlatVector(self.start_point + other.start_point, self.end_point + other.end_point)
        other = Point.check_Point(other)
        start = self.start_point + other
        end = self.end_point + other
        return FlatVector(start, end)

    # -
    def __sub__(self, other):
        if type(other) == FlatVector:
            return FlatVector(self.start_point - other.start_point, self.end_point - other.end_point)
        other = Point.check_Point(other)
        start = self.start_point - other
        end = self.end_point - other
        return FlatVector(start, end)

    # /
    def __truediv__(self, other):
        other = Point.check_Point(other)
        start = self.start_point / other
        end = self.end_point / other
        return FlatVector(start, end)

    # *
    def __mul__(self, other):
        other = Point.check_Point(other)
        start = self.start_point * other
        end = self.end_point * other
        return FlatVector(start, end)

    def __str__(self):
        return f"Start point: {str(self.start_point)}" \
               f"\nEnd point: {str(self.end_point)}" \
               f"\n\nRadius vector: {str(self.radius_vector())}"


def find_collinear_coefficients(what: FlatVector, i_fv: FlatVector, j_fv: FlatVector):
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
