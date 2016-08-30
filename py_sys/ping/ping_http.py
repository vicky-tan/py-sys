# coding=utf-8

import httplib
import socket
import time

class PingHTTP(object):
    
    def __init__(self):
        pass
    
    def ping_once(self, url, port, timeout):
        
        start_time = time.time()
        
        is_ssl = True if 'https' in url or port is 443 else False
        url = url[url.index('://') + 3:] if '://' in url else url
        
        http_client = None
        try:
            if is_ssl:
                http_client = httplib.HTTPSConnection(url, port, None, None, None, timeout)
            else:
                http_client = httplib.HTTPConnection(url, port, timeout)
                    
            http_client.request('GET', '/')
            
            response = http_client.getresponse()
            return time.time()- start_time, response.status
        except socket.timeout:
            return None, 0
        except Exception, (err, _):
            if err == 10060:
                return None, 0
            else:
                raise IOError(err)
        finally:
            if http_client:
                http_client.close()
        
    
    def ping(self, url, port = 80, timeout = 10, count = 5):
        
        ping_result_list = []
        
        if url is None:
            raise IOError('URL is None')
        
        url = url.lower()

        for _ in xrange(count):
            ping_result = {'url' : url, 'port' : port}
            try:
                delay, status = self.ping_once(url, port, timeout)
                if delay is not None:
                    ping_result['result'] = 'success'
                    ping_result['delay'] = delay * 1000
                    ping_result['status'] = status
                else:
                    ping_result['result'] = 'timeout'
            except Exception, e:
                ping_result['result'] = 'exception'
                ping_result['message'] = e
            
            ping_result_list.append(ping_result)
            
        return ping_result_list
        