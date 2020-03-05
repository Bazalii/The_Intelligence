# Класс для маркеров
from Classes.Point_class import Point


class Marker:
    def __init__(self, id: int, center_point: Point, origin_x: int, origin_y: int, **kwargs):
        self.center_point = center_point
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.id = id
        if kwargs.get("name", False):
            self.name = kwargs["name"]
