from threading import Timer
import time


class CustomTimer(object):
    def __init__(self, time, args=[], kwargs={}):
        self.__time = time
        self.__function = self.empty_function
        self.__args = args
        self.__kwargs = kwargs
        self.__set()
        self.__running = False
        self.started_at = None

    def empty_function(self):
        return

    def __set(self):
        self.__timer = Timer(self.__time, self.__function, self.__args, self.__kwargs)

    def start(self):
        self.__running = True
        self.__timer.start()
        self.started_at = time.time()

    def cancel(self):
        self.__running = False
        self.__timer.cancel()

    def is_alive(self):
        self.__timer.is_alive()

    def reset(self, start=False):
        if self.__running:
            self.__timer.cancel()

        self.__set()

        if self.__running or start:
            self.start()

    def elapsed(self):
        return time.time() - self.started_at

    def remaining(self):
        return self.__time - self.elapsed()
