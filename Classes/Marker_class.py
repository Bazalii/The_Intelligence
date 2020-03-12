# Класс для маркеров
from Classes.Point_class import Point


class Marker:
    def __init__(self, id: int, center_point: Point, size: float, corners = None, **kwargs):
        self.center_point = center_point
        self.id = id
        self.size = size
        self.corners = corners
        if kwargs.get("name", False):
            self.name = kwargs["name"]
