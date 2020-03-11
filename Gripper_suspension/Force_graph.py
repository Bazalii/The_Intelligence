from threading import Thread
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


class ForceGraph(Thread):

    def __init__(self, x: list or tuple = (-100, 100), y:
    list or tuple = (-100, 100), z: list or tuple = (-100, 100)):
        """
        Инициализирует графическую визуализацию значений.
        :param x: Первоначальные границы по X
        :param y: Первоначальные границы по Y
        :param z: Первоначальные границы по Z
        """
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
                if len(self.ax.lines) >= 5:
                    for i in range(5):
                        self.ax.lines[0].remove()

                if len(self.buffer) > 3:
                    self.buffer = list(self.buffer.pop(-1))
                val = self.buffer.pop(0)
                try:

                    self.ax.plot([-100, -100], [0, 0], [0, val[1]['-x']], c=[0.7, 0.2, 0.2, 1])
                    self.ax.plot([100, 100], [0, 0], [0, val[1]['+x']], c=[0.2, 0.7, 0.2, 1])
                    self.ax.plot([0, 0], [-100, -100], [0, val[1]['-y']], c=[0.2, 0.2, 0.7, 1])
                    self.ax.plot([0, 0], [100, 100], [0, val[1]['+y']], c=[0.2, 0.2, 0.2, 1])
                    self.ax.plot([val[0].start_point.x, val[0].end_point.x],
                                 [val[0].start_point.y, val[0].end_point.y],
                                 [val[0].start_point.z, val[0].end_point.z], c=[0, 0, 0, 1])

                    plt.draw()
                    plt.pause(0.025)
                except:
                    pass
        if self.ax is not None:
            del self.ax

    def terminate_thread(self):
        """
        Завершает работу визуализатора.
        """
        self.run_available = False

    def add_to_buffer(self, val: list or dict):
        """
        Добавляет значения для последующей визуализации.
        :param val: добавляемое значение.
        """
        if type(val) == list or tuple:
            self.buffer.append(val)
        elif type(val) == dict:
            self.buffer.append(val)
