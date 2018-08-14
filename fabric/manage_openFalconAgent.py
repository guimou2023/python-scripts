#!//usr/local/bin/python2
from fabric.api import *

env.parallel = True
env.user = 'root'
env.key_filename = "/var/root/tx_masterkey.dms"
env.hosts=['10.20.0.51']

def f_deploy():
    run('mkdir -pv /Application/falcon-agent')
    put('falcon-agent-5.1.2.tar.gz', '/Application/falcon-agent')
    run('tar -xf /Application/falcon-agent/falcon-agent-5.1.2.tar.gz -C /Application/falcon-agent')
 
def f_start():
    put('cfg.json','/Application/falcon-agent')
    run('bash /Application/falcon-agent/control start')

def f_stop():
    run('bash /Application/falcon-agent/control stop')
def task():
    execute(f_deploy)
    execute(f_start)
