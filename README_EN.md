#                                                             Flow Control

- function 
  - This package can control the number of calls (QPS) to a function or statement at a fixed time interval, and can set access times and time intervals,
  - Access Restrictions Access Times/Time Interval

- Usage method (use AverageFlowControl or FlowControl class for single process scenarios, AverageProcessFlowControl or ProcessFlowControl class for multi process scenarios)
- It is recommended to use AverageFlowControl or AverageProcessFlowControl, as this class consumes less resources.

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


  - Create an AverageFlowControl (in the case of a single process) or AverageProcessFlowControl (in the case of multiple processes) object with parameters (num=number of accesses, interval=time interval),
  - Then call the get method of the object
  - If the get method returns True, it indicates that the flow control limit has not been reached. If False is returned, it indicates that the number of function calls or accesses has reached the flow control limit and should be denied
