#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : utils.py
# Create date : 2021-05-12 19:29
# Modified date : 2021-05-21 01:44
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import numpy as np
from . import pylog

def cal_steer_point(stepsize, origin_point, target_point):
    '''Obtain the direction of the sampling point, 
    and take the distance less than the step size to calculate the new point

    Args:
        stepsize: a float, e.g. 10
        origin_point: a point type tuple, e.g.  (5.0, 5.0, 160.0)
        target_point: a point type tuple, e.g.  (13.844806424319426, 1.6934513997232292, 186.04868908520777)

    Returns:
        new_point: apoint type tuple, e.g.  (5.063844443306486, 4.976132348801884, 160.18802718496315)
        distance: a float e.g.  27.707364858237543

    Raises:
        AssertionError:The two points are different in length.
        AssertionError:step size should be bigger than zero

    '''
    assert len(origin_point) == len(target_point)
    assert stepsize > 0.0

    if np.equal(origin_point, target_point).all():
        return origin_point, 0.0

    distance = cal_two_point_distance(target_point, origin_point)
    distance = cal_two_point_distance(origin_point, target_point)
    step = stepsize
    step = min(distance, step)

#   increment = ((target_point[0] - origin_point[0]) / distance * step,
#                (target_point[1] - origin_point[1]) / distance * step,
#                (target_point[2] - origin_point[2]) / distance * step)
#   pylog.info(increment)

    increment = tuple([ (i - j)/distance * step for i, j in zip(target_point, origin_point)])
#   pylog.info(increment)

    new_point = (origin_point[0] + increment[0], origin_point[1] + increment[1], origin_point[2] + increment[2])

#   pylog.info("origin_point:%s" % str(origin_point))
#   pylog.info("target_point:%s" % str(target_point))
#   pylog.info("new_point:%s" % str(new_point))
#   pylog.info("distance:%s" % str(distance))

    return new_point, distance

def cal_rotation_matrix(z_angle, y_angle, x_angle):
    # s angle: row; y angle: pitch; z angle: yaw
    # generate rotation matrix in SO3
    # RzRyRx = R, ZYX intrinsic rotation
    # also (r1,r2,r3) in R3*3 in {W} frame
    # used in obb.O
    # [[R p]
    # [0T 1]] gives transformation from body to world 
    return np.array([[np.cos(z_angle), -np.sin(z_angle), 0.0], [np.sin(z_angle), np.cos(z_angle), 0.0], [0.0, 0.0, 1.0]])@ \
           np.array([[np.cos(y_angle), 0.0, np.sin(y_angle)], [0.0, 1.0, 0.0], [-np.sin(y_angle), 0.0, np.cos(y_angle)]])@ \
           np.array([[1.0, 0.0, 0.0], [0.0, np.cos(x_angle), -np.sin(x_angle)], [0.0, np.sin(x_angle), np.cos(x_angle)]])


def cal_two_point_distance(point1, point2):
    """calculate two point distance

    Args:
        point1: a point, type tuple, e.g. (13.646141876174925, 11.09254347631764, 177.71424612217223)
        point2: a point, type tuple, e.g. (9.969753836972952, 8.385700813800012, 170.5068815861147)

    Returns:
        A floating point number that represents the distance.
        e.g. 8.531642852934747

    Raises:
        AssertionError:The two points are different in length.
    
    """
    assert len(point1) == len(point2)
    a_distance = np.sqrt(sum([(d1-d2)**2 for d1, d2 in zip(point1, point2)]))
    return a_distance

def random_sample(env):
    '''biased sampling'''
    while True:
        x = np.random.uniform(env.boundary[0:3], env.boundary[3:6])
        if check_is_outof_obstacles(env, x):
            return x

def calculation(a_env, alg, trees, k, bias = 0.1):
    '''
    引入重力 x3_1 = map(lambda x:x**2,x3)
    '''
    while True:
        x = np.random.uniform(a_env.plane_L, a_env.boundary[3:6])
        qnear = tuple(alg.NEAREST_NEIGHBOR(x, trees))

        if k%2 == 0:
            qgoal = a_env.boundary[3:6]
        else:
            qgoal = a_env.boundary[0:3]
        qnew = np.array(qnear) + 5*(x-qnear+0.2*(qgoal-qnear))/np.sqrt(np.sum((qgoal-qnear)**2))

        if check_is_outof_obstacles(a_env, qnew):
            return tuple(qnew)

def check_is_under_map(mapinfo, x):
    if mapinfo[int(x[0])][int(x[1])] > int(x[2]):
        return True

    return False

def check_is_above_map(mapinfo, x):
    if mapinfo[int(x[0])][int(x[1])] < int(x[2]):
        return True

    return False

def check_is_in_balls(a_env, a_point):
    for a_ball in a_env.balls:
        if check_is_in_ball(a_ball, a_point):
            return True

def check_is_in_ball(a_ball, a_point, factor = 0):
    #point1 = i[0:3]
    point1 = a_ball[0:3]
    point2 = a_point
    if cal_two_point_distance(point1, point2):
        return True
    return False

def check_is_outof_obstacles(env, x):
    mapinfo = env.mapinfo
    if check_is_under_map(mapinfo, x):
        return False

    return True

#def isinball(i, x, factor = 0):
def check_is_in_ball(i, x, factor = 0):
    if getDist(i[0:3], x) <= i[3] + factor:
        return True
    return False

#def isinobb(i, x, isarray = False):
def check_is_in_obb(i, x, isarray = False):
    # transform the point from {W} to {body}
    if isarray:
        pts = (i.T@np.column_stack((x, np.ones(len(x)))).T).T[:,0:3]
        block = [- i.E[0],- i.E[1],- i.E[2],+ i.E[0],+ i.E[1],+ i.E[2]]
        #return isinbound(block, pts, isarray = isarray)
        return check_is_in_bound(block, pts, isarray = isarray)
    else:
        pt = i.T@np.append(x,1)
        block = [- i.E[0],- i.E[1],- i.E[2],+ i.E[0],+ i.E[1],+ i.E[2]]
        #return isinbound(block, pt)
        return check_is_in_bound(block, pt)

def check_is_in_bound(i, x, mode = False, factor = 0, isarray = False):
    if mode == 'obb':
        #return isinobb(i, x, isarray)
        return check_is_in_obb(i, x, isarray)
    if isarray:
        compx = (i[0] - factor <= x[:,0]) & (x[:,0] < i[3] + factor) 
        compy = (i[1] - factor <= x[:,1]) & (x[:,1] < i[4] + factor) 
        compz = (i[2] - factor <= x[:,2]) & (x[:,2] < i[5] + factor) 
        return compx & compy & compz
    else:    
        return i[0] - factor <= x[0] < i[3] + factor and i[1] - factor <= x[1] < i[4] + factor and i[2] - factor <= x[2] < i[5]

def modify_lineAABB(p0, p1, dist, mapinfo):
    # https://www.gamasutra.com/view/feature/131790/simple_intersection_tests_for_games.php?print=1
    # aabb should have the attributes of P, E as center point and extents
    if p0 == p1: return False

    mid = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2]  # mid point 临近点和目标点中间的点，叫中点
    I = [(p1[0] - p0[0]) / dist, (p1[1] - p0[1]) / dist, (p1[2] - p0[2]) / dist]  # unit direction 临近点朝目标点的方向（单位向量）
    hl = dist / 2  # radius
    #pylog.info(p0)
    #pylog.info(p1)

    for i in range(int(dist)):
        x_pos, y_pos, z_pos = p0[0]+I[0]*i, p0[1]+I[1]*i, p0[2]+I[2]*i
        if z_pos < mapinfo[int(x_pos)][int(y_pos)]: return True
    x_pos, y_pos, z_pos = p0[0]+I[0]*dist, p0[1]+I[1]*dist, p0[2]+I[2]*dist
    #pylog.info("x_pos:%s y_pos:%s" % (x_pos, y_pos))
    if z_pos < mapinfo[int(x_pos)][int(y_pos)]: return True
    return False

def lineSphere(p0, p1, ball):
    # https://cseweb.ucsd.edu/classes/sp19/cse291-d/Files/CSE291_13_CollisionDetection.pdf
    c, r = ball[0:3], ball[-1]
    line = [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]]
    d1 = [c[0] - p0[0], c[1] - p0[1], c[2] - p0[2]]
    t = (1 / (line[0] * line[0] + line[1] * line[1] + line[2] * line[2])) * (
                line[0] * d1[0] + line[1] * d1[1] + line[2] * d1[2])
    if t <= 0:
        if (d1[0] * d1[0] + d1[1] * d1[1] + d1[2] * d1[2]) <= r ** 2: return True #方向相反，节点在球里
    elif t >= 1:
        d2 = [c[0] - p1[0], c[1] - p1[1], c[2] - p1[2]]
        if (d2[0] * d2[0] + d2[1] * d2[1] + d2[2] * d2[2]) <= r ** 2: return True #方向相同，新节点在球里
    elif 0 < t < 1:
        x = [p0[0] + t * line[0], p0[1] + t * line[1], p0[2] + t * line[2]]
        k = [c[0] - x[0], c[1] - x[1], c[2] - x[2]]
        if (k[0] * k[0] + k[1] * k[1] + k[2] * k[2]) <= r ** 2: return True #方向相同，新节点在球里
    return False

def lineOBB(p0, p1, dist, obb):
    # transform points to obb frame
    res = obb.T@np.column_stack([np.array([p0,p1]),[1,1]]).T 
    # record old position and set the position to origin
    oldP, obb.P= obb.P, [0,0,0] 
    # calculate segment-AABB testing
    ans = lineAABB(res[0:3,0],res[0:3,1],dist,obb)
    # reset the position
    obb.P = oldP 
    return ans

def lineAABB(p0, p1, dist, aabb):
    # https://www.gamasutra.com/view/feature/131790/simple_intersection_tests_for_games.php?print=1
    # aabb should have the attributes of P, E as center point and extents
    mid = [(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, (p0[2] + p1[2]) / 2]  # mid point 临近点和目标点中间的点，叫中点
    I = [(p1[0] - p0[0]) / dist, (p1[1] - p0[1]) / dist, (p1[2] - p0[2]) / dist]  # unit direction 临近点朝目标点的方向（单位向量）
    hl = dist / 2  # radius
    T = [aabb.P[0] - mid[0], aabb.P[1] - mid[1], aabb.P[2] - mid[2]]    #障碍物中心点和中点的偏差（向量）
    # do any of the principal axis form a separting axis?
    if abs(T[0]) > (aabb.E[0] + hl * abs(I[0])): return False   #轨迹是否与障碍物有交点
    if abs(T[1]) > (aabb.E[1] + hl * abs(I[1])): return False
    if abs(T[2]) > (aabb.E[2] + hl * abs(I[2])): return False

    #下面没看懂，注释了
    # # I.cross(s axis) ?
    # r = aabb.E[1] * abs(I[2]) + aabb.E[2] * abs(I[1])
    # if abs(T[1] * I[2] - T[2] * I[1]) > r: return False
    # # I.cross(y axis) ?
    # r = aabb.E[0] * abs(I[2]) + aabb.E[2] * abs(I[0])
    # if abs(T[2] * I[0] - T[0] * I[2]) > r: return False
    # # I.cross(z axis) ?
    # r = aabb.E[0] * abs(I[1]) + aabb.E[1] * abs(I[0])
    # if abs(T[0] * I[1] - T[1] * I[0]) > r: return False

    return True

def check_is_collision(env, x, child, dist=None):
    '''see if line intersects obstacle'''
    '''specified for expansion in A* 3D lookup table'''
    # if collide, then return true
    if dist==None:
        dist = cal_two_point_distance(x, child)

    # check in bound
    if  not check_is_in_bound(env.boundary, child): 
        return True, dist

    # check collision in ball
    for a_ball in env.balls:
        if lineSphere(x, child, a_ball): 
            return True, dist

    if modify_lineAABB(x, child, dist, env.mapinfo): 
            return True, dist

    #check collision in AABB
    for i in range(len(env.AABB)):
        if lineAABB(x, child, dist, env.AABB[i]): 
            return True, dist

    # check collision with obb
    for i in env.OBB:
        if lineOBB(x, child, dist, i):
            return True, dist

    return False, dist
