#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    main.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Thu 17 Apr 2014 06:07:02 PM CST
# @Copyright:    MIT applies
# @Description:  Interact with the bash shell                 
#########################################################################
import sys
import color 
import upyun
import argparse
from cli import CLI
from upcloud import upcloud
from __init__ import __version__ as version

__version__ = version 

class cmd_parser():
  
    def __init__(self):
        self.parse_args()
        self.handle_args() 
        
    def parse_args(self):
        client_name = color.render_color('upcloud','red')
        client_des = color.render_color(' Remote terminal management client for UpYun !', 'yellow')
        self.parser = argparse.ArgumentParser(prog=client_name,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                description=client_des)
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
        self.parser.add_argument('-b', '--bucket', required=True, type=str,
            help='The name of your bucket')
        self.parser.add_argument('-u', '--username', required=True, type=str, 
            help='The operator\'s name of this bucket')
        self.parser.add_argument('-p', '--passwd', required=True, type=str,
            help='The operator\'s password of this bucket')
        self.parser.add_argument('-t', '--timeout',default=30, type=int,
            help='The HTTP request timeout time')
        self.parser.add_argument('-e', '--endpoint',default='auto',choices=["auto","telecom","cnc","ctt"],
            help='The network access point')
        self.args = self.parser.parse_args()
      
    def handle_args(self):
        bucket   = self.args.bucket
        username = self.args.username
        passwd   = self.args.passwd
        timeout = self.args.timeout
        endpoint = self.handle_endpoint(self.args.endpoint)
        self.handle_jobs(bucket, username, passwd, timeout, endpoint)
        
    def handle_endpoint(self, endpoint):
        if endpoint == 'auto':
            return upyun.ED_AUTO
        elif endpoint == 'telecom':
            return upyun.ED_TELECOM
        elif endpoint == 'cnc':
            return upyun.ED_CNC
        elif endpoint == 'ctt':
            return upyun.ED_CTT
        return upyun.ED_AUTO
          
    def handle_jobs(self, bucket, username, passwd, timeout=30, endpoint=upyun.ED_AUTO):
        prompt = self.args.username+'@'+self.args.bucket+' > ' 
        try:
            cli = CLI(prompt, bucket, username, passwd, timeout, endpoint)
            cli.cmdloop()
        except KeyboardInterrupt:
            cli.do_exit('exit')
        except upyun.UpYunServiceException as e:
            print color.render_color('Server error:','error'),e.msg
            sys.exit(1)
        except upyun.UpYunClientException as e:
            print color.render_color('Client error:','error'),e.msg
            sys.exit(1)


def main():
    cmd_parser()
 
if __name__ == '__main__':
    main()
