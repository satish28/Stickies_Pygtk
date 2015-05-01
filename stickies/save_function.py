#!/usr/bin/env python

import os
import time

# get home directory of the user
def get_home_directory():
    return os.path.expanduser('~')

# create project directory
def get_project_directory():
    sticky_dir = "/.Sticky"
    home_dir = get_home_directory()
    project_dir = home_dir + sticky_dir
    return project_dir

# check directory if present
def check_directory():
    project_dir = get_project_directory()
    if not os.path.exists(project_dir):
        create_directory()
        return True
    return True

# create directory if not present
def create_directory():
    project_dir = get_project_directory()
    os.makedirs(project_dir)
    return True

def create_filename():
    filename = ""
    filename = str(time.localtime().tm_year) +str(time.localtime().tm_mon) + str(time.localtime().tm_mday) +str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)+ ".txt"
    return filename



# save notes    
def save_sticky(notes, name):
    if check_directory():
        project_dir = get_project_directory()
        os.chdir(project_dir)
        if name == None:
            filename = create_filename()
        else:
            filename = name
        filename_descriptor = open(filename, 'w')
        filename_descriptor.write(notes)
    return filename
