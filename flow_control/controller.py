# encoding=utf-8
import time

from multiprocessing import RLock as ProcessLock
from multiprocessing import Value
from threading import RLock as ThreadLock
from threading import Thread


class FlowController(object):
    def __init__(self, num, interval):
        '''
        token 初始值为 1 保证首次可以调用通
        cache_token 最多存储 1s 的 token数量 ，若其小于 1 则取值为 1
        '''

        self.num = num
        self.interval = interval
        self.current_token = 1
        self.lock = ThreadLock()
        self.cache_token = 1 if 1 / interval * num < 1 else 1 / interval * num
        Thread(target=self.__start).start()

    def get(self):
        with self.lock:
            if self.current_token >= 1:
                self.current_token -= 1
                return True
            else:
                return False

    def add_token(self):
        self.current_token += self.num

    def reset_token(self):
        with self.lock:
            if self.current_token < self.cache_token:
                self.add_token()

    def __start(self):
        while True:
            before = time.time()
            try:
                self.reset_token()
            except Exception:
                pass
            finally:
                after = time.time()
                sleep_time = self.interval - (after - before)
                time.sleep(sleep_time if sleep_time > 0 else 0)


class ProcessFlowController(FlowController):
    def __init__(self, num, interval):
        super(ProcessFlowController, self).__init__(num, interval)
        self.lock = ProcessLock()
        self.current_token = Value('d', 1.0, lock=False)

    def get(self):
        with self.lock:
            if self.current_token.value >= 1:
                self.current_token.value -= 1
                return True
            else:
                return False

    def add_token(self):
        self.current_token.value += self.num

    def reset_token(self):
        with self.lock:
            if self.current_token.value < self.cache_token:
                self.add_token()


class AverageFlowController(object):
    def __init__(self, num, interval):
        self.num = num
        self.interval = interval
        self.current_token = 1
        self.lock = ThreadLock()
        self.cache_token = 1 if 1 / interval * num < 1 else 1 / interval * num
        self.last_time = time.time()
        self.qps_val = 1 / interval * num

    def get(self):
        with self.lock:
            self.reset_token()
            if self.current_token >= 1:
                self.current_token -= 1
                return True
            else:
                return False

    def reset_token(self):
        now = time.time()
        time_interval = now - self.last_time
        if self.current_token < self.cache_token:
            self.current_token += time_interval * self.qps_val
            self.last_time = now


class AverageProcessFlowController(AverageFlowController):
    def __init__(self, num, interval):
        super(AverageProcessFlowController, self).__init__(num, interval)
        self.lock = ProcessLock()
        self.current_token = Value('d', 1.0, lock=False)
        self.last_time = Value('d', time.time(), lock=False)

    def get(self):
        with self.lock:
            self.reset_token()
            if self.current_token.value >= 1:
                self.current_token.value -= 1
                return True
            else:
                return False

    def reset_token(self):
        now = time.time()
        time_interval = now - self.last_time.value
        if self.current_token.value < self.cache_token:
            self.current_token.value += time_interval * self.qps_val
            self.last_time.value = now
