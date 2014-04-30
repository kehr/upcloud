#! /usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# @File Name:    color.py
# @Author:	     kehr
# @Mail:		 kehr.china@gmail.com
# @Created Time: Wed 30 Apr 2014 12:33:26 PM CST
# @Copyright:    MIT applies
#########################################################################
class colors:
    PATH = '\033[7;37;40m'
    PURPLE = '\033[95m'
    BLUE = '\033[1;94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[1;91m'
    END = '\033[0m'
    
PATH = '\033[7;37;40m'
PURPLE = '\033[95m'
BLUE = '\033[1;94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
ERROR = '\033[1;91m'
END = '\033[0m'

def parse_color(color):
    if color == 'path':
        return PATH
    elif color == 'purple':
        return PURPLE
    elif color == 'blue':
        return BLUE
    elif color == 'green':
        return GREEN
    elif color == 'yellow' or color == 'warning':
        return WARNING
    elif color == 'red' or color == 'error':
        return ERROR

def render_color(msg, color='yellow'):
    color = parse_color(color)  
    return '%s%s%s' % (color, msg, colors.END)
