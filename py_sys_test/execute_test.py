# coding=utf-8

import platform
from py_sys import execute

import unittest

class ExecuteTest(unittest.TestCase):
    
    def test_run(self):
        os_type = platform.system().lower()
        if os_type == 'windows':
            output = execute.run('ver', 'gbk', True)
            self.assertTrue('Microsoft Windows' in output[0])
        elif os_type == 'linux':
            output = execute.run('uname -a', 'utf-8', True)