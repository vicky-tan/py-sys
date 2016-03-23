# coding=utf-8

from py_sys.utils import decorator

class LinuxInfo():
    @decorator.check_os(['linux'])
    @decorator.check_file('/proc/cpuinfo')
    def cpu(self):
        nprocs = 0
        cpu_info = {}
        proc_info = {}
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    #end of one processor
                    cpu_info['proc%s' % nprocs] = proc_info
                    nprocs = nprocs + 1
                    #Reset
                    proc_info = {}
                else:
                    if len(line.split(':')) == 2:
                        proc_info[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        proc_info[line.split(':')[0].strip()] = ''
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
    
    def version(self):
        pass


