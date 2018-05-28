# coding=utf-8

import sys
import os
import codecs

class SysEnvToFile():
    
    def read_file(self, filename, encoding = 'utf-8'):
        if self.is_empty(filename):
            raise IOError('filename is None')
        
        text = []
        try:   
            text_file = codecs.open(filename, 'r', encoding)
            text = [line for line in text_file.readlines()]
            text_file.close()
        except IOError:
            text = None

        return text
    
    def write_file(self, filename, text, encoding = 'utf-8'):
        if self.is_blank(filename):
            raise IOError('filename is None')
        
        try:
            text_file = codecs.open(filename, 'w', encoding)
            
            if isinstance(text, list):
                for line in text:
                    text_file.write(line)
            elif isinstance(text, basestring):
                text_file.write(text)
                
            text_file.close()
        except IOError:
            pass
    
    def is_empty(self, string):
        if not string:
            return True
        string = self.to_string(string)
        if string == '':
            return True
        string = string.strip()
        if string == '':
            return True
        return False
    
    def is_blank(self, string):
        return True if string == None else False
    
    def to_string(self, string):
        if self.is_blank(string):
            return None
        if isinstance(string, basestring):
            return string
        return str(string)
    
    def replace_all(self, string, search_str, replacement):
        if self.is_blank(string):
            return None
        
        string = self.to_string(string)
        if self.is_blank(search_str) or self.is_blank(replacement):
            return string
        
        search_str = self.to_string(search_str)
        replacement = self.to_string(replacement)
    
        return string.replace(search_str, replacement)
    
    def build(self, template_file, output_file):
        template = self.read_file(template_file)
        
        if template: 
            env_dist = os.environ
            replaced_text = []
            for line in template:
                for key in env_dist:
                    env_key = '${' + key + '}'
                    env_val = env_dist[key]
                    line = self.replace_all(line, env_key, env_val)
                replaced_text.append(line)
            
            self.write_file(output_file, replaced_text)  
        
if __name__ == '__main__':
    worker = SysEnvToFile()
    
    if len(sys.argv) == 3:
        template_file = sys.argv[0]
        output_file = sys.argv[1]
        
        worker.build(template_file, output_file)
    else:
        print 'Not enough parameters'
        exit(1)
        