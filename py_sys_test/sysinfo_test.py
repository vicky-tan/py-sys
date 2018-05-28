# coding=utf-8

from py_sys import sysinfo

import unittest

class SysinfoTest(unittest.TestCase):
    
    def test_cpu(self):
        cpu_info = sysinfo.cpu()
        self.assertGreaterEqual(len(cpu_info), 1)
        
    def test_memory(self):
        mem_info = sysinfo.cpu()
        self.assertGreaterEqual(len(mem_info), 1)
        
    def test_top(self):
        summary, ps_info = sysinfo.top()
        self.assertGreaterEqual(len(summary), 1)
        self.assertGreaterEqual(len(ps_info), 1)
        
    def test_ps(self): 
        ps_info = sysinfo.ps(False)
        self.assertGreaterEqual(len(ps_info), 1)
        
    def test_filesystem(self):
        df_info = sysinfo.filesystem()
        self.assertGreaterEqual(len(df_info), 1)
        
    def test_net_if(self):
        iface_info = sysinfo.net_if()
        self.assertGreaterEqual(len(iface_info), 1)
        
    def test_system(self):
        sys_info = sysinfo.system()
        self.assertIsNotNone(sys_info.get('hostname'))
        self.assertIsNotNone(sys_info.get('system'))
        