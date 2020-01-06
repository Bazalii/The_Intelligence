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
