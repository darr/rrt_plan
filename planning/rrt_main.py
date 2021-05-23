#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : rrt_main.py
# Create date : 2021-05-09 20:09
# Modified date : 2021-05-21 02:06
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import time
import numpy as np
from planning.rrt.rrt_plan import rrt_plan

from planning.rrt.read_data import read_data
from planning.rrt.read_data import read_maps
from planning.rrt.plan_env import env
from planning.rrt.tree import Tree
from planning.rrt.utils import calculation
from planning.rrt import pylog
from planning.rrt.utils import cal_two_point_distance

def find_path(p, a_env):
    starttime = time.time()
    maxiter = 10000
    render_step = 1

    Tree_A = Tree(p.qinit)
    Tree_B = Tree(p.qgoal)
    for k in range(maxiter):

        qrand = a_env.random_sample()
        #pylog.info(qrand)
        #qrand = calculation(a_env, p, Tree_A, k)
        #pylog.info(qrand)
        ret = p.plan_a_step(k, Tree_A, Tree_B, qrand)
        Tree_A, Tree_B = Tree_B, Tree_A

        if (k % render_step == 0 and k != 0) or p.done:
            if a_env.render:
                a_env._render_a_step(Tree_A, Tree_B, k, p.Path)

        if ret:
            a_path = p.find_path(k, Tree_A, Tree_B)
            final_path = _get_final_path(a_path)
            pylog.info("iter:%s" % k)
            pylog.info('time used = ' + str((time.time() - starttime)) + ' s')
            if a_env.display_plan:
                a_env._render_a_step(Tree_A, Tree_B, k, p.Path, final_path=final_path, pause=300)
            return a_path

def _get_final_path(a_path):
    final_path = []

    for i in range(1,len(a_path)):
        a_point = a_path[i-1]
        next_point = a_path[i]
        final_path.append((a_point, next_point))
    return tuple(final_path)


def plan_a_path(mapinfo, length, width, height, start_point ,goal_point):
    a_dic = {}

    a_dic["mapinfo"] = mapinfo
    a_dic["length"] = length
    a_dic["width"] = width
    a_dic["height"] = height
    a_dic["render_step"] = 1
    #a_dic["stepsize"] = 0.5
    a_dic["stepsize"] = 3.0
    a_dic["display_plan"] = True #display final plan
    #a_dic["render"] = True #display plan process
    #a_dic["display_plan"] = False #display final plan
    a_dic["render"] = False #display plan process

    #a_dic["start"] = np.array([5.0, 5.0, 150.0])  #numpy.ndarray 3d
    #a_dic["goal"] = np.array([45.0, 50.0, 160.0]) #numpy.ndarray 3d
    a_dic["start"] = start_point  #numpy.ndarray 3d
    a_dic["goal"] = goal_point #numpy.ndarray 3d

    a_env = env(a_dic, xmax=width, ymax=length, zmax=height)
    a_dic["env"] = a_env

    p = rrt_plan(a_dic)

    a_path = find_path(p, a_env)
    return a_path
