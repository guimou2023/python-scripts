#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import subprocess
import time
import sys
from fabric.colors import red, green


# 多线程判断主机存活
start_time = time.time()
host_list = ['10.20.0.{}'.format(x) for x in range(1,255)]
def ping_host(ipaddr):
    if subprocess.call('ping -c1 -W 1 %s > /dev/null' % ipaddr, shell=True) == 0:
        sys.stdout.write(green('%s is UP \n' % ipaddr))
     #  print green('%s is UP \n' % ipaddr)
    else:
        sys.stdout.write(red('%s is DOWN \n' % ipaddr))
ThreadList = []
for ip in host_list:
     t = threading.Thread(target=ping_host,args=(ip,))
     ThreadList.append(t)
for t in ThreadList:
     t.start()
for t in ThreadList:
     t.join()
end_time = time.time()
print('runtime is {}'.format(end_time-start_time))
