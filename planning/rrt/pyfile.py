#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : pyfile.py
# Create date : 2013-07-17 19:19
# Modified date : 2021-05-10 00:58
# Author : DARREN
# Describe : not set
# Email : lzygzh@126.com
#####################################

from __future__ import division
from __future__ import print_function

import os
import sys

from . import pylog

def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def get_file_full_name(path, name):
    create_path(path)
    if path[-1] == "/":
        full_name = path +  name
    else:
        full_name = path + "/" +  name
    return full_name

def open_file(path, name, open_type='a'):
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)

def create_file(path, name, open_type='w'):
    file_name = get_file_full_name(path, name)
    return open_file_with_full_name(file_name, open_type)

def check_is_have_file(path, name):
    file_name = get_file_full_name(path, name)
    return os.path.exists(file_name)

def open_file_with_full_name(full_path, open_type):
    try:
        file_object = open(full_path, open_type)
        return file_object
    except Exception as e:
        if e.args[0] == 2:
            open(full_path, 'w')
        else:
            pylog.error(e)

def delete_a_file(path, name):
    if check_is_have_file(path, name):
        file_name = get_file_full_name(path, name)
        if os.path.isfile(file_name):
            os.remove(file_name)

