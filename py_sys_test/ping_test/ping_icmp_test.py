# coding=utf-8

import unittest
from py_sys.ping import ping_icmp

class Test(unittest.TestCase):

    def test_ping(self):
        p = ping_icmp.PingICMP()
        result = p.ping_icmp('127.00.1', 1, 5)
        for item in result:
            self.assertEqual(item.get('result'), 'success')

if __name__ == "__main__":
    unittest.main()