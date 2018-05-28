# coding=utf-8

from task import task
from task import task_container

from task.job import job
from task.trigger import simple_trigger

from text import string_utils

from py_sys.info import linux
from py_sys import execute

class WatchDog():
    
    def __init__(self):
        self.watch_c = task_container.TaskContainer()
    
    def watch_process(self, processes):
        if processes == None or not isinstance(processes, dict):
            raise IOError('Processes list is None or not dict')
        
        for pid in processes:
            action = processes.get(pid)
            if action is not None:
                watch_task = task.Task('%s WatchDog' % pid, WatchProcessJob(pid, action), simple_trigger.SimpleTrigger(0, 1))
                self.watch_c.add_task(watch_task)
    
    def watch_service(self, services):
        if services == None or not isinstance(services, dict):
            raise IOError('Services list or not dict')
        
        for service in services:
            action = services.get(service)
            if action is not None:
                watch_task = task.Task('%s WatchDog' % service, WatchServiceJob(service, action), simple_trigger.SimpleTrigger(0, 1))
                self.watch_c.add_task(watch_task)
        
            
    def start(self):
        self.watch_c.start_all(True)
        
class WatchProcessJob(job.Job):
    
    def __init__(self, pid, action):
        self.pid = pid
        self.action = action
        
    def execute(self):
        linux_info = linux.LinuxInfo()
        ps_info = linux_info.ps(False)
        if ps_info is not None:
            for ps_item in ps_info:
                p_id = ps_item.get('pid')
                p_cmd = ps_item.get('cmd')
                
                if string_utils.is_numeric(self.pid):
                    if str(self.pid) == p_id:
                        return
                else:
                    if str(self.pid) == p_cmd:
                        return 
        
        execute.run(self.action)

class WatchServiceJob(job.Job):
    
    def __init__(self, service, action):
        try:
            if '/' in service:
                self.port, self.protocol = service.split('/')
        except:
            raise ValueError('service format expect : port/protocol, but %s' % service)
        
        self.action = action
        
    def execute(self):
        linux_info = linux.LinuxInfo()
        ns_info = linux_info.netstat(False)
        if ns_info is not None:
            for ns_item in ns_info:
                protocol = ns_item.get('protocol')
                local = ns_item.get('local')
                state = ns_item.get('state')
                
                if protocol == self.protocol and self.port in local and state == 'LISTENING':
                    return
        
        execute.run(self.action)   
                
        
        