#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    upcloud.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Wed 16 Apr 2014 08:03:45 PM CST
# @Copyright:    MIT applies
# @Description:  Perform interactive command                   
#########################################################################
import os
import upyun
from progressbar import *

class ProgressBarHandler(object):
    def __init__(self, totalsize, params):
        widgets = [params, Percentage(), ' ',
                   Bar(marker='>', left='[', right=']'), ' ',
                   ETA(), ' ', FileTransferSpeed()]
        self.pbar = ProgressBar(widgets=widgets, maxval=totalsize).start()
 
    def update(self, readsofar):
        self.pbar.update(readsofar)
 
    def finish(self):
        self.pbar.finish()

class upcloud():
 
    def __init__(self, bucketname=None, username=None, password=None, timeout=30, endpoint=upyun.ED_AUTO, workspace='/'):
        ''' Initialize the user infomation and the access point !
            param:
                 bucketname    --   your space's name
                 username      --   your operator's name of this space
                 password      --   your operator's password
                 timeout       --   the HTTP request timeout time, default is 30s
                 endpoint      --   your network access point: ED_AUTO, ED_TELECOM, ED_CNC, ED_CTT
                 workspace     --   current workspace,default is '/'
        '''
        self.BUCKETNAME = bucketname
        self.USERNAME   = username
        self.PASSWORD   = password
        self.TIMEOUT    = timeout
        self.ENDPOINT   = endpoint
        self.WORKSPACE  = workspace
        
        self.cloud = upyun.UpYun(self.BUCKETNAME, 
                                 self.USERNAME, 
                                 self.PASSWORD, 
                                 self.TIMEOUT, 
                                 self.ENDPOINT)
        self.print_connect_info()

    def upload(self, src, des='/'):
       # print "Uploading file ..."
       # headers = {"x-gmkerl-rotate": "180"}
       # 当文件为空时，progressbar无法处理，会抛出异常ZeroDivisionError。
        if os.path.getsize(src) != 0:
            with open(src, 'rb') as f:
                res = self.cloud.put(des, f, checksum=False, handler=ProgressBarHandler, params="Uploading ")
        else:
            #print "File %s is empty ! ingored. File is not uploaded." % src
            print "File %s is empty ! uploading ..." % src
            with open(src, 'rb') as f:
                res = self.cloud.put(des, f, checksum=False)
    
    def download(self, src, des):
       # print "Downloading file ..."
        file_path = '/'.join(des.split('/')[:-1])
        # 处理文件以/开头的情况
        if file_path: 
            if not os.path.exists(file_path):
                os.makedirs(file_path)
        with open(des, 'wb') as f:
            self.cloud.get(src, f, handler=ProgressBarHandler, params="Downloading ")
    
    def cat(self, path):
        cache_path = '/tmp/upcloud'
        file_path = cache_path+'/'.join(path.split('/')[:-1])+'/'
        file_name = '/'.join(path.split('/')[-1:])
        
        if not os.path.exists(file_path):
            os.makedirs(file_path)
      
        cache_file =  file_path + file_name 
        if os.path.exists(cache_file) and not os.path.isdir(cache_file):
            return cache_file
        else:
            with open(cache_file, 'wb') as f:
                self.cloud.get(path, f)
                return cache_file 

    def mkdir(self, path):
        print 'creating directory %s ...' % path
        self.cloud.mkdir(path)

    def remove(self, path):
        print 'removing file %s ...' % path[:-1]
        self.cloud.delete(path)
    
    def get_file_info(self, path):
        return self.cloud.getinfo(path)
    
    def get_file_list(self, path, flag=True):
        if flag:
            self.filelist = self.cloud.getlist(path)
            self.file_name_cache = []
            for files in self.filelist:
                self.file_name_cache.append(files['name'])

            return self.filelist
        else:
            return self.cloud.getlist(path)

    def clear_file_list_cache(self):
        self.filelist = ''

    def get_usage_info(self):
        return self.cloud.usage()
    
    def swith_workspace(self, path):
        if path.startswith('/') and path.endswith('/'):
            dir_info = self.cloud.getinfo(path)
            if dir_info['file-type'] != 'folder':
                import color 
                print color.render_color('Error: ','error') + path[:-1]+' is not a directory !'
                return
        else:
            print 'The directory path is not absolute path.'
            return 

        self.WORKSPACE = path
        # 在每次切换工作目录后，就对当前目录下的文件建立缓存。
        # 不用每次都要联网获取当前目录下的文件信息，提高性能。
        self.get_file_list(path)

    def get_current_workspace(self):
        return self.WORKSPACE

    def print_connect_info(self):
        
        info = '==============================\n' + \
               '+ Bucketname: %s\n' + \
               '+ Username: %s  \n' + \
               '+ Timeout:  %s  \n' + \
               '+ EndPoint: %s  \n' + \
               '+ Workspace: %s \n' + \
               '=============================='
        
        print info % (self.BUCKETNAME, self.USERNAME, self.TIMEOUT, self.ENDPOINT, self.WORKSPACE)

         
if __name__ == '__main__':
    pass 
