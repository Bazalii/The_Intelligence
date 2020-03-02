from Moving_systems.Moving_system_class import MovingSystem
from Classes.Point_class import Point


class Manipulator(MovingSystem):

    def __init__(self, moving_speed: float or int):
        self.current_position = Point(0, 0, 0)
        self.program_zero = Point(0, 0, 0)
        self.x_speed = moving_speed
        self.y_speed = moving_speed
        self.z_speed = moving_speed
        print("Manipulator initialisation")

    def move_to_point(self, x: float or Point = None, y: float = None, z: float = None, tx: float = None,
                      ty: float = None,
                      tz: float = None):
        if type(x) == Point:
            print(f"Moving to point -> {x}")
            self.current_position = x
        else:
            print(f"Moving to point -> ({x}, {y}, {z})")
            position = Point((0, 0, 0))
            if x is not None:
                position.x = x + self.program_zero.x
            else:
                position.x = self.current_position.x + self.program_zero.x
            if y is not None:
                position.y = y + self.program_zero.y
            else:
                position.y = self.current_position.y + self.program_zero.y
            if z is not None:
                position.z = z + self.program_zero.z
            else:
                position.z = self.current_position.z - self.program_zero.z
            self.current_position = position

    def set_zero(self):
        # something to set zero position on manipulator
        self.current_position = Point(0, 0, 0)
        print("Set zero.")

    def set_program_zero(self):
        self.program_zero = self.current_position.copy()
        print("Set zero.")

    def set_speed(self, **kwargs):
        if kwargs.get("x_speed", False):
            self.x_speed = kwargs["x_speed"]
        if kwargs.get("y_speed", False):
            self.y_speed = kwargs["y_speed"]
        if kwargs.get("z_speed", False):
            self.z_speed = kwargs["z_speed"]