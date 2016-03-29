# coding=utf-8

import wmi
import platform

from py_sys.utils import decorator

class WindowsInfo():
    def __init__(self):
        self.w = wmi.WMI ()
        self.pv = 32 if '32 bit' in platform.python_compiler() else 64
    
    @decorator.check_os(['windows'])
    def cpu(self):
        func = self.w.Win32_Processor() if self.pv == 32 else self.w.Win_Processor()
        return self.__info(func)
    
    @decorator.check_os(['windows'])
    def memory(self):
        func = self.w.Win32_PhysicalMemory() if self.pv == 32 else self.w.Win_PhysicalMemory()
        return self.__info(func)
            
    def __info(self, func):
        info_list = []
        for item in func:
            info = {}
            for prop_key in item._properties:
                prop_value = item.__getattr__(prop_key)
                info[prop_key] = prop_value
            info_list.append(info)
        return info_list
