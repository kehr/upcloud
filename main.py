#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    main.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Thu 17 Apr 2014 06:07:02 PM CST
# @Copyright:    GPL 2.0 applies
# @Description:                     
#########################################################################
import sys
import upyun
import argparse
from cli import CLI
from upcloud import upcloud

class cmd_parser():
    
    def __init__(self):
        self.parse_args()

    def parse_args(self):
        self.parser = argparse.ArgumentParser(prog='upcloud',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                description="upyun remote management of client !")
        self.parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
        self.parser.add_argument('-b', '--bucket', required=True, type=str,
            help='your space\'s name')
        self.parser.add_argument('-u', '--username', required=True, type=str, 
            help='your operator\'s name of this space')
        self.parser.add_argument('-p', '--passwd', required=True, type=str,
            help='your operator\'s password')
        self.parser.add_argument('-t', '--timeout',default=30, type=int,
            help='the HTTP request timeout time')
        self.parser.add_argument('-e', '--endpoint',default='auto',choices=["auto","telecom","cnc","ctt"],
            help='your network access point')
        self.args = self.parser.parse_args()

    def handle_args(self):
        if self.args.bucket is not None and self.args.username is not None and self.args.endpoint is not None:
            bucket   = self.args.bucket
            username = self.args.username
            passwd   = self.args.passwd
            timeout = self.args.timeout
            endpoint = self.handle_endpoint(self.args.endpoint)
        else:
            print '\n you should specify the "bucket, username, passwd" at the same time !'
            print ' try "-h" or "--help" for help\n'
            sys.exit(1)
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
        prompt = self.args.username+'@'+self.args.bucket+' $ ' 
        try:
            cli = CLI(prompt, bucket, username, passwd, timeout, endpoint)
            cli.cmdloop()
        except KeyboardInterrupt:
            cli.do_exit('exit')
        #except SystemExit: # 这里居然抓不到cli的SystemExit，我很郁闷:-(。放在这里抓argparse的推出也不合理。
        #    pass
        except upyun.UpYunServiceException as e:
            print "HTTP Status: " + str(e.status)
            print "Server error: " + e.msg + "\n"
            sys.exit(1)
        except upyun.UpYunClientException as ce:
            print "Client error: " + ce.msg + "\n"
            sys.exit(1)

def main():
    cmd = cmd_parser()
    cmd.handle_args()

if __name__ == '__main__':
    main()
