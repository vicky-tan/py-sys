# coding=utf-8

import os
import zipfile

class ZipFile(object):

    def __init__(self):
        pass
    
    def zip(self, dir_path, zip_file):
        file_list = []
        
        def walk_dir(sub_dir):
            for root, dirs, files in os.walk(sub_dir):
                for _file in files:
                    file_list.append(os.path.join(root, _file))
                for _dir in dirs:
                    walk_dir(_dir)
        
        if os.path.isfile(dir_path):
            file_list.append(dir_path)
        else :
            walk_dir(dir_path)
             
        zf = zipfile.ZipFile(zip_file, "w", zipfile.zlib.DEFLATED)
        
        for tar in file_list:
            arcname = tar[len(dir_path):]
            zf.write(tar, arcname)
        zf.close()
    
    def unzip(self, zip_file, dir_path):
        if not os.path.exists(dir_path): os.mkdir(dir_path, 0777)
        
        zf_obj = zipfile.ZipFile(zip_file)
        
        for zf_name in zf_obj.namelist():
            zf_name = zf_name.replace('\\','/')
            
            if zf_name.endswith('/'):
                os.mkdir(os.path.join(dir_path, zf_name))
            else:            
                ext_file = os.path.join(dir_path, zf_name)
                ext_dir= os.path.dirname(ext_file)
                
                if not os.path.exists(ext_dir): 
                    os.mkdir(ext_dir,0777)
                    
                out_file = open(ext_file, 'wb')
                out_file.write(zf_obj.read(zf_name))
                out_file.close()

        
