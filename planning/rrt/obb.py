#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : obb.py
# Create date : 2021-05-10 00:25
# Modified date : 2021-05-10 00:26
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################
import numpy as np

class obb(object):
    # P: center point
    # E: extents
    # O: Rotation matrix in SO(3), in {w}
    def __init__(self, P, E, O):
        self.P = P
        self.E = E
        self.O = O
        self.T = np.vstack([np.column_stack([self.O.T,-self.O.T@self.P]),[0,0,0,1]])
