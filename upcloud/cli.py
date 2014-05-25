#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    cli.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Thu 24 Apr 2014 05:08:30 PM CST
# @Copyright:    MIT applies
# @Description:  Interact with the bucket of UpYun                  
#########################################################################
import os 
import cmd
import sys
import color 
import upyun
import manual 
import getpass
import argparse
import readline
import subprocess
from upcloud import upcloud
from datetime import datetime

class CLI(cmd.Cmd):

    def __init__(self, prompt='>>> ',bucket=None, username=None, passwd=None, timeout=60, endpoint=upyun.ED_AUTO):
        cmd.Cmd.__init__(self)
        self.intro = manual.get_tips()
        self.doc_header=color.render_color('All commands you can use (type help <command> get more info):')
        self.undoc_header=color.render_color('All alias command:')
        self.prompt = color.render_color(prompt,'blue')
        self.init_upcloud(bucket, username, passwd, timeout, endpoint)
        self.current_local_workspace = os.path.abspath('.')

    # do_command methods ...
    def do_man(self,args):
        '''Show the detail message of command.'''
        try:
            self.cmdline('man', args)
        except SystemExit:
            pass
    
    def do_ll(self, args):
        try:
            self.do_ls('-l '+args)
        except SystemExit:
            print 'Type "ls -h" for help.'
    def do_ls(self, args):
        try:
            self.cmdline('ls', args)
        except SystemExit:
            print 'Type "ls -h" for help.'

    def do_put(self, args):
        try:
            current_local_path = os.path.abspath('.')
            self.cmdline('put', args)
        except SystemExit:
            print 'Type "put -h" for help.'
        except OSError as e:
            print color.render_color('Error: ','error') , e
        finally:
            # 最后要回到程序的初始工作目录
            os.chdir(current_local_path)
            # refresh the cache of current workspace
            self.cloud.get_file_list(self.cloud.get_current_workspace())

    def do_get(self, args):
        try:
            current_upyun_workspace = self.cloud.get_current_workspace()
            self.cmdline('get', args)
        except SystemExit:
            print 'Type "get -h" for help.'
        except OSError as e:
            print color.render_color('Error: ','error') , e
        finally:
            self.cloud.swith_workspace(current_upyun_workspace)

    def do_cd(self, args):
        try:
            self.cmdline('cd', args)
        except SystemExit:
            print 'Type "cd -h" for help.'
        except upyun.UpYunServiceException as e:
            print "Error: " + e.msg + "!"
            self.show_error(error='Server error', msg=e.msg)

        
    def do_pwd(self, args):
        if args.split():
            manual.get_manual('pwd', args.split())
        else:
            print self.cloud.get_current_workspace() + '\n'

    def do_mkdir(self, args):
        try:
            self.cmdline('mkdir', args)
        except SystemExit:
            print 'Type "mkdir -h" for help.'

    def do_cat(self, args):
        try:
            self.cmdline('cat', args)
        except SystemExit:
            print 'Type "cat -h" for help.'

    def do_rm(self, args):
        try:
            self.cmdline('rm', args)
        except SystemExit:
            print 'Type "rm -h" for help.'

    def do_usage(self, args='none'):
        if args == 'none':
            return self.readable(self.cloud.get_usage_info())
        elif not args:
            print 'Your space has been used: '+self.readable(self.cloud.get_usage_info())
        else:
            manual.get_manual('usage','-h')

    def do_exit(self, args):
        if args:
            manual.get_manual('exit', args.split())
        else:
            print '\nEnjoy your day. Bye !'
            sys.exit(0)
    
    def do_bash(self, args='bash'):
        '''run a bash shell environment'''
        subprocess.call(os.getenv('SHELL'))

    def do_shell(self, args):
        """Run shell command. command begain with '!'. \n"""
        command = args.split()
        
        # handle the empty line
        if not command: return 

        if command[0] == 'cd':
            try:
                if len(command) == 1:
                    os.chdir(self.current_local_workspace)
                else:
                    os.chdir(os.path.abspath(command[1]))
                print  os.path.abspath('.')
            except OSError as e:
                print color.render_color('Error: ','error') , e
        else:
            shell_cmd = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
            print shell_cmd.communicate()[0]
    
    def do_clear(self, args):
        if args.split():
            manual.get_manual('clear',args.split())
        else:
            shell_cmd = subprocess.Popen('clear', shell=True, stdout=subprocess.PIPE)
            print shell_cmd.communicate()[0]
    
    def action_man(self, args):
        if args.command == 'welcome':
            print manual.get_tips()
        else:
            manual.get_manual(args.command, '-h')

    def action_ls(self, args):
        if type(args.path) is str:
            path_list = [args.path]
        else:
            path_list = args.path
        # refresh the cache of current workspace
        if args.refresh:
            self.cloud.get_file_list(self.cloud.get_current_workspace())

        if '*' in path_list:
            path_list = self.show_file_list(None,self.cloud.get_current_workspace())

        for path in path_list:
            path = self.abspath(path)
            
            if args.directory:
                if args.long:
                    self.show_file_info(True, path)
                else:
                    self.show_file_info(False, path)
            else:
                if args.long:
                    if self.check(path) == 'folder':
                        print color.render_color(path,'path')+':'
                        self.show_file_list(True, path)
                    else:
                        self.show_file_info(True, path)
                else:
                    if self.check(path) == 'folder':
                        print color.render_color(path,'path')+':'
                        self.show_file_list(False, path)
                    else:
                        self.show_file_info(False, path)
            
           # if len(path_list) > 1: print ''

    def show_file_info(self, flag=False, filepath='/'):
        filepath = self.abspath(filepath)
        info = self.cloud.get_file_info(filepath)
        color_format = '%s  '+color.render_color('%-6s','purple')+'  %9s  '+color.render_color('%-s','blue')
        normal_format = '%s  '+color.render_color('%-6s','green')+'  %9s  '+color.render_color('%-s','yellow')
        
        info_type = info['file-type']
        info_name = ''.join(filepath.split('/')[-2:])
        info_format = normal_format
        if filepath == '/':
            info_time = 'None'
            info_name = '/'
        else:
            info_time = datetime.fromtimestamp(int(info['file-date']))
        if info['file-type'] == 'folder':
            info_type = '<dir>'
            info_format = color_format
            info_size = ''
        else:
            info_type = '<file>'
            info_size =  self.readable(info['file-size'])
        if flag:
            print info_format % (info_time, info_type, info_size, info_name)
        else:
            print info_format[-14:] % (info_name)

    def show_file_list(self, flag=False, path='/'):
        '''when flag is True or Flase,print long info or short info.
           when flag is None, return a name list of current workspace.
        '''
        if self.cloud.get_current_workspace() == path:
            info_list = self.cloud.filelist
        else:
            info_list = self.cloud.get_file_list(path,False)
        dir_num  = 0
        file_num = 0
        name_list = []
        names = []
        color_format = '%s  '+color.render_color('%-6s','purple')+'  %9s  '+color.render_color('%-s','blue')
        normal_format = '%s  '+color.render_color('%-6s','green')+'  %9s  '+color.render_color('%-s','yellow')
        
        for info in info_list:
            info_time = datetime.fromtimestamp(int(info['time']))
            info_type = info['type']
            info_size =  self.readable(info['size'])
            info_name = info['name']
            info_format = normal_format

            if info['type'] == 'F':
                info_type = '<dir>'
                dir_num += 1
                info_format = color_format
                info_size = ''
            else:
                info_type = '<file>'
                file_num += 1
                
            if flag:
                print info_format % (info_time, info_type, info_size, info_name)
            
            names.append(info_name)
            name_list.append({info_name:info_type})

        name_list.sort()
        name_dir_format = color.render_color('%-s', 'blue')
        name_file_format = color.render_color('%-s', 'yellow')

        if not flag: 
            for name in name_list:
                file_name,file_type = name.popitem()
                name_format = name_dir_format if file_type == '<dir>' else name_file_format
                if flag != None:
                    print name_format % file_name,
            print ''
        count_format = color.render_color('\n%d directories', 'purple') + ',' + color.render_color(' %d files', 'green')
        print count_format % (dir_num, file_num)
        
        return names

    def action_put(self, args):
        source_list = []
        destination = self.abspath(args.destination)
        # 预先处理路径，解决使用 . 或 .. 时多返回一级目录的问题。
        for path in args.source:
            if path == '*':
                path = '.'
            source_list.append(os.path.abspath(path))
        level = args.level
        print 'level:',level
        self.put_files_count = 0
        self.put_dirs_count = 0
        self.put_local_files(source_list, destination, level)
        put_count_format = color.render_color('%s directories, ','purple') + color.render_color('%s files','green')

        if self.put_files_count == 0:
            print 'The upload folder is empty. Did not upload any file !'
            return 
        print 'All files uploaded successfully! \n' + \
                'count: '+put_count_format % (self.put_dirs_count, self.put_files_count)

    def put_local_files(self, source_list=[], destination='/', level=0):
        
        des_pre = destination 
         
        for source_path in source_list:
            # 递归获取的文件列表是相对路径，这里需要再一次处理
            path = os.path.abspath(source_path) 
            if not os.path.exists(path):
                print color.render_color(path+':','error')+'file not exits !'
            else:
                if os.path.isdir(path):
                    print  color.render_color(path, 'blue')+':'
                    self.put_dirs_count += 1
                    # enter sub dir 
                    os.chdir(path)
                    file_list = os.listdir(path)
                    self.put_local_files(file_list, des_pre, level)
                    # return to parent dir (necessary!)
                    os.chdir('..')
                else:
                    print color.render_color('from: ','purple') + path
                    path_list = path.split('/')
                    path_list.pop(0) # remove the begain space
                    if level >= len(path_list):
                        level = len(path_list) - 1
                    destination = des_pre + '/'.join(path_list[level:]) 
                    print color.render_color('to:   ','green') + destination 
                    self.cloud.upload(path,destination)
                    self.put_files_count += 1
 
    def action_get(self, args):
        source_list = args.source 
        destination = os.path.abspath(args.destination)
        if not os.path.exists(destination):
            print color.render_color('Error: ','error') + 'The local folder does not exist !'
            flag = raw_input('Do you want to create it now?(y/n):')
            if flag == 'y':
                os.makedirs(destination)
            else:
                return 
        level = args.level
        print 'level:',level
        self.get_files_count = 0
        self.get_dirs_count = 0
        self.get_upyun_files(source_list, destination, level)
        if self.get_files_count == 0:
            print 'The download folder is empty. Did not download any file !'
            return 
        get_count_format = color.render_color('%s directories, ','purple') + color.render_color('%s files','green')
        print 'All files download successfully! \n' + \
                'count: '+get_count_format % (self.get_dirs_count, self.get_files_count)
    
    def get_upyun_files(self, source_list=[], destination='/tmp/', level=0):
        if not destination.endswith('/'):
            des_pre = destination + '/'
        else:
            des_pre = destination 
         
        for source_path in source_list:
            path = self.abspath(source_path) 
            check_file = self.check(path)
            if not check_file:
                print color.render_color(path+':','error')+'file not exits !'
            else:
                if check_file == 'folder':
                    print  color.render_color(path, 'blue')+':'
                    self.get_dirs_count += 1
                    # enter sub dir 
                    self.cloud.swith_workspace(path)
                    file_list = self.show_file_list(True,path)
                    self.get_upyun_files(file_list, des_pre, level)
                    # return to parent dir (necessary!)
                    self.cloud.swith_workspace(self.abspath('..'))
                else:
                    path = path[:-1] #去掉末尾的'/'
                    print color.render_color('from: ','purple') + path
                    path_list = path.split('/')
                    path_list.pop(0) # remove the begain space
                    if level >= len(path_list):
                        level = len(path_list) - 1
                    destination = des_pre + '/'.join(path_list[level:]) 
                    print color.render_color('to:   ','green') + destination 
                    self.cloud.download(path, destination)
                    self.get_files_count += 1

    def action_cd(self, parser, args):
        if args.help:
            parser.print_help()
        if not args.path:
            return
        workspace = self.abspath(args.path)
        self.cloud.swith_workspace(workspace)
        print self.cloud.get_current_workspace() + '\n'

    def action_mkdir(self, args):
        for directory in args.path:
            directory = self.abspath(directory)
            if args.parents:
                print 'recursive create the directory: %s' % directory
                dir_list = directory.split('/')[1:-1]
                # 先检查第一级目录
                parent_dir = self.abspath(dir_list[0])
                file_type = self.check(parent_dir)
                if not file_type:
                    self.cloud.mkdir(parent_dir)
                # 如果目录只有一级直接返回
                if len(dir_list) == 1: continue

                for dir_name in dir_list[1:]:
                    parent_dir += dir_name + '/'
                    file_type = self.check(parent_dir)
                    if not file_type:  #文件不存在
                        self.cloud.mkdir(parent_dir)
            else:
                self.cloud.mkdir(directory)
        else:
            print 'All the files to create success!'
            # refresh current workspace cache 
            self.cloud.get_file_list(self.cloud.get_current_workspace()) 
    
    def check(self, path):
        '''check the file exits.if the file exits,returns the file type else returns False'''
     
        if path == self.cloud.get_current_workspace():
            return 'folder'
        for fileinfo in self.cloud.filelist:
            if path == self.abspath(fileinfo['name']):
                if fileinfo['type'] == 'F':
                    return 'folder'
                else:
                    return 'file'
        info = {}
        try:
            info = self.cloud.get_file_info(path)
        except upyun.UpYunServiceException as e:
            pass
        if not info:
            return False
        return info['file-type']

    def action_cat(self, args):
        file_path = self.abspath(args.file)
        file_type = self.check(file_path)
        if file_type and file_type == 'folder':
            print self.show_error(file_path+' is directory !')
            return
        else:
            local_file = self.cloud.cat(file_path[:-1])
            if not local_file:
                print local_file
                print self.show_error('File not exists !')
                return
            
            print ''
            if  args.tail:
                command = 'tail -n '+str(args.tail)+' '+local_file + ' | cat -n'
                self.do_shell(command)
                return 
            if  args.number:
                command = 'head -n '+str(args.number)+' '+local_file+' | cat -n' 
            else:
                command = 'cat '+local_file + ' | cat -n'
            self.do_shell(command)

    def action_rm(self, args):
        for directory in args.path:
            directory = self.abspath(directory)
            if args.recursive:
                print 'Recursive delete the directory: %s' % directory
                self.recursive_rm(directory)
                self.cloud.remove(directory)
            else:
                self.cloud.remove(directory)
        else:
            print 'All files deleted successfully!'
            # refresh current workspace cache 
            try:
                self.cloud.get_file_list(self.cloud.get_current_workspace()) 
            except upyun.UpYunServiceException as e:
                self.cloud.clear_file_list_cache()
                print 'The current working directory is failure！'

    def recursive_rm(self,path):
        file_type = self.check(path)
        if not file_type:
            msg = 'file not exits !'
            self.show_error(msg)
            return
        else:
            print '+'*50
            print color.render_color(path,'path')+': '
            file_list = self.show_file_list(True,path)
            for file_name in file_list:
                print 'removing '+color.render_color(path,'blue') +': '
                sub_path = path + file_name+'/'
                if self.check(sub_path) == 'folder':
                    self.recursive_rm(sub_path)
                    self.cloud.remove(sub_path)
                else:
                    self.cloud.remove(sub_path)
            else:
                print 'sucess!'

    #Auto completion setting
    def complete_ls(self, text, line, begidx, endidx):
        return [name for name in self.cloud.file_name_cache if name.startswith(text)]
    
    def complete_man(self, text, line, begidx, endidx):
        commands =  ['put','get','mkdir','cd','ls','rm','pwd','clear','cat','usage','exit','quit','help']
        return [name for name in commands if name.startswith(text)]

    # help_command methods ...
    def help_ls(self):
        manual.ls()

    def help_put(self):
        manual.put()

    def help_get(self):
        manual.get()

    def help_cd(self):
        manual.cd()

    def help_pwd(self):
        manual.pwd()

    def help_mkdir(self):
        manual.mkdir()

    def help_cat(self):
        manual.cat()

    def help_rm(self):
        manual.rm()

    def help_usage(self):
        manual.usage()

    def help_exit(self):
        manual.exist()

    def help_quit(self):
        manual.quit()

    def help_help(self):
        pass 

    def help_clear(self):
        manual.clear()


    # overrid some methods ...

    # overrid this method. It will do nothing, when you input a empty line.
    def emptyline(self):
        pass

    def default(self, command):
        if command == 'EOF':
           # self.do_exit('')
           flag = raw_input('\nDo you really want to exit?(y/n):')
           if flag == 'y':
               sys.exit(0)
        else:
            self.command_not_found(command)

    # some extend methods ...
    def init_upcloud(self, bucket, username, passwd, timeout, endpoint):
        self.cloud = upcloud(bucket, username, passwd, timeout, endpoint)
        print ' login ...\n'
        try:
            print '+ Space usage: %s' % self.do_usage()
            # build cache for '/'
            self.cloud.get_file_list(self.cloud.get_current_workspace())
        except upyun.UpYunServiceException as e:
           # print "HTTP Status: " + str(e.status)
            self.show_error(error='Server error',msg=e.msg)
            print 'login failed ! please check your login information.'
            sys.exit(1)
        except upyun.UpYunClientException as e:
            self.show_error(error='Client error',msg=e.msg)
            sys.exit(1)
        except KeyboardInterrupt:
            print '\nNetwork is busy, please try again later !\n'
            sys.exit(1)
        print '\n login sucess ! Have a nice day !'

    def cmdline(self, command, args):
        if type(args) is str:
            args = args.split()
        else:
            msg = 'args require a string type !'
            self.show_error(msg)
            return
        try:
            if command == 'man':
                parser = argparse.ArgumentParser(prog='man', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('command', nargs='?', default='welcome',
                        help='The command that you want to konw')
                args_list = parser.parse_args(args)
                self.action_man(args_list)
            elif command == 'ls':
                parser = argparse.ArgumentParser(prog='ls', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('path', nargs='*', default=self.cloud.get_current_workspace(),
                        help='the directory path that you want to see') 
                parser.add_argument('-l', '--long', action='store_true',
                        help='use a long listing format')
                parser.add_argument('-d', '--directory',action='store_true', 
                        help='list directory entries instead of contents')
                parser.add_argument('-r', '--refresh',action='store_true', 
                        help='refresh the file list of current workspace')
                args_list = parser.parse_args(args)
                self.action_ls(args_list)
            elif command == 'put':
                parser = argparse.ArgumentParser(prog='put', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('-s', '--source', nargs='+', required='True',
                        help='The file path of your local system')
                parser.add_argument('-d', '--destination', default='/', 
                        help='The file path of your bucket<UpYun space>')
                parser.add_argument('-l', '--level', type=int, default=0 ,
                        help='remove The file path level(Support negative number), ' + \
                             'begain with local path "/". save the name of files by dafaut')
                args_list = parser.parse_args(args)
                self.action_put(args_list)
            elif command == 'get':
                parser = argparse.ArgumentParser(prog='get', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('-s', '--source', nargs='+', required='True',
                        help='The file path of your bucket<UpYun space>')
                parser.add_argument('-d', '--destination', default='.',
                        help='The file path of your local system')
                parser.add_argument('-l', '--level', type=int, default=0 ,
                        help='Remove The file path level(Support negative number),' + \
                             'begain with bucket path "/". save the name of files by dafaut')
                args_list = parser.parse_args(args)
                self.action_get(args_list)
            elif command == 'cd':
                parser = argparse.ArgumentParser(prog='cd', add_help=False,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                        epilog='Type "man cd" get more info.')
                group = parser.add_mutually_exclusive_group()
                group.add_argument('-h', '--help', action='store_true', 
                        help='show this message and return.')
                group.add_argument('path', nargs='?', default='/',
                        help='Your destination workspace')
                arg_dict = parser.parse_args(args)
                # 由于当参数出错时argparse会报错且退出程序，显然我并不需要在这里退出
                # 解决：http://srackoverflow.com/questions/5943249
                #try:
                #    arg_dict = parser.parse_args(args)
                #except SystemExit:
                #    print 'sucess'
                self.action_cd(parser, arg_dict)
            elif command == 'mkdir':
                parser = argparse.ArgumentParser(prog='mkdir', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('-p', '--parents', action='store_true',
                        help='make parent directories as needed')
                parser.add_argument('path', nargs='+', help='Create one or more directories')
                args_list = parser.parse_args(args)
                self.action_mkdir(args_list)
            elif command == 'cat':
                parser = argparse.ArgumentParser(prog='cat', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('file',  metavar='FILE', help='The file path that you want to see')
                group = parser.add_mutually_exclusive_group()
                group.add_argument('-n', '--number', type=int, help='Get first N rows content file')
                group.add_argument('-t', '--tail', type=int,  help='N lines after access to files')
                args_list = parser.parse_args(args)
                self.action_cat(args_list)
            elif command == 'rm' :
                parser = argparse.ArgumentParser(prog='rm', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('-r', '--recursive', action='store_true', 
                        help='remove directories and their contents recursively')
               # parser.add_argument('-f', '--force', action='store_true',
               #         help='ignore nonexistent files, never prompt')
                parser.add_argument('path', nargs='+', help='remove one or more files or directories')
                args_list = parser.parse_args(args)
                self.action_rm(args_list)
            else:
                self.command_not_found(command)
        except upyun.UpYunServiceException as e:
            self.show_error(error='Server error', msg=e.msg)
        except upyun.UpYunClientException as e:
            self.show_error(error='Client error', msg=e.msg)

    def abspath(self, path, sys=False):
        workspace = self.cloud.get_current_workspace()
        # format workspace
        if not workspace.endswith('/'):
            workspace += '/'
        if path == '*' or path == '.':
            return workspace
        elif path == '..':
            if workspace != '/':
                path_list = workspace.split('/')
                workspace = '/'.join(path_list[:-2]) + '/'
        elif path.startswith('../'):
            path_list = path.split('/')
            if path_list[1] == '..':
                return workspace
            workspace = '/'.join(workspace.split('/')[:-2]) + '/'+'/'.join(path_list[1:])
        elif path.startswith('./'):
            path_list = path.split('/')
            if path_list[1] == '.':
                return
            workspace += '/'.join(path.split('/')[1:])
        elif not path.startswith('/'):
            workspace += path
        else:
            workspace = path
        if not  workspace.endswith('/'):
            workspace += '/'
        return workspace

    def  readable(self, usage):
        '''format usage to human readable'''
        # 又拍云SDK BUG，如果连接cmcc，请求回来的是认证页面
        if '<html>' in usage:
            raise upyun.UpYunClientException('Unable to connect to the network!')
        usage = int(usage)
        if usage == 0: return '0B'
        level = [1.0 * 1024 ** n for n in xrange(6)]
        unit  = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        while usage >= level[i]:
            i += 1
        return '%.2f%s' % (usage/level[i-1], unit[i-1])

    def command_not_found(self, command):
        msg = 'command not found ! %s' % command 
        self.show_error(msg)
        print 'Type "?" or "help" or press double <Tab> key to get a command list'

    def show_error(self, msg=None,  error='Error'):
        print color.render_color(error+': ','error')+msg

    # define the same action ...
    do_q    = do_exit
    do_cls  = do_clear
    do_quit = do_exit
    complete_ll  = complete_ls
    complete_cat = complete_ls
    complete_cd  = complete_ls
    complete_put = complete_ls
    complete_get = complete_ls
    complete_rm  = complete_ls

def main():
    cli = CLI(username='test01',passwd='testtest',bucket='kehrspace',timeout=60,endpoint=upyun.ED_AUTO)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print color.render_color('\nWarning: operation was interrupted by user !')
        main()
    except SystemExit:
        pass 

if __name__ == '__main__':
    main()
