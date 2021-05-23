#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : rrt_plan.py
# Create date : 2021-05-20 23:39
# Modified date : 2021-05-21 01:59
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from numpy.matlib import repmat

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

from . import pylog

from .utils import cal_two_point_distance
from .cal_point import get_check_point_list_from_two_point
from .utils import check_is_above_map

class rrt_plan():
    def __init__(self, a_dic):

        self.stepsize = a_dic["stepsize"]
        self.done = False
        self.env = a_dic["env"]

        self.Parent = {}
        self.V = []
        self.E = set()
        self.i = 0
        self.Path = []
        self.qinit = tuple(self.env.start)
        self.qgoal = tuple(self.env.goal)
        self.x0 = tuple(self.env.start)
        self.xt = tuple(self.env.goal)
        self.qnew = None
        self.ind = 0
        self.fig = plt.figure(figsize=(10,10))#(figsize=(20, 16))

        self.plane_L= self.env.boundary[0:3]
        self.plane_L[2] = min(self.qinit[2]-1, self.qgoal[2]-1) # 飞机高度限制

    def EXTEND(self, tree, q):
        qnear = tuple(self.NEAREST_NEIGHBOR(q, tree))
        qnew, dist = self.env.cal_steer_point(self.stepsize, qnear, q)
        qnew = tuple(map(lambda x: round(x), qnew))
        self.qnew = qnew # store qnew outside  ######################## until here
        if not self.is_collision(qnear, qnew, dist=None):
            tree.add_vertex(qnew)
            tree.add_edge(qnear, qnew)
            if qnew == q:
                return 'Reached'
            else:
                return 'Advanced'
        return 'Trapped'

    def NEAREST_NEIGHBOR(self, q, tree):
        # find the nearest neighbor in the tree
        V = np.array(tree.V)
        if len(V) == 1:
            return V[0]
        xr = repmat(q, len(V), 1)
        dists = np.linalg.norm(xr - V, axis=1)
        return tuple(tree.V[np.argmin(dists)])

    def is_collision(self, qnear, qnew, dist = None):
        collide, _ = self.env.check_is_collision(qnear, qnew, dist = dist)
        return collide

#----------RRT connect algorithm
    def CONNECT(self, Tree, q):
        #pylog.info("try connect")
        while True:
            S = self.EXTEND(Tree, q)
            if S != 'Advanced':
                break
        return S

    def process_path(self, a_path):
        new_path = []
        new_path.append(a_path[0])
        last_point = None

        for i in range(1, len(a_path)-1):
            start_point = new_path[-1]
            a_point = a_path[i]
            next_point = a_path[i+1]

            #res = self.check_two_point_connect(start_point, a_point)
            #res2 = self.check_two_point_connect(start_point, next_point)
            #跟前一个点可以连通，跟后面的点不能连通 说明当前的点不能被丢掉
            #if res2 == False and res == True:
            #    new_path.append(a_point)

            res = self.is_collision(start_point, a_point)
            res2 = self.is_collision(start_point, next_point)

            #跟前一个点not collision，跟后面的点collision 说明当前的点不能被丢掉

            if res2 == True and res == False:
                new_path.append(a_point)
            #pylog.info(new_path)

        new_path.append(a_path[-1])
        pylog.info(new_path)
        return new_path


#   def check_two_point_connect(self, point1, point2):
#       '''
#       检查两个点连接后的直线所经过的点，
#       这些点的高程有一个比地图上的点低，
#       那么返回 False，说明这两个点不能连线。
#       所有点的高程都比地图上的点高，
#       那么返回True， 说明这两个点可以连线
#       可以设定距离阈值，超过这个距离阈值就不能连线。
#       '''

#       item = ((int(point1[0]), int(point1[1])),
#               (int(point2[0]), int(point2[1]))
#               )

#       point_lt  = get_check_point_list_from_two_point(item)

#       ret_lt = []
#       for p in point_lt:
#           new_p = (p[0],p[1], min(point1[2], point2[2]))
#           ret = check_is_above_map(self.env.mapinfo, new_p)
#           ret_lt.append(ret)

#       res = all(ret_lt)
#       return res

    def add_distance_check(self, res, point1, point2):
        if res:
            a_distance = cal_two_point_distance(point1, point2)
            pylog.info("a_distance:%s" % a_distance)
            if a_distance > 10:
                return False
        return res

    def find_path(self, k, Tree_A, Tree_B):
        self.done = True
        self.Path = self.PATH(Tree_A, Tree_B)
        a_path = self.make_path(Tree_A, Tree_B)
        new_path = self.process_path(a_path)
        return new_path

    def plan_a_step(self, k, Tree_A, Tree_B, qrand):
        if self.EXTEND(Tree_A, qrand) != 'Trapped':
            qnew = self.qnew # get qnew from outside
            if self.CONNECT(Tree_B, qnew) == 'Reached':
                return True
        return False

    def get_path_from_tree(self, a_tree, a_qnew):
        a_path = []
        qnew = a_qnew
        while True:
            a_path.append(qnew)
            qnew = a_tree.Parent[qnew]
            if qnew == self.qinit:
                a_path.append(qnew)
                a_path.reverse()
                is_start = True
                return a_path, is_start

            if qnew == self.qgoal:
                a_path.append(qnew)
                a_path.pop(0)#pop first point
                is_start = False
                return a_path, is_start

    def make_path(self, tree_a, tree_b):
        qnew = self.qnew
        patha,is_starta = self.get_path_from_tree(tree_a, qnew)
        pathb,is_startb = self.get_path_from_tree(tree_b, qnew)

        a_path = []
        if is_starta:
            a_path.extend(patha)
            a_path.extend(pathb)
            return a_path

        if is_startb:
            a_path.extend(pathb)
            a_path.extend(patha)
            return a_path

    def _make_path_segment_from_tree(self, a_tree, qnew):
        a_path = []
        while True:
            a_path.append((a_tree.Parent[qnew], qnew))
            qnew = a_tree.Parent[qnew]
            if qnew == self.qinit or qnew == self.qgoal:
                break
        return a_path

    def PATH(self, tree_a, tree_b):
        qnew = self.qnew
        patha = self._make_path_segment_from_tree(tree_a, qnew)
        qnew = self.qnew
        pathb  = self._make_path_segment_from_tree(tree_b, qnew)
        return patha + pathb
