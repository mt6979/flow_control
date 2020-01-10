#encoding=utf-8
import os
import threading

from datetime import datetime
from flow_control.controller import FlowControl
from flow_control.controller import ProcessFlowControl
from threading import Thread
from multiprocessing import Process


def work(flowcontrol):
    while True:
        if flowcontrol.get():
            print("{}--{}--{}".format(os.getpid(), threading.currentThread().ident, datetime.now()))


def test_thread():
    flow_control = FlowControl(num=1, interval=1)
    Thread(target=work, args=(flow_control,)).start()
    Thread(target=work, args=(flow_control,)).start()


def test_process():
    '''
    :arg 在windows平台上效果并不好

    '''
    process_flow_control = ProcessFlowControl(1, 1)
    Process(target=work, args=(process_flow_control,)).start()
    Thread(target=work, args=(process_flow_control,)).start()


if __name__ == '__main__':
    test_thread()
