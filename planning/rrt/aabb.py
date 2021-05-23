#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : aabb.py
# Create date : 2021-05-10 00:24
# Modified date : 2021-05-10 00:24
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

class aabb(object):
    # make AABB out of blocks, 
    # P: center point
    # E: extents
    # O: Rotation matrix in SO(3), in {w}
    def __init__(self,AABB):
        self.P = [(AABB[3] + AABB[0])/2, (AABB[4] + AABB[1])/2, (AABB[5] + AABB[2])/2]# center point
        self.E = [(AABB[3] - AABB[0])/2, (AABB[4] - AABB[1])/2, (AABB[5] - AABB[2])/2]# extents
        self.O = [[1,0,0],[0,1,0],[0,0,1]]

