from threading import Thread
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


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
            if len(self.buffer) > 0:
                if len(self.ax.lines) >= 4:
                    for i in range(4):
                        self.ax.lines[0].remove()

                val = self.buffer.pop(0)
                self.ax.plot([-100, -100], [-100, -100], [0, val['-x']], c=[0.7, 0.2, 0.2, 1])
                self.ax.plot([100, 100], [100, 100], [0, val['+x']], c=[0.2, 0.7, 0.2, 1])
                self.ax.plot([100, 100], [-100, -100], [0, val['-y']], c=[0.2, 0.2, 0.7, 1])
                self.ax.plot([-100, -100], [100, 100], [0, val['+y']], c=[0.2, 0.2, 0.2, 1])
                plt.draw()
                plt.pause(0.0001)

    def terminate_thread(self):
        self.run_available = False
        if self.ax is not None:
            del self.ax

    def add_to_buffer(self, val: list or dict):
        if type(val) == list:
            self.buffer.extend(val)
        elif type(val) == dict:
            self.buffer.append(val)
