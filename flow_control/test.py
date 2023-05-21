# encoding=utf-8
import os
import threading
import time

from datetime import datetime
from flow_control.controller import FlowController
from flow_control.controller import ProcessFlowController
from flow_control.controller import AverageFlowController
from flow_control.controller import AverageProcessFlowController
from threading import Thread
from multiprocessing import Process
from unittest import TestCase


class TestFlowController(TestCase):

    def work(self, flowcontrol):
        while True:
            if flowcontrol.get():
                print("{}--{}--{} ".format(os.getpid(), threading.currentThread().ident, datetime.now()))

    def test_thread(self):
        flow_control = FlowController(num=0.5, interval=1)
        Thread(target=self.work, args=(flow_control,)).start()
        self.work(flow_control)

    def test_process(self):
        '''
        :arg 在windows平台上效果并不好

        '''
        process_flow_control = ProcessFlowController(1, 1)
        print(os.getpid())
        Process(target=self.work, args=(process_flow_control,)).start()
        self.work(process_flow_control)

    def test_avg_thread(self):
        flow_control = AverageFlowController(num=2, interval=1)
        Thread(target=self.work, args=(flow_control,)).start()
        Thread(target=self.work, args=(flow_control,)).start()
        self.work(flow_control)

    def test_avg_process(self):
        '''
        :arg 在windows平台上效果并不好

        '''
        process_flow_control = AverageProcessFlowController(0.5, 1)
        print(os.getpid())
        Process(target=self.work, args=(process_flow_control,)).start()
        Thread(target=self.work, args=(process_flow_control,)).start()
        self.work(process_flow_control)


if __name__ == '__main__':
    TestFlowController().test_thread()
