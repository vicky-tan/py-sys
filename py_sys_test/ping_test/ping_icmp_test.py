# coding=utf-8

import unittest
from py_sys.ping import ping_icmp

class Test(unittest.TestCase):

    def test_ping(self):
        p = ping_icmp.PingICMP()
        result = p.ping('127.0.0.1', 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'success')
            
    def test_ping_timeout(self):
        p = ping_icmp.PingICMP()
        result = p.ping('192.168.1.2', 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'timeout')
if __name__ == "__main__":
    unittest.main()