#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : pylog.py
# Create date : 2019-10-15 09:21
# Modified date : 2021-01-16 21:51
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################


from __future__ import division
from __future__ import print_function

import datetime
import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from os.path import join, getsize
import operator


LOG_LEVEL_DIC = {}
PYLOG_IS_INIT = False


def get_log_level_dic():
    level_dic = {}
    level_dic['all'] = 0
    level_dic['debug'] = 10
    level_dic['info'] = 20
    level_dic['warning'] = 30
    level_dic['error'] = 40
    level_dic['critical'] = 50
    return level_dic


def init_log():
    global LOG_LEVEL_DIC
    global PYLOG_IS_INIT

    LOG_LEVEL_DIC = get_log_level_dic()
    PYLOG_IS_INIT = True


def get_log_file_name():
    LOG_FILE_NAME = "logfile"
    return LOG_FILE_NAME


def get_log_file_path():
    LOG_FILE_PATH = "./logs/"
    return LOG_FILE_PATH


def get_file_log_level():
    LOG_WRITE_LEVEL = 'debug'
    return LOG_WRITE_LEVEL


def get_print_log_level():
    LOG_PRINT_LEVEL = 'info'
    return LOG_PRINT_LEVEL


def get_print_log_all_info_level():
    LOG_PRINT_ALL_INFO_LEVEL = 'warning'
    return LOG_PRINT_ALL_INFO_LEVEL


def get_log_full_name(log_path=""):
    if log_path:
        full_path = '%s%s' % (log_path, datetime.datetime.now().strftime('%Y-%m-%d'))
    else:
        full_path = '%s%s' % (get_log_name(), datetime.datetime.now().strftime('%Y-%m-%d'))
    return full_path


def get_log_name():
    path = get_log_file_path()
    if not os.path.isdir(path):
        os.makedirs(path)
    return '%s%s' % (path, get_log_file_name())


def write_log(log, log_path=""):
    full_fill_name = get_log_full_name(log_path)
    if os.path.isfile(full_fill_name):
        pass
    else:
        check_dir_size()
        full_fill_name = get_log_full_name(log_path)
    file_object = open(full_fill_name, 'a', encoding="utf-8")
    try:
        file_object.write(log)
    finally:
        file_object.close()


def out_put_log2(level, content, log_path="", log_key="log", stack_layer=2, ):
    func_name = sys._getframe(stack_layer).f_code.co_name
    file_name = sys._getframe(stack_layer).f_code.co_filename
    line = sys._getframe(stack_layer).f_lineno
    now_time = datetime.datetime.now()
    # log_format = 'LEVEL:%s, LINE:%s, FUNC:%s, FILE:%s, TIME:%s, CONTENT:%s\n'
    log_format = 'LEVEL:%s, LINE:%s, FUNC:%s, FILE:%s, TIME:%s, CONTENT:%s'
    con = log_format % (level, line, func_name, file_name, now_time, content)

    if is_print_log(level):
        if is_print_log_all_info(level):
            print(con)
        else:
            f_name = file_name.split('/')[-1]
            print("%s line:%s %s" % (f_name, line, content))

    if is_write_log(level):
        write_log("%s\n" % con, log_path)

def out_put_log(level, content, log_path="", log_key="log", stack_layer=2, ):
    func_name = sys._getframe(stack_layer).f_code.co_name
    file_name = sys._getframe(stack_layer).f_code.co_filename
    line = sys._getframe(stack_layer).f_lineno
    now_time = datetime.datetime.now()
    log_format = 'LEVEL:%s, LINE:%s, FUNC:%s, FILE:%s, TIME:%s, CONTENT:%s\n'
    #log_format = 'LEVEL:%s, LINE:%s, FUNC:%s, FILE:%s, TIME:%s, CONTENT:%s'
    con = log_format % (level, line, func_name, file_name, now_time, content)

    if is_print_log(level):
        if is_print_log_all_info(level):
            #print(con)
            print_str = con
            sys.stdout.write(print_str)
            sys.stdout.flush()
        else:
            f_name = file_name.split('/')[-1]
            #print("%s line:%s %s" % (f_name, line, content))
            print_str = "%s line:%s %s\n" % (f_name, line, content)
            sys.stdout.write(print_str)
            sys.stdout.flush()

    if is_write_log(level):
        write_log("%s\n" % con, log_path)


def get_description_str(content, stack_layer=2):
    func_name = sys._getframe(stack_layer).f_code.co_name
    file_name = sys._getframe(stack_layer).f_code.co_filename
    line = sys._getframe(stack_layer).f_lineno
    log_format = 'LINE:%s, FUNC:%s, FILE:%s, CONTENT:%s'
    con = log_format % (line, func_name, file_name, content)
    return con

def check_dir_size():
    dir_name = get_log_file_path()
    dir_size = get_dir_size(dir_name)
    if dir_size > 200 * 1024 * 1024:
        delete_log_dir()


def get_dir_size(dir_name):
    size = 0
    for root, dirs, files in os.walk(dir_name):
        size += sum([getsize(join(root, name)) for name in files])

    return size


def delete_log_dir():
    dir_name = get_log_file_path()
    delete_file_folder(dir_name)


def delete_file_folder(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass

    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


def debug(content, log_path="", ):
    level = 'debug'
    out_put_log(level, content, log_path)


def auto_test_debug(content, log_path=""):
    level = 'debug'
    out_put_log(level, content, log_path, stack_layer=3)


def error(content, log_path=""):
    level = 'error'
    out_put_log(level, content, log_path)


def auto_test_error(content, log_path=""):
    level = 'error'
    out_put_log(level, content, log_path, stack_layer=3)


def warning(content, log_path=""):
    level = 'warning'
    out_put_log(level, content, log_path)


def info(content, log_path=""):
    level = "info"
    out_put_log(level, content, log_path)


def auto_test_info(content, log_path=""):
    level = "info"
    out_put_log(level, content, log_path, stack_layer=3)


def critical(content, log_path=""):
    level = 'critical'
    out_put_log(level, content, log_path)


def condition_value_is_null(content="", log_path=""):
    # error(content)
    level = 'error'
    # out_put_log(level, content, log_path, stack_layer=3)
    out_put_log(level, content, log_path, stack_layer=2)


def is_print_log(log_level):
    global LOG_LEVEL_DIC
    config_log_level = LOG_LEVEL_DIC[get_print_log_level()]
    current_log_level = LOG_LEVEL_DIC[log_level]
    if current_log_level >= config_log_level:
        return True
    return False


def is_print_log_all_info(log_level):
    global LOG_LEVEL_DIC
    config_log_level = LOG_LEVEL_DIC[get_print_log_all_info_level()]
    current_log_level = LOG_LEVEL_DIC[log_level]
    if current_log_level >= config_log_level:
        return True
    return False


def is_write_log(log_level):
    global LOG_LEVEL_DIC
    config_log_level = LOG_LEVEL_DIC[get_file_log_level()]
    current_log_level = LOG_LEVEL_DIC[log_level]
    if current_log_level >= config_log_level:
        return True
    return False


def test_compare_value(real_value, expected_value):
    if real_value != expected_value:
        auto_test_error("real:%s expect:%s" % (real_value, expected_value))
    else:
        auto_test_debug("real:%s expect:%s" % (real_value, expected_value))

def test_compare_data(real_value, expected_value):
    if not operator.eq(real_value ,expected_value):
        auto_test_error("real:%s expect:%s" % (real_value, expected_value))
    else:
        auto_test_debug("real:%s expect:%s" % (real_value, expected_value))


init_log()
