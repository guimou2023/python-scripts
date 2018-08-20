#!/usr/bin/env python

# 多进程探测主机存活
import multiprocessing
import subprocess
import time
start_time = time.time()
host_list = ['10.20.0.{}'.format(x) for x in range(1,255)]
if len(host_list) > 10:
    process_number = 10
else:
    process_number = len(host_list)
def ping_host(ipaddr):
    if subprocess.call('ping -c1 -W 1 %s > /dev/null' % ipaddr, shell=True) == 0:
        print '%s is OK' % ipaddr
    else:
        print '%s is DOWN' % ipaddr
pool = multiprocessing.Pool(processes=process_number)
for ip in host_list:
    pool.apply_async(ping_host,(ip,))
pool.close()
pool.join()
end_time = time.time()
print('runtime is {}'.format(end_time-start_time))
