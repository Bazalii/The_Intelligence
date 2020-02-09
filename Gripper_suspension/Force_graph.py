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

        self.start()

    def run(self) -> None:
        self.run_available = True
        ax = plt.axes(projection="3d")
        ax.set_xlim3d(self.x)
        ax.set_ylim3d(self.y)
        ax.set_zlim3d(self.z)

        ax.set_xlabel('X, g')
        ax.set_ylabel('Y, g')
        ax.set_zlabel('Z, g')

        while self.run_available:
            if len(self.buffer) > 1:
                for i in range(4):
                    ax.lines[0].remove()

                val = self.buffer.pop(0)
                ax.plot([0, 0], [0, 0], [0, val['-x']])
                ax.plot([100, 100], [100, 100], [0, val['+x']])
                ax.plot([100, 100], [0, 0], [0, val['-y']])
                ax.plot([0, 0], [100, 100], [0, val['+y']])
                plt.draw()