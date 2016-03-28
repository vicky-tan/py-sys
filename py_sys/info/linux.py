# coding=utf-8

import platform
import re

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
    @decorator.check_cmd(['top -version > /dev/null'])
    def top(self):
        summary = {}
        ps_list = []
        
        exec_result = execute.run('top -n 1 -b')
        if exec_result and len(exec_result) > 6:
            pattern = re.compile('top - (.*) up  (.*),  (\d+) users,  load average: (.*)')
            match = pattern.match(exec_result[0])
            if match:
                items = match.groups()
                if items and len(items) == 4:
                    summary = {'startup' : items[0], 'uptime' : items[1], 
                               'users' : items[2], 'cpu-usage' : items[3]}
            
            prefixs = ['task', 'cpu', 'memory', 'swap']
            for line_num in range(1,5):
                line = exec_result[line_num]
                line = line[line.index(':') + 1:]
                items = self.__split(line, ',')
                for item in items:
                    _i = item.split(' ')
                    if len(_i) == 2:
                        prefix = prefixs[line_num - 1]
                        if not summary.has_key(prefix):
                            summary[prefix] = {}
                        summary[prefix][_i[1]] = _i[0]
            
            for line in exec_result[7:]:
                ps_items = self.__split(line, ' ', True, 12)
                columns = ['pid', 'uid', 'pr', 'ni', 'virt', 'res', 'shr', 'stime', 'cpu', 'mem', 'rtime', 'cmd']
                ps = self.__map(ps_items, columns)
                if len(ps) > 0:
                    ps_list.append(ps)
                    
        return summary, ps_list
                    
    @decorator.check_os(['linux'])
    @decorator.check_cmd(['ps --version > /dev/null'])
    def ps(self, system = True):
        ps_info = []
        
        def action(line):
            ps_items = self.__split(line, ' ', True, 8)
            columns = ['uid', 'pid', 'ppid', 'c', 'stime', 'tty', 'time', 'cmd']
            ps = self.__map(ps_items, columns)
            if len(ps) > 0:
                ps_info.append(ps)
                
        self.__exec('ps -ef', 1, action)
        if not system:
            filtered_ps = []
            for ps in ps_info:
                cmd = ps.get('cmd')
                if cmd and cmd.startswith('[') and cmd.endswith(']'):
                    continue
                filtered_ps.append(ps)
            return filtered_ps
        else:
            return ps_info
    
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
        
        def action(line):
            df_items = self.__split(line, ' ')
            columns = ['fs', 'type', 'total', 'used', 'free', 'usage', 'mount']
            df = self.__map(df_items, columns)
            if len(df) > 0:
                df_info.append(df)
        
        self.__exec('df -a -BK -T', 1, action)
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
    
    def __exec(self, cmd, skip, action):
        exec_result = execute.run(cmd)
        if exec_result:
            line_count, skip_line = 0, 1
            for line in exec_result:
                line_count += 1
                if skip_line >= line_count:
                    continue
                action(line)
                
    def __split(self, line, sep, strip = True, size = 0):
        if line and sep:
            result = []
            items = line.split(sep)
            for item in items:
                item = item.strip() if strip else item
                if item:
                    result.append(item)
            if size > 0 and len(result) > size:
                prefix = result[:size-1]
                suffix = sep.join(result[size-1:len(result)])
                result = prefix
                result.append(suffix)
            return result

    def __map(self, items, columns):
        data = {}
        if items and columns and len(items) == len(columns):
            for i in range(len(items)):
                data[columns[i]] = items[i]
        return data
    