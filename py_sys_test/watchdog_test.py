# coding=utf-8

from py_sys import watchdog

class WatchDogTest():
    
    def __init__(self):
        pass
    
    def test_watch_dog(self):
        processes = {5447 : 'echo warning > ~/warning '}
        wd = watchdog.WatchDog()
        wd.watch(processes)
        wd.start()
    
if __name__ == '__main__':
    wdt = WatchDogTest()
    wdt.test_watch_dog()