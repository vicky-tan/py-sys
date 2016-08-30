# coding=utf-8

from task import task_container, task
from task.trigger import simple_trigger

from text import conf_utils

from py_sys.monitor import linux_monitor as linux
from py_sys.monitor import net_monitor as net

class SystemMonitor():
    
    def __init__(self, conf_file):
        conf = conf_utils.Configuration(conf_file)
        self.__load_task(conf)
    
    def __load_task(self, conf):
        self.container = task_container.TaskContainer()
                
        # CPU监控
        if self.conf.get(conf, 'cpu_monitor', 'true') == 'true':
            cpu_threshold = self.conf.get(conf, 'cpu_usage', 80.0)
            cpu_interval = self.conf.get(conf, 'cpu_interval', 60)
            cpu_task = task.Task('cpu_monitor', linux.CPUMonitor(cpu_threshold), 
                           simple_trigger.SimpleTrigger(0, cpu_interval))
            self.container.add_task(cpu_task)
        
        # Memory 内存监控
        if self.conf.get(conf, 'memory_monitor', 'true') == 'true':
            memory_threshold = self.conf.get(conf, 'memory_usage', 80.0)
            memory_interval = self.conf.get(conf, 'memory_interval', 60)
            memory_task = task.Task('Memory_Monitor', linux.MemoryMonitor(memory_threshold), 
                           simple_trigger.SimpleTrigger(0, memory_interval))
            self.container.add_task(memory_task)
        
        # Store 存储监控 (挂载点监控)
        if self.conf.get(conf, 'store_monitor', 'true') == 'true':
            store_mount = self.conf.get(conf, 'store_mount', '/')
            store_threshold = self.conf.get(conf, 'store_usage', '80.0')
            store_interval = self.conf.get(conf, 'store_interval', 60)
            store_task = task.Task('store_monitor', linux.DiskMonitor(store_mount, store_threshold), 
                           simple_trigger.SimpleTrigger(0, store_interval))
            self.container.add_task(store_task)
            
        # Processor 本地进程监控
        if self.conf.get(conf, 'processor_monitor', 'true') == 'true':
            process_interval = self.conf.get(conf, 'process_interval', 60)
            process_pid = self.conf.get(conf, 'process_pid', None)
            if process_pid is not None:
                process_task = task.Task('process_monitor', linux.ProcessMonitor(process_pid),
                                         simple_trigger.SimpleTrigger(0, process_interval))
                self.container.add_task(process_task)
                
        # LocalService 本地服务监控
        if self.conf.get(conf, 'service_monitor', 'true') == 'true':
            service_interval = self.conf.get(conf, 'service_interval', 60)
            service_ports = self.conf.get(conf, 'service_ports', None)
            service_recvq = self.conf.get(conf, 'service_recvq', None)
            if service_ports is not None:
                service_task = task.Task('service_monitor', linux.ServiceMonitor(service_ports, service_recvq),
                                         simple_trigger.SimpleTrigger(0, service_interval))
                self.container.add_task(service_task)
                
        # HostPing 主机存在监控 
        if self.conf.get(conf, 'host_monitor', 'true') == 'true':
            host_interval = self.conf.get(conf, 'host_interval', 60)
            host_address = self.conf.get(conf, 'host_address', None)
            host_timeout = self.conf.get(conf, 'host_timeout', 10)
            if host_address is not None:
                host_task = task.Task('host_monitor', net.HostPingMonitor(host_address, host_timeout),
                                         simple_trigger.SimpleTrigger(0, host_interval))
                self.container.add_task(host_task)
                
    def start(self):
        self.container.start_all(True)
        
    
if __name__ == '__main__':
    monitor = SystemMonitor('sys.conf')
    monitor.start()