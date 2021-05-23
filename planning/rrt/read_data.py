#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : read_data.py
# Create date : 2021-05-09 20:31
# Modified date : 2021-05-21 00:55
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################
import numpy as np
import pandas as pd
from . import pylog


def read_data(data_file_path):
    data = pd.read_table(data_file_path,header = None, sep=' ')
    data = data.dropna(axis=1,how='all') ##删除空列
    data = np.array(data)
    data = data[:20]
    data = data[:,:20] #取前30平方个格子y?
    #pylog.info(data)
    #pylog.info(type(data))
    #less 100 set 100

    #data = data / 10
    idx= np.where(data<150) 
    data[idx] = 150
    idx= np.where(data>200) 
    data[idx] = 200

    #idx= np.where(200>data>100) 
    #data[idx] = 200

    #pylog.info(data)
    
    #raise
    return data, data.shape[1], data.shape[0], np.max(data) #源数据，列，行，海拔最大值

def read_maps(file_path):
    data = pd.read_table(file_path,header = None, sep=' ')
    data = data.dropna(axis=1,how='all') ##删除空列
    data = np.array(data)

    idx= np.where(data<150) 
    data[idx] = 150
    idx= np.where(data>200) 
    data[idx] = 200
    return data, data.shape[1], data.shape[0], np.max(data) #源数据，列，行，海拔最大值

#   def read_data2(data_file_path):
#       data = pd.read_table(data_file_path,header = None, sep=' ')
#       data = data.dropna(axis=1,how='all') ##删除空列
#       data = np.array(data)
#       data = data[:100]
#       data = data[:,:110] #取前30平方个格子y?
#       return data, data.shape[1], data.shape[0], np.max(data) #源数据，列，行，海拔最大值
