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
        self.buffer = []
        self.ax = None

        self.start()

    def run(self) -> None:
        self.run_available = True
        self.ax = plt.axes(projection="3d")
        self.ax.set_xlim3d(self.x)
        self.ax.set_ylim3d(self.y)
        self.ax.set_zlim3d(self.z)

        self.ax.set_xlabel('X, g')
        self.ax.set_ylabel('Y, g')
        self.ax.set_zlabel('Z, g')

        while self.run_available:
            if len(self.buffer) > 1:
                for i in range(4):
                    self.ax.lines[0].remove()

                val = self.buffer.pop(0)
                self.ax.plot([0, 0], [0, 0], [0, val['-x']])
                self.ax.plot([100, 100], [100, 100], [0, val['+x']])
                self.ax.plot([100, 100], [0, 0], [0, val['-y']])
                self.ax.plot([0, 0], [100, 100], [0, val['+y']])
                plt.draw()

    def terminate_thread(self):
        self.run_available = False
        if self.ax is not None:
            self.ax.show()
            del self.ax

    def add_to_buffer(self, val: list or dict):
        if type(val) == list:
            self.buffer.extend(val)
        elif type(val) == dict:
            self.buffer.append(val)
