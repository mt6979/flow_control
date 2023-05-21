#                                                             Flow Control

- 功能 
  - 这个packages可以控制每秒一个函数或者语句的调用次数，可以设置访问次数和时间间隔，
  - 访问限制 访问次数/时间间隔

- 使用方法(单进程情况下使用FlowControl 类，多进程情况下使用ProcessFlowControl类)

  ```Python
  # encoding=utf-8
  import os
  import threading
  
  from datetime import datetime
  from flow_control.controller import FlowController
  from flow_control.controller import ProcessFlowController
  from flow_control.controller import AverageFlowControl
  from flow_control.controller import AverageProcessFlowControl
  from threading import Thread

  
  
  def work(flowcontrol):
      while True:
          if flowcontrol.get():
              print("{}--{}--{}".format(os.getpid(), threading.currentThread().ident, datetime.now()))
  
  flow_control = AverageFlowControl(num=0.5, interval=1)
  Thread(target=work, args=(flow_control,)).start()
  work(flow_control)
  ```


  - 创建一个FlowControl (单进程情况下)或者 ProcessFlowControl(多进程情况下) 对象，参数为(num=访问次数,interval=时间间隔)，
  - num的类型应该为int类型，interval应该为int或者float类型
  - 然后调用该对象的 get方法
  - 如果get方法返回 True，则说明可以未达到流控限制，如果返回False则说明函数调用次数或者访问次数已经 达到流控限制，应该拒绝调用或访问
