# coding=utf-8

import os

def run(cmd, decoding = None, clean = False):
    if cmd:
        result = []
        output = os.popen(cmd).readlines()
        for line in output:
            if decoding:
                line = line.decode(decoding)
            if clean:
                line = line.strip()
            if line and line != '':
                result.append(line)
        return result
    else:
        raise ValueError('Command is Empty')
    
