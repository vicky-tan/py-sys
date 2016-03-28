# coding=utf-8

from py_sys.info import linux

import unittest

class LinuxInfoTest(unittest.TestCase):
    def test_cpu(self):
        linux_info = linux.LinuxInfo()
        cpu_info = linux_info.cpu()
        self.assertGreaterEqual(len(cpu_info), 1)
        self.assertTrue(cpu_info[0].has_key('processor'))
        self.assertTrue(cpu_info[0].has_key('model name'))
        
    def test_memory(self):
        linux_info = linux.LinuxInfo()
        mem_info = linux_info.memory()
        self.assertTrue(mem_info.has_key('MemTotal'))
        self.assertTrue(mem_info.has_key('MemFree'))
        
    def test_net_if(self):
        linux_info = linux.LinuxInfo()
        iface_info = linux_info.net_if()
        self.assertGreaterEqual(len(iface_info), 1)
        
    def test_system(self):
        linux_info = linux.LinuxInfo()
        sys_info = linux_info.system()
        self.assertIsNotNone(sys_info.get('hostname'))
        self.assertTrue(sys_info.has_key('uptime'))
        self.assertTrue(sys_info.has_key('version'))