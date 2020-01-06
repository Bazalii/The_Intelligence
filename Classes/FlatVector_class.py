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
