# coding=utf-8

from ctypes import *

from py_sys.utils import decorator

class WindowsInfo():
    def __init__(self):
        pass
    
    @decorator.check_os(['windows'])
    def cpu(self):
        pass
    
    @decorator.check_os(['windows'])
    def memory(self):
        pass


