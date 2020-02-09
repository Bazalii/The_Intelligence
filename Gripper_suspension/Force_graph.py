from threading import Thread
import numpy as np
import matplotlib.pyplot as plt


class ForceGraph(Thread):

    def __init__(self, x: list or tuple = (-100, 100), y:
    list or tuple = (-100, 100), z: list or tuple = (-100, 100)):
        Thread.__init__(self)
        self.x = x
        self.y = y
        self.z = z
        self.run_available = False
