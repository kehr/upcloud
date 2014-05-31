#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    manual.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Thu 01 May 2014 03:55:54 PM CST
# @Copyright:    MIT applies
# @Description:  the manul of cli            
#########################################################################
from __init__ import __version__ as version

__version__ = version 

def ls():
    name = 'ls - list directory content'
    synopsis = 'ls [OPTIONS] [PATH ...]'
    description = '1. List the information about the FILEs, The default directory is current working directory.\n' + \
                  '\t   example: ls\n'+\
                  '\t2. -d, --directory, list directory entries instead of contents.\n' + \
                  '\t   example: ls -d dir1 dir2 ...\n' + \
                  '\t   If you want to get more information about the directory,\n' + \
                  '\t   type: ls -ld dir1, dir2 ...\n' + \
                  '\t3. -l, --list, Use a long listing format.show file\'s detail information.\n' +\
                  '\t   example: ls -l dir1 dir2 ...\n' + \
                  '\t4. -r, --refresh, Refresh the file list of current working directory.\n' +\
                  '\t   example: ls -r\n' + \
                  '\t5. -R, --reverse, list subdirectories recursively.\n' +\
                  '\t   example: ls -R\n' + \
                  '\t6. -s, --sort, sort the file list. You can sort it by name, type, size, or time.\n' +\
                  '\t   example: ls -s time\n' 

    format_helpinfo(name, synopsis, description)

def put():
    name = 'put - put file to upyun'
    synopsis = 'put [OPTIONS] PATH ...'
    description = '1. -s, --source, Your local file location which can be multiple files path or folders path. This parameter is required.\n' + \
                  '\t   example: put -s file1 file2 dir1 dir2 ...\n' + \
                  '\t2. -d, --destination, Your cloud directory location. The default path is "/".\n' + \
                  '\t   examlpe: put -s file1 -d /temp/ \n' + \
                  '\t3. -l, --level, Specify the save file path level. Default is 0, it means upload the full path of file which start with "/".\n' + \
                  '\t   The vlaue also support negative number.\n' + \
                  '\t   Assume the full path of the file "test_file" is "/home/kehr/temp/test_file",\n'+\
                  '\t   if you want to upload to cloud as /tmp/temp/test_file.\n'+\
                  '\t       type: get -s /home/kehr/temp/test_file -d /tmp -l 2 \n'+\
                  '\t   if you just want to upload the name of the file,\n'+\
                  '\t       type: get -s /home/kehr/temp/test_file -d /tmp -l -1 \n'
    format_helpinfo(name, synopsis, description)

def get():
    name = 'get - download files from upyun'
    synopsis = 'get [OPTIONS] PATH ...'
    description = '1. -s, --source, Your cloud file location which can be multiple files path or folders path. This parameter is required.\n' + \
                  '\t   example: get -s file1 file2 dir1 dir2 ...\n' + \
                  '\t2. -d, destination, Your local directory location. The default path is current working directory.\n' + \
                  '\t   examlpe: get -s file1 -d /home/kehr/temp \n' + \
                  '\t3. -l, --level, Specify the save file path level. Default is 0, it means save the full path of file which start with "/".\n' + \
                  '\t   The vlaue also support negative number.\n' + \
                  '\t   Assume the full path of the file "test_file" is "/a/b/c/d/test_file",\n'+\
                  '\t   if you want to save to local system as /home/kehr/temp/c/d/test_file.\n'+\
                  '\t       type: get -s /a/b/c/test_file -d /home/kehr/temp -l 2 \n'+\
                  '\t   if you just want to save the name of the file,\n'+\
                  '\t       type: get -s /a/b/c/test_file -d /home/kehr/temp -l -1 \n'

    format_helpinfo(name, synopsis, description)

def cd():
    name = 'cd - switch your work space'
    synopsis = 'cd PATH'
    description = 'This commad will enter into / by default.\n' + \
                  '\t1. The [path]  support the absolute path and the relative path.\n' + \
                  '\t2. You can type "cd .." return to parent directory.\n' 
    format_helpinfo(name, synopsis, description)

def pwd():
    name = 'pwd - show your current work space'
    synopsis = 'pwd'
    description = 'Print your current workspace of upyun with No parameters'
    format_helpinfo(name, synopsis, description)

def mkdir():
    name = 'mkdir - make directories'
    synopsis = 'mkdir [OPTION] DIRECTORY ...'
    description = 'Create the DIRECTORYs, if they do not already exist.\n' +\
                  '\t1. This command will create folders in the current directory by default.\n' + \
                  '\t   example: mkdir dir1 dir2 ...\n' + \
                  '\t2. -p, --parent, You can use the -p parameter to create multiple directories.\n ' +\
                  '\t   example: mkdir -p /a/b/c/d\n' 
    format_helpinfo(name, synopsis, description)

def cat():
    name = 'cat - view the online file content'
    synopsis = 'cat [OPTION] FILE'
    description = 'The parameter FILE  support the absolute path and the relative path.\n' + \
                  '\t1. -n, --number, View the first n line of the  file. As the head command.\n' + \
                  '\t   example: cat -n 10 test_file \n' + \
                  '\t2. -t, --tail, View the After n line of the file. As the tail command. \n' + \
                  '\t   example: cat -t 10 test_file \n' + \
                  '\t3. View all content of the file by default.\n' + \
                  '\t   example: cat test_file\n'
    format_helpinfo(name, synopsis, description)

def rm():
    name = 'rm - remove files or directories'
    synopsis = 'rm [OPTION] FILEs ...'
    description = 'support the absolute path and the relative path.\n' + \
                  '\t1. Remove empty directory and normal files.\n' + \
                  '\t   example: rm file1 file2 ...\n' + \
                  '\t2. -r, --recursive,  Remove directories and their contents recursively.\n' + \
                  '\t   example: rm -r dir1 dir2 ...\n'
    format_helpinfo(name, synopsis, description)

def usage():
    name = 'usage - show the use of information'
    synopsis = 'usage'
    description = 'No parameters'
    format_helpinfo(name, synopsis, description)

def exit():
    name = 'exit - exit program'
    synopsis = 'exit'
    description = 'No parameters'
    format_helpinfo(name, synopsis, description)

def quit():
    name = 'quit | q - exit program '
    synopsis = 'quit | q'
    description = "The command 'quit' and 'q' have the same action as command 'exit'.\n" + \
                  "\tplease run help exit see more info.\n"

    format_helpinfo(name, synopsis, description)

def help():
    name = 'help - help you get more command usage'
    synopsis = 'help [command]'
    description = 'You can use this command get more information.\n' + \
                  '\texample: help ls or ?ls'
    format_helpinfo(name, synopsis, description)

def clear():
    name = 'clear  - clear the terminal screen'
    synopsis = 'clear'
    description = 'clear has alias "cls" '
    format_helpinfo(name, synopsis, description)

def get_manual(command, args):
    if '-h' in args or '--help' in args:
        if command == 'man':
            print 'Type "man -h" for help'
        elif command == 'ls':
            ls()
        elif command == 'put':
            put()
        elif command == 'get':
            get()
        elif command == 'cd':
            cd()
        elif command == 'pwd':
            pwd()
        elif command == 'mkdir':
            mkdir()
        elif command == 'cat':
            cat()
        elif command == 'rm' :
            rm()
        elif command == 'usage':
            usage()
        elif command == 'exit':
            exit()
        elif command == 'quit':
            quit()
        elif command == 'clear':
            clear()
        else:
            pass 

def format_helpinfo(name='None', synopsis='None', description='None'):
    info = 'NAME\n' + \
           '\t' +name + '\n\n' + \
           'SYNOPSIS\n' + \
           '\t' + synopsis + '\n\n' + \
           'DESCRIPTION\n' + \
           '\t'+description 
    print info

def get_tips():
    intro='\n\tWelcome to use upcloud ! version: '+str(__version__)+'\n\n'+\
           'You can use this tool to manage your remote space easily. Enjoy it !\n\n' + \
           'Type "man" show this message again.\n' + \
           'Type "help" or "?" for help.\n' + \
           'Type "-h" or "--help" behind a command for help.\n' + \
           'Type "![command]" or "shell [command]" run a shell command. example: !ls\n' + \
           'Type "bash" enter the local bash environment. \n' + \
           'Type "cls" or "clear" to clear the terminal screen. \n' + \
           'Type double <Tab> key to get a command list.\n' 
    return intro
