# coding=utf-8

import time
from task.job import job

class Monitor(job.Job):
    def __init__(self):
        pass
    
    def execute(self):
        pass
    
    def get_now(self):
        time_stamp = time.time()
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
        return time_now
    
    def output(self, message):
        print message