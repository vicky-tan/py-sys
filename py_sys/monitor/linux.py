# coding=utf-8

import time

from task import task_container, task

from task.job import job
from task.trigger import simple_trigger

from py_sys.info import linux
from py_sys.ping import ping_icmp

from text import conf_utils

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
            cpu_task = task.Task('cpu_monitor', CPUMonitor(cpu_threshold), 
                           simple_trigger.SimpleTrigger(0, cpu_interval))
            self.container.add_task(cpu_task)
        
        # Memory 内存监控
        if self.conf.get(conf, 'memory_monitor', 'true') == 'true':
            memory_threshold = self.conf.get(conf, 'memory_usage', 80.0)
            memory_interval = self.conf.get(conf, 'memory_interval', 60)
            memory_task = task.Task('Memory_Monitor', MemoryMonitor(memory_threshold), 
                           simple_trigger.SimpleTrigger(0, memory_interval))
            self.container.add_task(memory_task)
        
        # Store 存储监控 (挂载点监控)
        if self.conf.get(conf, 'store_monitor', 'true') == 'true':
            store_mount = self.conf.get(conf, 'store_mount', '/')
            store_threshold = self.conf.get(conf, 'store_usage', '80.0')
            store_interval = self.conf.get(conf, 'store_interval', 60)
            store_task = task.Task('store_monitor', DiskMonitor(store_mount, store_threshold), 
                           simple_trigger.SimpleTrigger(0, store_interval))
            self.container.add_task(store_task)
            
        # Processor 本地进程监控
        if self.conf.get(conf, 'processor_monitor', 'true') == 'true':
            process_interval = self.conf.get(conf, 'process_interval', 60)
            process_pid = self.conf.get(conf, 'process_pid', None)
            if process_pid is not None:
                process_task = task.Task('process_monitor', ProcessMonitor(process_pid),
                                         simple_trigger.SimpleTrigger(0, process_interval))
                self.container.add_task(process_task)
                
        # LocalService 本地服务监控
        if self.conf.get(conf, 'service_monitor', 'true') == 'true':
            service_interval = self.conf.get(conf, 'service_interval', 60)
            service_ports = self.conf.get(conf, 'service_ports', None)
            service_recvq = self.conf.get(conf, 'service_recvq', None)
            if service_ports is not None:
                service_task = task.Task('service_monitor', ServiceMonitor(service_ports, service_recvq),
                                         simple_trigger.SimpleTrigger(0, service_interval))
                self.container.add_task(service_task)
                
        # HostPing 主机存在监控 
        if self.conf.get(conf, 'host_monitor', 'true') == 'true':
            host_interval = self.conf.get(conf, 'host_interval', 60)
            host_address = self.conf.get(conf, 'host_address', None)
            host_timeout = self.conf.get(conf, 'host_timeout', 10)
            if host_address is not None:
                host_task = task.Task('host_monitor', HostPingMonitor(host_address, host_timeout),
                                         simple_trigger.SimpleTrigger(0, host_interval))
                self.container.add_task(host_task)
                

        
    def start(self):
        self.container.start_all(True)
        
class Monitor(job.Job):
    def __init__(self):
        pass
    
    def execute(self):
        pass
    
    def get_now(self):
        time_stamp = time.time()
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
        return time_now
    
class LinuxMonitor(Monitor):
    def __init__(self):
        self.linux_info = linux.LinuxInfo()
        
    def execute(self):
        pass
        
class CPUMonitor(LinuxMonitor):
    
    def __init__(self, threshold):
        LinuxMonitor.__init__(self)
        self.threshold = threshold
        
    def execute(self):
        summary, _ = self.linux_info.top()
        try:
            cpu_usage = summary.get('cpu-usage').split(',')
            if len(cpu_usage)  == 3:
                cpu_1m = float(cpu_usage[0].strip())
            else:
                raise ValueError('Read cpu usage from top Error')
        except:
            raise ValueError('Read cpu usage from top Error')
        
        if self.threshold < cpu_1m:
            print 'CPU Warning time: %s, 1m_usage: %d' % (self.get_now(), cpu_1m)
        
class MemoryMonitor(LinuxMonitor):
    def __init__(self, threshold):
        LinuxMonitor.__init__(self)
        self.threshold = threshold
        
    def execute(self):
        
        def parse_item(key): 
            try:
                value = mem.get(key)
                return float(value[:str(value).index(' ')])
            except:
                raise ValueError('Read memory key %s Error' % key)
        
        mem = self.linux_info.memory()
        if mem is not None and mem.has_key('MemTotal') and mem.has_key('MemFree'):
            total = parse_item('MemTotal')
            free = parse_item('MemFree')
            mem_usage = float((total - free) / total) * 100
            if self.threshold < mem_usage:
                print 'Memory Warning time: %s, usage: %d%% , total: %d, free: %d' % (self.get_now(), mem_usage, total, free)
        else:
            raise ValueError('Read memory usage from /proc/meminfo Error')
        
        
class DiskMonitor(LinuxMonitor):
    def __init__(self, mount, threshold):
        LinuxMonitor.__init__(self)
        self.mounts = map(lambda m: m.strip(), mount.split(';'))
        self.thresholds = map(lambda t: t.strip(), threshold.split(';'))
        if len(self.mounts) != len(self.thresholds):
            raise ValueError("Mount's length and Threshold's length are not equals")
        
    def execute(self):
        
        def index_monut(mount):
            for i in range(len(self.mounts)):
                if self.mounts[i] == mount:
                    return i
            return -1
        
        fs_list = self.linux_info.filesystem()
        try:
            for i in range(len(fs_list)):
                fs = fs_list[i]
                mount = fs.get('mount')
                m_idx = index_monut(mount)
                if m_idx != -1:
                    total, free = fs.get('total'), fs.get('free')
                    store_usage = fs.get('usage')
                    store_usage = float(store_usage[:len(store_usage)-1])
                    threshold = float(self.thresholds[m_idx])
                    if threshold < store_usage:
                        print 'Disk Warning time: %s, mount: %s, usage: %d%% , total: %s, free: %s' % (self.get_now(), mount, store_usage, total, free)
        except Exception, e:
            raise IOError(e)
        
class ProcessMonitor(LinuxMonitor):
    def __init__(self, pid):
        LinuxMonitor.__init__(self)
        self.pids = map(lambda p: p.strip(), pid.split(';'))
        
    def execute(self):
        
        ps_list = self.linux_info.ps(True)
        try:
            for pid in self.pids:
                active = False
                for ps in ps_list:
                    if pid == ps.get('pid'):
                        active = True
                        break
                if not active:
                    print 'Process Warning time: %s, pid: %s, error: Process NOT Found' % (self.get_now(), pid)
                    
        except Exception, e:
            raise IOError(e)
        
class ServiceMonitor(LinuxMonitor):
    def __init__(self, service_port, service_recvq):
        LinuxMonitor.__init__(self)
        self.service_ports = map(lambda p: p.strip(), service_port.split(';'))
        self.service_recvq = map(lambda r: r.strip(), service_recvq.split(';')) if service_recvq is not None else None
        if self.service_recvq is not None and len(self.service_ports) != len(self.service_recvq):
            raise ValueError("Service's length and Receive-Queue's length are not equals")
    
    def execute(self):
        service_list = self.linux_info.netstat('all')
        try:
            for i in range(len(self.service_ports)):
                service_port = self.service_ports[i]
                # active: 服务状态激活,  revq: Receive队列数量
                active, recvq = False, -1
                for service in service_list:
                    if service.get('local') == service_port:
                        active, recvq = True, int(service.get('recv-q'))
                        break
                if not active:
                    print 'Service Warning time: %s, service: %s, error: Service NO Active' % (self.get_now(), service_port)
                if active and self.service_recvq is not None and recvq > int(self.service_recvq[i]):
                    print 'Service Warning time: %s, service: %s, receive-queue: %d, error: Out of Receive-Queue' % (self.get_now(), service_port, recvq)
        except Exception, e:
            raise IOError(e)

class NetMonitor(Monitor):
    def __init__(self):
        self.ping_icmp = ping_icmp.PingICMP()
        
    def execute(self):
        pass
    
class HostPingMonitor(NetMonitor):
    def __init__(self, host, timeout = 10):
        NetMonitor.__init__(self)
        self.hosts = map(lambda h: h.strip(), host.split(';'))
        self.timeout = timeout
    
    def execute(self):
        for host in self.hosts:
            ping_ret_lst = self.ping_icmp.ping(host, self.timeout, 1)
            if len(ping_ret_lst) > 0:
                ping_ret = ping_ret_lst[0].get('result')
                if ping_ret != 'success':
                    print 'Host Warning time: %s, host: %s, result: %s' % (self.get_now(), host, ping_ret)
    
    
if __name__ == '__main__':
    monitor = SystemMonitor('../../../conf/sys.conf')
    monitor.start()
    
        