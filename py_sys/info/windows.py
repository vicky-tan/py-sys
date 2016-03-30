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
        cpu = self.w.Win32_Processor() if self.pv == 32 else self.w.Win_Processor()
        return self.__info(cpu)
    
    @decorator.check_os(['windows'])
    def memory(self):
        mem = self.w.Win32_PhysicalMemory() if self.pv == 32 else self.w.Win_PhysicalMemory()
        return self.__info(mem)
    
    @decorator.check_os(['windows'])
    def top(self):
        if self.pv == 32:
            top = self.w.Win32_PerfFormattedData_PerfProc_Process() 
        else:
            top = self.w.Win_PerfFormattedData_PerfProc_Process()
        return self.__info(top)
    
    @decorator.check_os(['windows'])
    def ps(self):
        ps = self.w.Win32_Process() if self.pv == 32 else self.w.Win_Process()
        return self.__info(ps)
    
    @decorator.check_os(['windows'])
    def filesystem(self):
        disk_drive = self.w.Win32_DiskDrive () if self.pv == 32 else self.w.Win_DiskDrive ()
        logic_disk = self.w.Win32_LogicalDisk() if self.pv == 32 else self.w.LogicalDisk ()
        return self.__info(disk_drive), self.__info(logic_disk)
    
    @decorator.check_os(['windows'])
    def net_if(self):
        net = self.w.Win32_NetworkAdapterConfiguration()  if self.pv == 32 else self.w.Win_NetworkAdapterConfiguration()
        return self.__info(net)
    
    def __info(self, func):
        info_list = []
        for item in func:
            info = {}
            for prop_key in item._properties:
                prop_value = item.__getattr__(prop_key)
                info[prop_key] = prop_value
            info_list.append(info)
        return info_list
