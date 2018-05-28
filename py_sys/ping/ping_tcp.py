# coding=utf-8

import socket
import time

class PingTCP(object):
    
    def __init__(self):
        pass
    
    def ping_once(self, dest_addr, timeout):
        
        start_time = time.time()
        
        try:
            tcp_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp_socket.settimeout(timeout)
            tcp_socket.connect(dest_addr)
            tcp_socket.send('hello\r')
            tcp_socket.close()
            
            return time.time() - start_time
        except socket.timeout:
            return None
        except socket.error:
            raise socket.error
        
    
    def ping(self, host_name, port, timeout = 10, count = 5):
        
        ping_result_list = []
        
        try:
            dest_addr = socket.gethostbyname(host_name)
        except socket.gaierror, e:
            raise IOError('%s is not right hostname or ip' % host_name)
        
        for _ in xrange(count):
            ping_result = {'host_name' : host_name, 'dest_addr' : dest_addr, 'dest_port' : port}
            try:
                delay = self.ping_once((dest_addr, port), timeout)
                if delay is not None:
                    ping_result['result'] = 'success'
                    ping_result['delay'] = delay * 1000
                else:
                    ping_result['result'] = 'timeout'
            except socket.gaierror, e:
                ping_result['result'] = 'exception'
                ping_result['message'] = e
            
            ping_result_list.append(ping_result)
            
        return ping_result_list
        