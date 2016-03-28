# coding=utf-8

import platform

from py_sys.utils import decorator
from py_sys import execute
 
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
    
    @decorator.check_os(['linux'])
    def filesystem(self):
        df_info = []
        exec_result = execute.run('df -a -BK')
        if exec_result:
            line_count, skip_line = 0, 1
            for line in exec_result:
                line_count += 1
                if skip_line >= line_count:
                    continue
                df_items = self.__split(line, ' ')
                columns = ['fs','total','used', 'free', 'usage', 'mount']
                df = self.__map(df_items, columns)
                if len(df) > 0:
                    df_info.append(df)
        return df_info
    
    @decorator.check_os(['linux'])
    @decorator.check_file('/proc/net/dev')
    def net_if(self):
        iface_info = []
        line_count, skip_line = 0, 2
        with open('/proc/net/dev') as f:
            for line in f:
                line_count += 1
                if skip_line >= line_count:
                    continue
                iface_items = self.__split(line, ' ')
                columns = ['iface','r-bytes','r-packets', 'r-errs', 'r-drop', 'r-fifo', 'r-frame', 'r-compressed', 'r-multicast',
                           't-bytes', 't-packets', 't-errs', 't-drop', 't-fifo', 't-colls', 't-carrier', 't-compressed']
                iface = self.__map(iface_items, columns)
                if iface.has_key('iface'):
                    iface_name = iface.get('iface')
                    iface['iface'] = iface_name[:len(iface_name) -1]
                    iface_info.append(iface)
        return iface_info
    
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

    def __split(self, line, sep, strip = True):
        if line and sep:
            result = []
            items = line.split(sep)
            for item in items:
                item = item.strip() if strip else item
                if item:
                    result.append(item)
            return result

    def __map(self, items, columns):
        data = {}
        if items and columns and len(items) == len(columns):
            for i in range(len(items)):
                data[columns[i]] = items[i]
        return data
         
