#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    cloud.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Wed 16 Apr 2014 08:03:45 PM CST
# @Copyright:    GPL 2.0 applies
# @Description:                     
#########################################################################
# 检查参数是否正常，为空抛出异常
# 

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
        
        self.print_connect_info()

    def connect_upyun(self):
        
        self.cloud = upyun.UpYun(self.BUCKETNAME, 
                                 self.USERNAME, 
                                 self.PASSWORD, 
                                 self.TIMEOUT, 
                                 self.ENDPOINT)
        return self.cloud
        


    def upload_files(self, src, des='/'):

        print "Uploading a new object to UpYun from a file ..."
       # headers = {"x-gmkerl-rotate": "180"}
        with open(src, 'rb') as f:
            res = self.cloud.put(des+'imgs/Linux.png', f, checksum=False)
        print "Uploaded"
    
    def download_files(self):
        print 'download files ...'

    def create_dir(self):
        print 'create dir ... '

    def remove_files(self):
        print 'remove files ...'

    def get_filelist(self):
        print 'show file list ...'
    
    def get_file_info(self):
        print 'show file\'s info ...'

    def get_usage_info(self):
        print 'show space usage info ...'
    
    def check_connect_info(self):
        pass
    
    def swith_workspace(self, path):
        
        self.get_current_workspace()

    def get_current_workspace(self):
        print self.WORKSPACE

    def print_connect_info(self):
        
        info = '==============================\n' + \
               '+ Bucketname: %s\n' + \
               '+ Username: %s  \n' + \
               '+ Password: %s  \n' + \
               '+ Timeout:  %s  \n' + \
               '+ EndPoint: %s  \n' + \
               '+ Current Workspace: %s  \n' + \
               '==============================\n'
        
        print info % (self.BUCKETNAME, self.USERNAME, self.PASSWORD, self.TIMEOUT, self.ENDPOINT, self.WORKSPACE)

    def help(self):
        user_help = '----------------------------------------------\n' + \
                    ''
        pass
         
if __name__ == '__main__':
    up = upcloud('kehrspace','kehr','kehr4444')
    up.connect_upyun()
    up.upload_files('/home/kehr/Github/upcloud/test/img/unix.png')
