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
        
    def test_top(self):
        linux_info = linux.LinuxInfo()
        summary, ps_info = linux_info.top()
        self.assertTrue(summary.has_key('uptime'))
        self.assertTrue(summary.has_key('cpu-usage'))
        self.assertGreaterEqual(len(ps_info), 1)
        self.assertEquals(len(ps_info[0]), 12)
        
    def test_ps(self): 
        linux_info = linux.LinuxInfo()
        ps_info = linux_info.ps(False)
        self.assertGreaterEqual(len(ps_info), 1)
        self.assertEquals(len(ps_info[0]), 8)
        
    def test_filesystem(self):
        linux_info = linux.LinuxInfo()
        df_info = linux_info.filesystem()
        self.assertGreaterEqual(len(df_info), 1)
        self.assertEquals(len(df_info[0]), 7)
        
    def test_net_if(self):
        linux_info = linux.LinuxInfo()
        iface_info = linux_info.net_if()
        self.assertGreaterEqual(len(iface_info), 1)
        self.assertEquals(len(iface_info[0]), 17)
        
    def test_netstat(self):
        linux_info = linux.LinuxInfo()
        netstat_info = linux_info.netstat('tcp')
        self.assertGreaterEqual(len(netstat_info), 1)
        self.assertEquals(len(netstat_info[0]), 7)
        
    def test_iostat(self):
        linux_info = linux.LinuxInfo()
        iostat_info = linux_info.iostat()
        