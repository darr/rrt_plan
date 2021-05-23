#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : utils_test.py
# Create date : 2021-05-12 20:33
# Modified date : 2021-05-14 00:40
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

from rrt.utils import cal_two_point_distance
from rrt.utils import cal_steer_point
from rrt import pylog

def test_cal_two_point_distance():
    p1 = (13.646141876174925, 11.09254347631764, 177.71424612217223)
    p2 = (9.969753836972952, 8.385700813800012, 170.5068815861147)
    a_distance = cal_two_point_distance(p1, p2)
    #print("%s dimention distance:%s" % (len(p1), a_distance))

    real_value = a_distance
    expect_value = 8.531642852934747 
    pylog.test_compare_data(real_value, expect_value)

def test_cal_two_point_distance1():
    p1 = (13.646141876174925, 11.09254347631764)
    p2 = (9.969753836972952, 8.385700813800012)
    a_distance = cal_two_point_distance(p1, p2)
    #print("%s dimention distance:%s" % (len(p1), a_distance))
    real_value = a_distance
    expect_value = 4.565394420464989
    pylog.test_compare_data(real_value, expect_value)

def test_cal_two_point_distance2():
    p1 = (13.646141876174925, 11.09254347631764, 177.71424612217223, 30.0)
    p2 = (9.969753836972952, 8.385700813800012, 170.5068815861147, 40.0)
    a_distance = cal_two_point_distance(p1, p2)

    real_value = a_distance
    expect_value = 13.144920302916734
    pylog.test_compare_data(real_value, expect_value)

def test_cal_two_point_distance0():
    p1 = (13.646141876174925, 11.09254347631764, 177.71424612217223)
    p2 = (9.969753836972952, 8.385700813800012, 170.5068815861147, 3.0)
    a_distance = cal_two_point_distance(p1, p2)
    print("%s dimention distance:%s" % (len(p1), a_distance))

def test_cal_steer_point():
    stepsize = 10
    origin_point = (5.0, 5.0, 160.0)
    target_point = (13.844806424319426, 1.6934513997232292, 186.04868908520777)
    new_point, distance = cal_steer_point(stepsize, origin_point, target_point)

    real_value = new_point
    expect_value = (8.192222165324328, 3.8066174400941932, 169.40135924815795)
    pylog.test_compare_data(real_value, expect_value)

    real_value = distance
    expect_value = 27.707364858237543
    pylog.test_compare_data(real_value, expect_value)

    #print("distances:%s" % str(distance))

def run_test():
    #test_cal_two_point_distance0()
    test_cal_two_point_distance()
    test_cal_two_point_distance1()
    test_cal_two_point_distance2()
    test_cal_steer_point()
