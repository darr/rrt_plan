#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : kdtree.py
# Create date : 2021-05-12 21:02
# Modified date : 2021-05-12 21:02
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

#---------------KD tree, used for nearest neighbor search
class kdTree:
    def __init__(self):
        pass

    def R1_dist(self, q, p):
        return abs(q-p)

    def S1_dist(self, q, p):
        return min(abs(q-p), 1- abs(q-p))

    def P3_dist(self, q, p):
        # cubes with antipodal points
        q1, q2, q3 = q
        p1, p2, p3 = p
        d1 = np.sqrt((q1-p1)**2 + (q2-p2)**2 + (q3-p3)**2)
        d2 = np.sqrt((1-abs(q1-p1))**2 + (1-abs(q2-p2))**2 + (1-abs(q3-p3))**2)
        d3 = np.sqrt((-q1-p1)**2 + (-q2-p2)**2 + (q3+1-p3)**2)
        d4 = np.sqrt((-q1-p1)**2 + (-q2-p2)**2 + (q3-1-p3)**2)
        d5 = np.sqrt((-q1-p1)**2 + (q2+1-p2)**2 + (-q3-p3)**2)
        d6 = np.sqrt((-q1-p1)**2 + (q2-1-p2)**2 + (-q3-p3)**2)
        d7 = np.sqrt((q1+1-p1)**2 + (-q2-p2)**2 + (-q3-p3)**2)
        d8 = np.sqrt((q1-1-p1)**2 + (-q2-p2)**2 + (-q3-p3)**2)
        return min(d1,d2,d3,d4,d5,d6,d7,d8)
