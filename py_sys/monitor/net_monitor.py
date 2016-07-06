# coding=utf-8

from py_sys.monitor import monitor
from py_sys.ping import ping_icmp

class NetMonitor(monitor.Monitor):
    def __init__(self):
        self.ping_icmp = ping_icmp.PingICMP()
        
    def execute(self):
        pass
    
class HostPingMonitor(NetMonitor):
    def __init__(self, host, timeout = 10):
        NetMonitor.__init__(self)
        self.hosts = map(lambda h: h.strip(), host.split(';'))
        self.timeout = timeout
    
    def execute(self):
        for host in self.hosts:
            ping_ret_lst = self.ping_icmp.ping(host, self.timeout, 1)
            if len(ping_ret_lst) > 0:
                ping_ret = ping_ret_lst[0].get('result')
                if ping_ret != 'success':
                    print 'Host Warning time: %s, host: %s, result: %s' % (self.get_now(), host, ping_ret)