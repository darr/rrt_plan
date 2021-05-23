#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : rrt_main.py
# Create date : 2021-05-09 20:09
# Modified date : 2021-05-21 02:33
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import time
import numpy as np
from planning.rrt.read_data import read_data
from planning.rrt.read_data import read_maps
from planning.rrt_main import plan_a_path
from planning.rrt import pylog

def run():
    #data_path = 'planning/rrt_3D/altitude.txt'
    data_path = 'planning/rrt/maps/altitude.txt'
    mapinfo, length, width, height = read_data(data_path)
    start_point = np.array([5.0, 5.0, 160.0])  #numpy.ndarray 3d
    pylog.info("start point:%s" % str(start_point))
    goal_point  = np.array([15.0, 12.0, 180.0]) #numpy.ndarray 3d
    pylog.info("goal point:%s" % str(goal_point))

    a_path = plan_a_path(mapinfo, length, width, height, start_point ,goal_point)
    #pylog.info(a_path)

def run2():
    #data_path = 'planning/rrt/maps/map1.txt'
    #data_path = 'planning/rrt/maps/map2.txt'
    #data_path = 'planning/rrt/maps/map3.txt'
    #data_path = 'planning/rrt/maps/map4.txt'
    #data_path = 'planning/rrt/maps/map5.txt'
    #data_path = 'planning/rrt/maps/map6.txt'
    #data_path = 'planning/rrt/maps/map7.txt'
    #data_path = 'planning/rrt/maps/map_obstacle.txt'
    #data_path = 'planning/rrt/maps/map_obstacle2.txt'
    data_path = 'planning/rrt/maps/map_obstacle3.txt'
    mapinfo, length, width, height = read_maps(data_path)
    start_point = np.array([5.0, 5.0, 160.0])  #numpy.ndarray 3d
    pylog.info("start point:%s" % str(start_point))
    goal_point  = np.array([35.0, 35.0, 180.0]) #numpy.ndarray 3d
    pylog.info("goal point:%s" % str(goal_point))

    a_path = plan_a_path(mapinfo, length, width, height, start_point ,goal_point)

#run()
run2()
