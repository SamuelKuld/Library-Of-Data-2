from inspect import Parameter
import threading
import time


class Thread(threading.Thread):
    def __init__(self, funct, parameters=()):
        threading.Thread.__init__(self, target=funct, args=parameters)

    def run(self) -> None:
        return super().run()