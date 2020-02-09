from threading import Thread
from time import sleep

import serial
import serial.tools.list_ports


class GripSuspension(Thread):

    def __init__(self, port: str = None, baudrate: int = None, **kwargs):
        Thread.__init__(self)
        self.run_available = False
        self.data_buffer_len = 5
        self.sleep_time = 0.05
        if (port is not None) and (baudrate is not None):
            self.serial = serial.Serial(port, baudrate, timeout=0.2)
        else:
            self.serial = None
        if kwargs.get("data_buffer", False):
            self.data_buffer_len = kwargs["data_buffer"]
        if kwargs.get("sleep_time", False):
            self.sleep_time = kwargs["sleep_time"]
