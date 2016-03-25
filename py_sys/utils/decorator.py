# coding=utf-8

import os
import platform

def check_os(os_list):
    def decorators(func):
        def wrapper(*args, **kwargs):
            os_t = platform.system().lower()
            if os_t not in os_list:
                raise ValueError('Not Support :' + os_t)
            return func( *args , **kwargs)
        return wrapper
    return decorators

def check_file(filename):
    def decorators(func):
        def wrapper(*args, **kwargs):
            if filename != None:
                if (isinstance(filename, str) or isinstance(filename, unicode)) and not os.path.exists(filename):
                    raise IOError('File not exists :' + filename)
                elif isinstance(filename, list):
                    for _fn in filename:
                        if not os.path.exists(_fn):
                            raise IOError('File not exists :' + _fn)
            else:
                raise IOError('Filename is None')
            return func( *args , **kwargs)
        return wrapper
    return decorators