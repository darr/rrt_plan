#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : cal_point.py
# Create date : 2021-05-16 05:47
# Modified date : 2021-05-16 20:34
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

def get_check_point_list_from_two_point(item):
    #check is same point
    check_point_lt = []
    if item[0][0] == item[1][0] and item[0][1] == item[1][1]:
        return check_point_lt

    if item[0][0] == item[1][0]:
        # x is same
        #point from (y1, y2), except for y1 and y2
        y1 = min(item[0][1], item[1][1])
        y2 = max(item[0][1], item[1][1])
        for a_y in range(y1+1,y2):
            a_point = (item[0][0], a_y)
            check_point_lt.append(a_point)
        return check_point_lt

    if item[0][1] == item[1][1]:
        # y is same
        # point for (x1, x2), except for x1 and x2
        x1 = min(item[0][0], item[1][0])
        x2 = max(item[0][0], item[1][0])

        for a_x in range(x1+1, x2):
            a_point = (a_x, item[0][1])
            check_point_lt.append(a_point)
        return check_point_lt

    a_lt = get_point_list(item)
    check_point_lt.extend(a_lt)
    return check_point_lt

def get_point_list(item):
    x1 = item[0][0]
    y1 = item[0][1]
    x2 = item[1][0]
    y2 = item[1][1]

    A,B,C = GeneralEquation1(x1, y1, x2, y2)
    
    # y = kx + b
    k, b = GeneralEquation2(x1,y1,x2,y2)
    x1 = min(item[0][0], item[1][0])
    x2 = max(item[0][0], item[1][0])
    x_lt = []
    for a_x in range(x1+1, x2):
        a_y = k * a_x + b
        #a_point = (a_x ,a_y)
        a_point = (int(a_x), int(a_y))
        x_lt.append(a_point)

    #print("x_lt:%s" % x_lt)

    # x = ky + b
    k, b = GeneralEquation2(y1,x1,y2,x2)
    y1 = min(item[0][1], item[1][1])
    y2 = max(item[0][1], item[1][1])
    y_lt = []
    for a_y in range(y1+1, y2):
        a_x = k * a_y + b
        #a_point = (a_x, a_y)
        a_point = (int(a_x), int(a_y))
        y_lt.append(a_point)
    #print("y_lt:%s" % y_lt)
    ret_lt = []
    ret_lt.extend(x_lt)
    ret_lt.extend(y_lt)
    ret = list(set(ret_lt))
    #for a_point in a_set:
    #    print(a_point)
    return ret

def GeneralEquation1(first_x,first_y,second_x,second_y):
    # 一般式 Ax+By+C=0
    A = second_y-first_y
    B = first_x-second_x
    C = second_x*first_y-first_x*second_y
    #print("%sx+%sy+%s=0" % (A, B, C))
    return A, B, C


def GeneralEquation2(first_x,first_y,second_x,second_y):
    #截距式方程的y=kx+b
    A = second_y-first_y
    B = first_x-second_x
    C = second_x*first_y-first_x*second_y
    k = -1 * A / B
    b = -1 * C / B

    #print("y=%sx+%s" % (k,b))
    return k, b

#   item = ((1,1),(6,3))

#   ret = get_check_point_list_from_two_point(item)
#   for a_point in ret:
#       print(a_point)



