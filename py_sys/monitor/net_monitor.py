# coding=utf-8

import types

from py_sys.monitor import monitor
from py_sys.ping import ping_icmp, ping_tcp, ping_http

class NetMonitor(monitor.Monitor):
    def __init__(self):
        self.ping_icmp = ping_icmp.PingICMP()
        self.ping_tcp = ping_tcp.PingTCP()
        self.ping_http = ping_http.PingHTTP()
        
    def execute(self):
        pass
    
class HostPingMonitor(NetMonitor):
    def __init__(self, host, timeout = 10):
        NetMonitor.__init__(self)
        self.hosts = map(lambda h: h.strip(), host.split(';'))
        self.timeout = timeout
    
    def execute(self, callback):
        for host in self.hosts:
            ping_ret_lst = self.ping_icmp.ping(host, self.timeout, 3)
            if len(ping_ret_lst) > 0:
                ping_ret = ping_ret_lst[0].get('result')
                if ping_ret != 'success':
                    if callback is not None and type(callback) == types.FunctionType:
                        callback(host, ping_ret)
                    self.output('Host Warning time: %s, host: %s, result: %s' % (self.get_now(), host, ping_ret))
                    
class TcpPingMonitor(NetMonitor):
    def __init__(self, host, port, timeout = 10):
        NetMonitor.__init__(self)
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def execute(self, callback):
        ping_ret_lst = self.ping_icmp.ping(self.host, self.timeout, 3)
        if len(ping_ret_lst) > 0:
            ping_ret = ping_ret_lst[0].get('result')
            if ping_ret != 'success':
                if callback is not None and type(callback) == types.FunctionType:
                    callback(self.host, self.port, ping_ret)
                self.output('Host Warning time: %s, host: %s, result: %s' % (self.get_now(), self.host, self.port, ping_ret))

class UrlMonitor(NetMonitor):
    def __init__(self, url, port, timeout = 10):
        NetMonitor.__init__(self)
        self.url = url
        self.timeout = timeout
        
    def execute(self, callback):
        ping_ret_lst = self.ping_http.ping(self.url, self.port, self.timeout, 3)
        if len(ping_ret_lst) > 0:
            ping_ret = ping_ret_lst[0].get('result')
            if ping_ret != 'success':
                if callback is not None and type(callback) == types.FunctionType:
                    callback(self.url, ping_ret)
                self.output('URL Warning time: %s, url: %s, result: %s' % (self.get_now(), self.url, ping_ret))
        