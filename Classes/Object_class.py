# Класс для объектов, находящихся на столе
from Classes.Marker_class import Marker


class Object:
    def __init__(self, marker_1: Marker, marker_2: Marker, height, center_point: int, **kwargs):
        self.center_point = center_point
        self.marker_1 = marker_1
        self.marker_2 = marker_2
        self.height = height
        self.ids = [marker_1.id, marker_2.id]
        if kwargs.get("name", False):
            self.name = kwargs["name"]

        if kwargs.get("angle", False):
            self.name = kwargs["angle"]