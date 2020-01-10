#encoding=utf-8
import time

from multiprocessing import Queue as ProcessQueue
from multiprocessing import Lock
from queue import Queue as ThreadQueue
from threading import Thread


class FlowControl:
    def __init__(self, num, interval):

        assert isinstance(num, int)
        assert isinstance(interval, (int, float))

        self.num = num
        self.interval = interval
        self.__queue = ThreadQueue(self.num)
        Thread(target=self.__start).start()

    def get(self):
        try:
            self.__queue.get_nowait()
            return True
        except Exception:
            return False

    def __put(self):
        self.__queue.put_nowait(True)

    def __start(self):
        while True:
            before = time.time()
            try:
                for i in range(self.num):
                    self.__put()
            except Exception:
                pass
            finally:
                after = time.time()
                sleep_time = self.interval - (after - before)
                time.sleep(sleep_time if sleep_time > 0 else 0)

class ProcessFlowControl:
    def __init__(self, num, interval):

        assert isinstance(num, int)
        assert isinstance(interval, (int, float))

        self.num = num
        self.interval = interval
        self.__queue = ProcessQueue(self.num)
        self.__lock = Lock()
        Thread(target=self.__start).start()

    def get(self):
        try:
            self.__lock.acquire()
            self.__queue.get_nowait()
            return True
        except Exception:
            return False
        finally:
            self.__lock.release()

    def __put(self):
        self.__queue.put_nowait(True)

    def __start(self):
        while True:
            before = time.time()
            try:
                self.__lock.acquire()
                for i in range(self.num):
                    self.__put()
            except Exception:
                pass
            finally:
                self.__lock.release()
                after = time.time()
                sleep_time = self.interval - (after - before)
                time.sleep(sleep_time if sleep_time > 0 else 0)



