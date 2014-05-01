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
import socket
import getpass
import argparse
import readline
import subprocess
from upcloud import upcloud
from datetime import datetime
from __init__ import __version__ as version

__version__ = version 

class CLI(cmd.Cmd):

    def __init__(self, prompt='>>> ',bucket=None, username=None, passwd=None, timeout=30, endpoint=upyun.ED_AUTO):
        cmd.Cmd.__init__(self)
        self.intro = self.get_help_message()
        self.doc_header=color.render_color('All commands you can use (type help <command> get more info):')
        self.undoc_header=color.render_color('All alias command:')
        self.prompt = color.render_color(prompt,'blue')
        self.init_upcloud(bucket, username, passwd, timeout, endpoint)


    # do_command methods ...
    def do_man(self,args):
        '''Show the detail message of command.'''
        try:
            self.parse_cmdline('man', args)
        except SystemExit:
            pass
    
    def do_ll(self, args):
        try:
            self.do_ls('-l '+args)
        except SystemExit:
            print 'Type "ls -h" for help.'
    def do_ls(self, args):
        try:
            self.parse_cmdline('ls', args)
        except SystemExit:
            print 'Type "ls -h" for help.'

    def do_put(self, args):
        try:
            current_local_path = os.path.abspath('.')
            self.parse_cmdline('put', args)
        except SystemExit:
            print 'Type "put -h" for help.'
        except OSError as e:
            print color.render_color('Error: ','error') , e
        finally:
            # 最后要回到程序的初始工作目录
            os.chdir(current_local_path)

    def do_get(self, args):
        try:
            self.parse_cmdline('get', args)
        except SystemExit:
            print 'Type "get -h" for help.'

    def do_cd(self, args):
        try:
            self.parse_cmdline('cd', args)
        except SystemExit:
            print 'Type "cd -h" for help.'
        except upyun.UpYunServiceException as e:
            print "Error: " + e.msg + "!"
            self.show_error(error='Server error', msg=e.msg)

        
    def do_pwd(self, args):
        if args.split():
            self.show_help('pwd', args.split())
        else:
            print self.cloud.get_current_workspace() + '\n'

    def do_mkdir(self, args):
        try:
            self.parse_cmdline('mkdir', args)
        except SystemExit:
            print 'Type "mkdir -h" for help.'

    def do_cat(self, args):
        try:
            self.parse_cmdline('cat', args)
        except SystemExit:
            print 'Type "cat -h" for help.'

    def do_rm(self, args):
        try:
            self.parse_cmdline('rm', args)
        except SystemExit:
            print 'Type "rm -h" for help.'

    def do_usage(self, args='none'):
        if args == 'none':
            return self.human_readable(self.cloud.get_usage_info())
        elif not args:
            print 'Your space has been used: '+self.human_readable(self.cloud.get_usage_info())
        else:
            self.show_help('usage','-h')

    def do_exit(self, args):
        if args:
            self.show_help('exit', args.split())
        else:
            print '\nEnjoy your day. Bye !'
            sys.exit(0)
    
    def do_bash(self, args='bash'):
        '''run a bash shell environment'''
        print ''
        prompt = getpass.getuser()+'@'+socket.gethostname() + ' > '
        prompt = color.render_color(prompt,'green')
        while True:
            command = raw_input(prompt)
            if command:
                if command == 'exit': 
                    break
                self.do_shell(command)

    def do_shell(self, args):
        """Run shell command. command begain with '!'. \n"""
        if args.split()[0] == 'cd':
            try:
                os.chdir(args.split()[1])
                print 'local  workspace changed !\n', os.path.abspath('.')
            except OSError as e:
                print color.render_color('Error: ','error') , e

        shell_cmd = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
        print shell_cmd.communicate()[0]
    
    def do_clear(self, args):
        if args.split():
            self.show_help('clear',args.split())
        else:
            shell_cmd = subprocess.Popen('clear', shell=True, stdout=subprocess.PIPE)
            print shell_cmd.communicate()[0]
    
    def action_man(self, args):
        if args.command == 'welcome':
            print self.get_help_message()
        else:
            self.show_help(args.command, '-h')

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
            path = self.get_path(path)
            print color.render_color(path,'path')+':'

            if args.directory:
                if args.list:
                    self.show_file_list(True, path)
                else:
                    self.show_file_list(path)
            else:
                if args.list:
                    self.show_file_list(True, path)
                else:
                    self.show_file_list(path)
            
            if len(path_list) > 1: print ''

    
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
            info_size =  self.human_readable(info['size'])
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
        name_dir_format = color.render_color('%s  ', 'blue')
        name_file_format = color.render_color('%s  ', 'yellow')

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
        # 预先处理路径，解决使用 . 或 .. 时多返回一级目录的问题。
        for path in args.source:
            source_list.append(os.path.abspath(path))
            
        destnation = args.destnation
        self.put_files_count = 0
        self.put_dirs_count = 0
        self.get_local_files(source_list)
        put_count_format = color.render_color('%s directories, ','purple') + color.render_color('%s files','green')
        print put_count_format % (self.put_dirs_count, self.put_files_count)

    def get_local_files(self, source_list=[]):
        for source_path in source_list:
            # 递归获取的文件列表是相对路径，这里需要再一次处理
            path = os.path.abspath(source_path) 
            if not os.path.exists(path):
                print color.render_color(path+':','error')+'file not exits !'
                pass
            else:
                if os.path.isdir(path):
                    print  color.render_color(path, 'blue')+':'
                    self.put_dirs_count += 1
                    # enter sub dir 
                    os.chdir(path)
                    file_list = os.listdir(path)
                    self.get_local_files(file_list)
                    # return to parent dir (necessary!)
                    os.chdir('..')
                else:
                    print color.render_color(path) 
                    self.put_files_count += 1
        
    
    def put_to_upyun(self, source, destnation):
        pass

    def action_get(self, args):
        pass
    
    def action_cd(self, parser, args):
        if args.help:
            parser.print_help()
        if not args.path:
            return
        workspace = self.get_path(args.path)
        self.cloud.swith_workspace(workspace)
        print self.cloud.get_current_workspace() + '\n'

    def action_mkdir(self, args):
        for directory in args.path:
            directory = self.get_path(directory)
            if args.parents:
                print 'recursive create the directory: %s' % directory
                dir_list = directory.split('/')[1:-1]
                # 先检查第一级目录
                parent_dir = self.get_path(dir_list[0])
                file_type = self.check_file(parent_dir)
                if not file_type:
                    self.cloud.create_dir(parent_dir)
                # 如果目录只有一级直接返回
                if len(dir_list) == 1: continue

                for dir_name in dir_list[1:]:
                    parent_dir += dir_name + '/'
                    file_type = self.check_file(parent_dir)
                    if not file_type:  #文件不存在
                        self.cloud.create_dir(parent_dir)
            else:
                self.cloud.create_dir(directory)
        else:
            print 'All the files to create success!'
            # refresh current workspace cache 
            self.cloud.get_file_list(self.cloud.get_current_workspace()) 
    
    def check_file(self, path):
        '''check the file exits.if the file exits,returns the file type else returns False'''
        info = {}
        try:
            info = self.cloud.get_file_info(path)
        except upyun.UpYunServiceException as e:
            pass
        if not info:
            return False
        return info['file-type']

    def action_cat(self, args):
        pass

    def action_rm(self, args):
        for directory in args.path:
            directory = self.get_path(directory)
            if args.recursive:
                print 'Recursive delete the directory: %s' % directory
                self.recursive_rm(directory)
                self.cloud.remove_files(directory)
            else:
                self.cloud.remove_files(directory)
        else:
            print 'All files deleted successfully!'
            # refresh current workspace cache 
            try:
                self.cloud.get_file_list(self.cloud.get_current_workspace()) 
            except upyun.UpYunServiceException as e:
                self.cloud.clear_file_list_cache()
                print 'The current working directory is failure！Please return to / .'

    def recursive_rm(self,path):
        file_type = self.check_file(path)
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
                if self.check_file(sub_path) == 'folder':
                    self.recursive_rm(sub_path)
                    self.cloud.remove_files(sub_path)
                else:
                    self.cloud.remove_files(sub_path)
            else:
                print 'sucess !'

    # help_command methods ...
    def help_ls(self):
        name = 'ls - list directory content'
        synopsis = 'ls [-l | -d] [FILE]'
        description = 'List information about the FILEs (the current directory by default).\n' + \
                      '\n\tJust support short options now O(∩_∩)O !\n' + \
                      '\n\t(usage example): ls\n'+\
                      '\t\tlist current directory content.\n' + \
                      '\n\t-d\n' + \
                      '\t\tlist directory entries instead of contents.\n' + \
                      '\n\t-l\n' + \
                      '\t\tuse a long listing format.show file\'s detail information.'
        self.format_helpinfo(name, synopsis, description)

    def help_put(self):
        name = 'put - put file to upyun'
        synopsis = 'put [source] [destnation]'
        description = '[source] is your local file\'s path\n' + \
                      '\t[description] is upyun space\'s path\n' + \
                      '\tThe [source] and [description] are support the absolute path and the relative path.\n' 
        self.format_helpinfo(name, synopsis, description)

    def help_get(self):
        name = 'get - download files from upyun'
        synopsis = 'get [source] [description]'
        description = '[source] is upyun space\'s path\n' + \
                      '\t[description] is your local file\'s path\n' + \
                      '\tThe [source] and [description] are support the absolute path and the relative path.\n' 
        self.format_helpinfo(name, synopsis, description)

    def help_cd(self):
        name = 'cd - switch your work space'
        synopsis = 'cd [path]'
        description = 'this commad will enter into / by default.\n' + \
                      '\tThe [path]  support the absolute path and the relative path.\n' 
        self.format_helpinfo(name, synopsis, description)

    def help_pwd(self):
        name = 'pwd - show your current work space'
        synopsis = 'pwd'
        description = 'No parameters'
        self.format_helpinfo(name, synopsis, description)

    def help_mkdir(self):
        name = 'mkdir - make directories'
        synopsis = 'mkdir DIRECTORY...'
        description = 'Create the DIRECTORYs, if they do not already exist.'
        self.format_helpinfo(name, synopsis, description)

    def help_cat(self):
        name = 'cat - concatenate files and print on the standard output'
        synopsis = 'cat FILE'
        description = 'The parameter FILE  support the absolute path and the relative path.\n' 
        self.format_helpinfo(name, synopsis, description)

    def help_rm(self):
        name = 'rm - remove files or directories'
        synopsis = 'rm [FILEs OR DIRECTORYs PATH]'
        description = 'support the absolute path and the relative path.\n'
        self.format_helpinfo(name, synopsis, description)

    def help_usage(self):
        name = 'usage - show the use of information'
        synopsis = 'usage'
        description = 'No parameters'
        self.format_helpinfo(name, synopsis, description)

    def help_exit(self):
        name = 'exit - exit program'
        synopsis = 'exit'
        description = 'No parameters'
        self.format_helpinfo(name, synopsis, description)
    
        name = 'quit | q - exit program '
    def help_quit(self):
        synopsis = 'quit | q'
        description = "The command 'quit' and 'q' have the same action as command 'exit'.\n" + \
                      "\tplease run help exit see more info."

        self.format_helpinfo(name, synopsis, description)

    def help_help(self):
        name = 'help - help you get more command usage'
        synopsis = 'help [command]'
        self.format_helpinfo(name, synopsis)

    def help_clear(self):
        name = 'clear  - clear the terminal screen'
        synopsis = 'clear'
        description = 'clear has alias "cls" '
        self.format_helpinfo(name, synopsis, description)


    # overrid some methods ...

    # overrid this method. It will do nothing, when you input a empty line.
    def emptyline(self):
        pass

    def default(self, command):
        if command == 'EOF':
            self.do_exit('')
        
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
            print 'login failed ! please check your login info.'
            sys.exit(1)
        except upyun.UpYunClientException as e:
            self.show_error(error='Client error',msg=e.msg)
            sys.exit(1)
        except KeyboardInterrupt:
            print '\nNetwork is busy, please try again later !\n'
            sys.exit(1)
        print '\n login sucess ! Have a nice day !'

    def get_help_message(self):
        intro='\n\tWelcome to use upcloud ! version: '+str(__version__)+'\n\n'+\
               'You can use this tool to manage your remote space easily. Enjoy it !\n\n' + \
               'Type "help" or "?" for help.\n' + \
               'Type "-h" or "--help" behind a command for help.\n' + \
               'Type double <Tab> key to get a command list.\n' + \
               'Type "![command]" or "shell [command]" run a shell command. example: !ls\n' + \
               'Type "cls" or "clear" to clear the terminal screen. \n' + \
               'Type "man" show this message again.\n'
        return intro

    def parse_cmdline(self, command, args):
        
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
                parser.add_argument('-l', '--list', action='store_true',
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
                parser.add_argument('-d', '--destnation', required='True', 
                        help='The file path of your bucket<UpYun space>')
                args_list = parser.parse_args(args)
                self.action_put(args_list)
            elif command == 'get':
                parser = argparse.ArgumentParser(prog='man', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('command', nargs='?', default='w',help='')
                args_list = parser.parse_args(args)
                self.action_man(args_list)
            elif command == 'cd':
                parser = argparse.ArgumentParser(prog='cd', add_help=False,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                        epilog='Type "man cd" get more info.')
                group = parser.add_mutually_exclusive_group()
                group.add_argument('-h', '--help', action='store_true', 
                        help='show this message and return.')
                group.add_argument('path', nargs='?', default='/',
                        help='Your destnation workspace')
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
                parser = argparse.ArgumentParser(prog='man', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('command', nargs='?', default='w',help='')
                args_list = parser.parse_args(args)
                self.action_man(args_list)
            elif command == 'rm' :
                parser = argparse.ArgumentParser(prog='rm', add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
                parser.add_argument('-r', '--recursive', action='store_true', 
                        help='remove directories and their contents recursively')
                parser.add_argument('-f', '--force', action='store_true',
                        help='ignore nonexistent files, never prompt')
                parser.add_argument('path', nargs='+', help='remove one or more files or directories')
                args_list = parser.parse_args(args)
                self.action_rm(args_list)
            else:
                self.command_not_found(command)
        except upyun.UpYunServiceException as e:
            self.show_error(error='Server error', msg=e.msg)
        except upyun.UpYunClientException as e:
            self.show_error(error='Client error', msg=e.msg)

    def show_help(self, command, args):
        if '-h' in args or '--help' in args:
            if command == 'man':
                print 'Type "man -h" for help'
            elif command == 'ls':
                self.help_ls()
            elif command == 'put':
                self.help_put()
            elif command == 'get':
                self.help_get()
            elif command == 'cd':
                self.help_cd()
            elif command == 'pwd':
                self.help_pwd()
            elif command == 'mkdir':
               self.help_mkdir()
            elif command == 'cat':
                self.help_cat()
            elif command == 'rm' :
                self.help_rm()
            elif command == 'usage':
                self.help_usage()
            elif command == 'exit':
                self.help_exit()
            elif command == 'quit':
                self.help_quit()
            elif command == 'clear':
                self.help_clear()
            else:
                self.command_not_found(command)

    def handle_args(self,args):
        arg_list = args.split()
    #    for arg in arg_list:
    #        print arg
        return arg_list

    def format_helpinfo(self,name='None', synopsis='None', description='None'):
        info = 'NAME\n' + \
               '\t' +name + '\n\n' + \
               'SYNOPSIS\n' + \
               '\t' + synopsis + '\n\n' + \
               'DESCRIPTION\n' + \
               '\t'+description 
        print info
    
    def get_path(self, path, sys=False):
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
            #    print 'current version: %r not support this path.' % __version__
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

    def  human_readable(self, usage):
        '''format usage to human readable'''
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
    do_quit = do_exit
    do_q = do_exit
    do_cls = do_clear
    #help_q = help_quit
    #help_cls = help_clear

if __name__ == '__main__':
    import upyun
    cli = CLI(username='kehr',passwd='kehr4444',bucket='kehrspace',timeout=30,endpoint=upyun.ED_AUTO)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print color.render_color('\nWarning: operation was interrupted by user !')
    except SystemExit:
        pass 
