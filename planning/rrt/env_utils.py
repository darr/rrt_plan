#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : env_utils.py
# Create date : 2021-05-10 00:29
# Modified date : 2021-05-13 02:16
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import numpy as np
from .aabb import aabb
from . import pylog

from .utils import cal_rotation_matrix

def R_matrix(z_angle,y_angle,x_angle):
    ret = cal_rotation_matrix(z_angle, y_angle, x_angle)
    return ret

def getblocks():
    # AABBs
    block = [[4.00e+00, 1.20e+01, 0.00e+00, 5.00e+00, 2.00e+01, 5.00e+00],
             [5.5e+00, 1.20e+01, 0.00e+00, 1.00e+01, 1.30e+01, 5.00e+00],
             [1.00e+01, 1.20e+01, 0.00e+00, 1.40e+01, 1.30e+01, 5.00e+00],
             [1.00e+01, 9.00e+00, 0.00e+00, 2.00e+01, 1.00e+01, 5.00e+00],
             [9.00e+00, 6.00e+00, 0.00e+00, 1.00e+01, 1.00e+01, 5.00e+00]]
    Obstacles = []
    for i in block:
        i = np.array(i)
        Obstacles.append([j for j in i])
    return np.array(Obstacles)

def getballs():
    #spheres = [[2.0,6.0,2.5,1.0],[16.0,12.0,25.5,2]] #[[2.0,6.0,2.5,1.0],[14.0,14.0,2.5,2]] [16.0,12.0,35.5,4]]
    spheres = [[10.0,12.0,300,3.0],[16.0,12.0,400,2]] #[[2.0,6.0,2.5,1.0],[14.0,14.0,2.5,2]] [16.0,12.0,35.5,4]]
    Obstacles = []
    for i in spheres:
        Obstacles.append([j for j in i])
    return np.array(Obstacles)

def getAABB(blocks):
    # used for Pyrr package for detecting collision
    AABB = []
    for i in blocks:
        AABB.append(np.array([np.add(i[0:3], -0), np.add(i[3:6], 0)]))  # make AABBs alittle bit of larger
    return AABB

def getAABB2(blocks):
    # used in lineAABB
    AABB = []
    for i in blocks:
        AABB.append(aabb(i))
    return AABB

def add_block(block = [1.51e+01, 0.00e+00, 2.10e+00, 1.59e+01, 5.00e+00, 6.00e+00]):
    return block
