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
