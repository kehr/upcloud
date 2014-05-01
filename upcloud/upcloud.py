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

import upyun

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

        print "Uploading file ..."
       # headers = {"x-gmkerl-rotate": "180"}
        with open(src, 'rb') as f:
            res = self.cloud.put(des, f, checksum=False)
    
    def download(self):
        print 'download files ...'

    def create_dir(self, path):
        print 'creating directory %s ...' % path
        self.cloud.mkdir(path)

    def remove_files(self, path):
        print 'removing file %s ...' % path[:-1]
        self.cloud.delete(path)
    
    
    def check_file(self,path):
        '''if file not exit return None,else return file type.'''
        if path == '/':
            return 'folder'

        name = ''
        if path.endswith('/'):
            name = ''.join(path.split('/')[-2:-1])
        else:
            name = ''.join(path.split('/')[-1:])
        
        
        for info in self.filelist:
            if info['name'] == name:
                if info['type'] == 'F':
                    return 'folder'
                else:
                    return 'file'
                break
        else:
            return None

    def get_file_info(self, path):
        return self.cloud.getinfo(path)
    
    def get_file_list(self, path, flag=True):
        if flag:
            self.filelist = self.cloud.getlist(path)
            return self.filelist
        else:
            return self.cloud.getlist(path)

    def clear_file_list_cache(self):
        self.filelist = ''

    def get_usage_info(self):
        return self.cloud.usage()
    
    def get_abspath(self, path):
        if path.startswith('/'):
            return path
        else:
            if self.WORKSPACE.endswith('/'):
                return self.WORKSPACE + path
            else:
                return self.WORKSPACE + '/' + path

    def swith_workspace(self, path):
        if path.startswith('/') and path.endswith('/'):
            dir_info = self.cloud.getinfo(path)
            if dir_info['file-type'] != 'folder':
                print path+' is not a directory !'
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

    def help(self):
        user_help = '----------------------------------------------\n' + \
                    ''
        pass
         
if __name__ == '__main__':
    up = upcloud('kehrspace','kehr','kehr4444')
 #   up.connect_upyun()
  #  up.upload_files('/home/kehr/Github/upcloud/test/img/unix.png')
   # print up.get_usage_info()
    print up.get_file_info('/a/b/c/d/')
    print up.get_file_info('/a/')
