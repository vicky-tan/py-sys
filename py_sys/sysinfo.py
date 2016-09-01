# coding=utf-8

import platform
from info import linux, windows

os_t = platform.system().lower()
if os_t == 'linux':
    __os = linux.LinuxInfo()
elif os_t == 'windows':
    __os = windows.WindowsInfo()
else:
    raise 'Not Support : ' + os_t

def cpu():
    return __os.cpu()

def top():
    return __os.top()

def ps(system=True):
    return __os.ps(system)

def memory():
    return __os.memory()

def filesystem():
    return __os.filesystem()

def net_if():
    return __os.net_if()

def system():
    system = {
              'hostname' : platform.node(),
              'system'  : platform.system(),
              'machine' : platform.machine(),
              'architecture' : platform.architecture(),
              'release' : platform.release(),
              'dist' : platform.dist(),
              'python' : platform.python_version()
              }
    return system


    