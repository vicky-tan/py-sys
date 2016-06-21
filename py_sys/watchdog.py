# coding=utf-8

from task import task
from task import task_container

from task.job import job
from task.trigger import simple_trigger

from py_sys.info import linux
from py_sys import execute

class WatchDog():
    
    def __init__(self):
        self.watch_c = task_container.TaskContainer()
    
    def watch(self, processes):
        if processes == None or not isinstance(processes, dict):
            raise IOError('Watch processes is NULL or not dict')
        
        for pid in processes:
            action = processes.get(pid)
            if action is not None:
                watch_task = task.Task('%s WatchDog' % pid, WatchJob(pid, action), simple_trigger.SimpleTrigger(0, 1))
                self.watch_c.add_task(watch_task)
            
    def start(self):
        self.watch_c.start_all(True)
        
class WatchJob(job.Job):
    
    def __init__(self, pid, action):
        self.pid = pid
        self.action = action
        
    def execute(self):
        linux_info = linux.LinuxInfo()
        ps_info = linux_info.ps(True)
        if ps_info is not None:
            for ps_item in ps_info:
                _pid = ps_item.get('pid')
                if self.pid == _pid:
                    return
        
        execute.run(self.action)
                
        
        