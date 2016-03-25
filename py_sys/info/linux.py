# coding=utf-8

import platform

from py_sys.utils import decorator

class LinuxInfo():
    @decorator.check_os(['linux'])
    @decorator.check_file('/proc/cpuinfo')
    def cpu(self):
        cpu_info = []
        with open('/proc/cpuinfo') as f:
            cpu = {}
            for line in f:
                if not line.strip():
                    cpu_info.append(cpu)
                    cpu = {}
                else:
                    if len(line.split(':')) == 2:
                        cpu[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        cpu[line.split(':')[0].strip()] = ''
        return cpu_info
    
    @decorator.check_os(['linux'])
    @decorator.check_file('/proc/meminfo')
    def memory(self):
        mem_info = {}
        with open('/proc/meminfo') as f:
            for line in f:
                mem_info[line.split(':')[0]] = line.split(':')[1].strip()
        return mem_info
    
    def partitions(self):
        pass
    
    def interface(self):
        pass
    
    def device(self):
        pass
    
    def process(self):
        pass
    
    def filesystem(self):
        pass
    
    @decorator.check_os(['linux'])
    @decorator.check_file(['/proc/uptime', '/proc/version'])
    def system(self):
        system = {
                  'hostname' : platform.node(),
                  'system'  : platform.system(),
                  'machine' : platform.machine(),
                  'architecture' : platform.architecture(),
                  'release' : platform.release(),
                  'dist' : platform.dist(),
                  'version' : open('/proc/version').readline(),
                  'uptime' : open('/proc/uptime').readline(),
                  'python' : platform.python_version()
                  }
        return system


