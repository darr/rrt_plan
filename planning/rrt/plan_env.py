#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : plan_env.py
# Create date : 2021-05-20 23:09
# Modified date : 2021-05-21 01:52
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

from .obb import obb
from . import pylog
import numpy as np

from .env_utils import R_matrix
from .env_utils import getblocks
from .env_utils import getAABB
from .env_utils import getAABB2
from .env_utils import add_block

from .render import render_a_step
from .utils import check_is_collision

from .utils import cal_steer_point

def get_goal_obstacle_ball():
    spheres = [[10.0,12.0,300,3.0],[16.0,12.0,400,2],[30.0,30.0,180,4.0]] 
    Obstacles = []
    for i in spheres:
        Obstacles.append([j for j in i])
    return np.array(Obstacles)

class env():
    def __init__(self, a_dic, xmin=0, ymin=0, zmin=0, xmax=30, ymax=30, zmax=255, resolution=1):
    # def __init__(self, xmin=-5, ymin=0, zmin=-5, xmax=10, ymax=5, zmax=10, resolution=1):  
        self.resolution = resolution
        self.boundary = np.array([xmin, ymin, zmin, xmax, ymax, zmax])

        self.blocks = getblocks()
    
        self.AABB = getAABB2(self.blocks)
        self.AABB_pyrr = getAABB(self.blocks)

        #self.balls = getballs()
        self.balls = get_goal_obstacle_ball()

        self.OBB = np.array([obb([5.0,7.0,2.5],[0.5,2.0,2.5],R_matrix(135,0,0)),
                             obb([12.0,4.0,2.5],[0.5,2.0,2.5],R_matrix(45,0,0))])
        self.start = a_dic["start"] #numpy.ndarray 3d
        self.goal = a_dic["goal"] #numpy.ndarray 3d
        self.current_start = self.start
        self.current_goal = self.goal

        self.mapinfo = a_dic["mapinfo"]
        self.t = 0 # time 

        self.plane_L= self.boundary[0:3]
        self.plane_L[2] = min(self.start[2]-1, self.goal[2]-1) # 飞机高度限制

        self.render = a_dic["render"]
        self.display_plan = a_dic["display_plan"]

    def reset(self):
        '''
        重置环境的状态，返回观测
        reset env state, return observation
        '''
        pylog.info("run reset")
        self.current_start = self.start
        self.current_goal = self.goal

        observation = self._get_observation()
        return observation

    def _get_observation(self):
        '''

        '''
        observation = [self.current_start, self.current_goal]
        return observation

    def random_sample(self):
        ret = self._random_sample()
        return tuple(ret)

    def check_is_under_map(self, mapinfo, x):
        if mapinfo[int(x[0])][int(x[1])] > int(x[2]):
            return False

        return True

    def check_is_in_obstacle(self, x):
        if self.check_is_under_map(self.mapinfo, x):
            return True

        return False

    def check_is_collision(self, qnear, qnew, dist):

        collide, _ = check_is_collision(self, qnear, qnew, dist = dist)
        return collide, _

    def cal_steer_point(self, stepsize, qnear, q):
        qnew, dist = cal_steer_point(stepsize, qnear, q)
        return qnew, dist

    def _random_sample(self):
        '''biased sampling'''
        while True:
            x = np.random.uniform(self.boundary[0:3], self.boundary[3:6])
            if self.check_is_in_obstacle(x):
                return x

    def _get_reward(self):
        return 0.1

    def step(self, action):
        pylog.info("run a step")
        obs = self._get_observation()
        reward = self._get_reward()
        done = False
        info = ""
        return observation, reward, done, info

    def _render_a_step(self, tree_a, tree_b, index, Path, final_path=None, pause=0.01):
        render_a_step(tree_a, tree_b, index, Path, self, final_path=final_path, pause=pause)

    def New_block(self):
        newblock = add_block()
        self.blocks = np.vstack([self.blocks,newblock])
        self.AABB = getAABB2(self.blocks)
        self.AABB_pyrr = getAABB(self.blocks)

    def move_start(self, x):
        self.start = x

    def move_block(self, a = [0,0,0], s = 0, v = [0.1,0,0], block_to_move = 0, mode = 'translation'):
        # t is time , v is velocity in R3, a is acceleration in R3, s is increment ini time, 
        # R is an orthorgonal transform in R3*3, is the rotation matrix
        # (s',t') = (s + tv, t) is uniform transformation
        # (s',t') = (s + a, t + s) is a translation
        if mode == 'translation':
            ori = np.array(self.blocks[block_to_move])
            self.blocks[block_to_move] = \
                np.array([ori[0] + a[0],\
                    ori[1] + a[1],\
                    ori[2] + a[2],\
                    ori[3] + a[0],\
                    ori[4] + a[1],\
                    ori[5] + a[2]])

            self.AABB[block_to_move].P = \
            [self.AABB[block_to_move].P[0] + a[0], \
            self.AABB[block_to_move].P[1] + a[1], \
            self.AABB[block_to_move].P[2] + a[2]]
            self.t += s
            # return a range of block that the block might moved
            a = self.blocks[block_to_move]
            return np.array([a[0] - self.resolution, a[1] - self.resolution, a[2] - self.resolution, \
                            a[3] + self.resolution, a[4] + self.resolution, a[5] + self.resolution]), \
                    np.array([ori[0] - self.resolution, ori[1] - self.resolution, ori[2] - self.resolution, \
                            ori[3] + self.resolution, ori[4] + self.resolution, ori[5] + self.resolution])
            # return a,ori
        # (s',t') = (Rx, t)
    def move_OBB(self, obb_to_move = 0, theta=[0,0,0], translation=[0,0,0]):
    # theta stands for rotational angles around three principle axis in world frame
    # translation stands for translation in the world frame
        ori = [self.OBB[obb_to_move]]
        # move obb position
        self.OBB[obb_to_move].P = \
            [self.OBB[obb_to_move].P[0] + translation[0], 
            self.OBB[obb_to_move].P[1] + translation[1], 
            self.OBB[obb_to_move].P[2] + translation[2]]
        # Calculate orientation
        self.OBB[obb_to_move].O = R_matrix(z_angle=theta[0],y_angle=theta[1],x_angle=theta[2])
        # generating transformation matrix
        self.OBB[obb_to_move].T = np.vstack([np.column_stack([self.OBB[obb_to_move].O.T,\
            -self.OBB[obb_to_move].O.T@self.OBB[obb_to_move].P]),[translation[0],translation[1],translation[2],1]])
        return self.OBB[obb_to_move], ori[0]
          
if __name__ == '__main__':
    newenv = env()
