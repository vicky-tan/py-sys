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
        