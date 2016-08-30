# coding=utf-8

import types

from py_sys.monitor import monitor
from py_sys.info import linux

class LinuxMonitor(monitor.Monitor):
    def __init__(self):
        self.linux_info = linux.LinuxInfo()
        
    def execute(self):
        pass
        
class CPUMonitor(LinuxMonitor):
    
    def __init__(self, threshold):
        LinuxMonitor.__init__(self)
        self.threshold = threshold
        
    def execute(self, callback):
        summary, _ = self.linux_info.top()
        try:
            cpu_usage = summary.get('cpu-usage').split(',')
            if len(cpu_usage) == 3:
                cpu_1m = float(cpu_usage[0].strip())
            else:
                raise ValueError('Read cpu usage from top Error')
        except:
            raise ValueError('Read cpu usage from top Error')
        
        if self.threshold < cpu_1m:
            if callback is not None and type(callback) == types.FunctionType:
                callback(cpu_1m)
            self.output('CPU Warning time: %s, 1m_usage: %d' % (self.get_now(), cpu_1m))
        
class MemoryMonitor(LinuxMonitor):
    def __init__(self, threshold):
        LinuxMonitor.__init__(self)
        self.threshold = threshold
        
    def execute(self, callback):
        
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
            usage = float((total - free) / total) * 100
            if self.threshold < usage:
                if callback is not None and type(callback) == types.FunctionType:
                    callback(usage, total, free)
                self.output('Memory Warning time: %s, usage: %d%% , total: %d, free: %d' % (self.get_now(), usage, total, free))
        else:
            raise ValueError('Read memory usage from /proc/meminfo Error')
        
        
class DiskMonitor(LinuxMonitor):
    def __init__(self, mount, threshold):
        LinuxMonitor.__init__(self)
        self.mounts = map(lambda m: m.strip(), mount.split(';'))
        self.thresholds = map(lambda t: t.strip(), threshold.split(';'))
        if len(self.mounts) != len(self.thresholds):
            raise ValueError("Mount's length and Threshold's length are not equals")
        
    def execute(self, callback):
        
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
                    usage = fs.get('usage')
                    usage = float(usage[:len(usage) - 1])
                    threshold = float(self.thresholds[m_idx])
                    if threshold < usage:
                        if callback is not None and type(callback) == types.FunctionType:
                            callback(mount, usage, total, free)
                        self.output('Disk Warning time: %s, mount: %s, usage: %d%% , total: %s, free: %s' % (self.get_now(), mount, usage, total, free))
        except Exception, e:
            raise IOError(e)
        
class ProcessMonitor(LinuxMonitor):
    def __init__(self, pid):
        LinuxMonitor.__init__(self)
        self.pids = map(lambda p: p.strip(), pid.split(';'))
        
    def execute(self, callback):
        
        ps_list = self.linux_info.ps(True)
        try:
            for pid in self.pids:
                active = False
                for ps in ps_list:
                    if pid == ps.get('pid'):
                        active = True
                        break
                if not active:
                    if callback is not None and type(callback) == types.FunctionType:
                        callback(pid)
                    self.output('Process Warning time: %s, pid: %s, error: Process NOT Found' % (self.get_now(), pid))
                    
        except Exception, e:
            raise IOError(e)
        
class ServiceMonitor(LinuxMonitor):
    def __init__(self, service_port, service_recvq):
        LinuxMonitor.__init__(self)
        self.service_ports = map(lambda p: p.strip(), service_port.split(';'))
        self.service_recvq = map(lambda r: r.strip(), service_recvq.split(';')) if service_recvq is not None else None
        if self.service_recvq is not None and len(self.service_ports) != len(self.service_recvq):
            raise ValueError("Service's length and Receive-Queue's length are not equals")
    
    def execute(self, callback):
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
                    if callback is not None and type(callback) == types.FunctionType:
                        callback(service_port, -1)
                    self.output('Service Warning time: %s, service: %s, error: Service NO Active' % (self.get_now(), service_port))
                if active and self.service_recvq is not None and recvq > int(self.service_recvq[i]):
                    if callback is not None and type(callback) == types.FunctionType:
                        callback(service_port, recvq)
                    self.output('Service Warning time: %s, service: %s, receive-queue: %d, error: Out of Receive-Queue' % (self.get_now(), service_port, recvq))
        except Exception, e:
            raise IOError(e)


    
        
