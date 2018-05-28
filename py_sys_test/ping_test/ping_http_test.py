# coding=utf-8

import unittest
from py_sys.ping import ping_http

class Test(unittest.TestCase):

    def test_ping_http(self):
        p = ping_http.PingHTTP()
        result = p.ping('http://www.baidu.com', 80, 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'success')
            
    def test_ping_https(self):
        p = ping_http.PingHTTP()
        result = p.ping('https://www.baidu.com', 443, 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'success')
            
    def test_ping_timeout(self):
        p = ping_http.PingHTTP()
        result = p.ping('www.baidu.com', 8080, 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'timeout')
    
    def test_ping_err(self):
        p = ping_http.PingHTTP()
        result = p.ping('nosuchhost', 80, 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'timeout')  
if __name__ == "__main__":
    unittest.main()