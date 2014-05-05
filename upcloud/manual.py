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
    description = 'List information about the FILEs (the current directory by default).\n' + \
                  '\n\tJust support short options now O(∩_∩)O !\n' + \
                  '\n\t(usage example): ls\n'+\
                  '\t\tlist current directory content.\n' + \
                  '\n\t-d\n' + \
                  '\t\tlist directory entries instead of contents.\n' + \
                  '\n\t-l\n' + \
                  '\t\tuse a long listing format.show file\'s detail information.'
    format_helpinfo(name, synopsis, description)

def put():
    name = 'put - put file to upyun'
    synopsis = 'put [OPTIONS] [PATH ...]'
    description = ' \n' + \
                  '[source] is your local file\'s path\n' + \
                  '\t[destination] is upyun space\'s path\n' + \
                  '\tThe [source] and [destination] are support the absolute path and the relative path.\n' 
    format_helpinfo(name, synopsis, description)

def get():
    name = 'get - download files from upyun'
    synopsis = 'get [OPTIONS] [PATH ...]'
    description = '[source] is upyun space\'s path\n' + \
                  '\t[destination] is your local file\'s path\n' + \
                  '\tThe [source] and [destination] are support the absolute path and the relative path.\n' 
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
    synopsis = 'mkdir DIRECTORY ...'
    description = 'Create the DIRECTORYs, if they do not already exist.\n' +\
                  '\t1. You can use the -p parameter to create multiple directories.\n ' +\
                  '\t   example: mkdir -p /a/b/c/d\n' + \
                  '\t2. The mkdir will create folders in the current directory by default.\n' + \
                  '\t   example: mkdir dir1 dir2 ...'
    format_helpinfo(name, synopsis, description)

def cat():
    name = 'cat - view the online file content'
    synopsis = 'cat [OPTION] FILE'
    description = 'The parameter FILE  support the absolute path and the relative path.\n' + \
                  '\t1. -n, View the first n line of the  file. As the head command.\n' + \
                  '\t   example: cat -n 10 test_file \n' + \
                  '\t2. -t, View the After n line of the file. As the tail command. \n' + \
                  '\t   example: cat -t 10 test_file \n' + \
                  '\t3. View all content of the file by default.\n' + \
                  '\t   example: cat test_file\n'
    format_helpinfo(name, synopsis, description)

def rm():
    name = 'rm - remove files or directories'
    synopsis = 'rm [FILEs OR DIRECTORYs PATH]'
    description = 'support the absolute path and the relative path.\n'
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
                  "\tplease run help exit see more info."

    format_helpinfo(name, synopsis, description)

def help():
    name = 'help - help you get more command usage'
    synopsis = 'help [command]'
    format_helpinfo(name, synopsis)

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
