# coding=utf-8

from py_sys.info import windows

import unittest

class WindowsInfoTest(unittest.TestCase):
    def test_cpu(self):
        windows_info = windows.WindowsInfo()
        cpu_info = windows_info.cpu()
        self.assertGreaterEqual(len(cpu_info), 1)
        
    def test_memory(self):
        windows_info = windows.WindowsInfo()
        mem_info = windows_info.memory()
        self.assertGreaterEqual(len(mem_info), 1)
        
    def test_filesystem(self):
        windows_info = windows.WindowsInfo()
        disk_drive, logic_disk = windows_info.filesystem()
        self.assertGreaterEqual(len(disk_drive), 1)
        self.assertGreaterEqual(len(logic_disk), 1)
        
    def test_net_if(self):
        windows_info = windows.WindowsInfo()
        net_info = windows_info.net_if()
        self.assertGreaterEqual(len(net_info), 1)
        