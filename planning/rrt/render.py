#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : render.py
# Create date : 2021-05-21 01:02
# Modified date : 2021-05-21 01:51
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import mpl_toolkits.mplot3d as plt3d
from mpl_toolkits.mplot3d import proj3d
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def draw_block_list(ax, blocks, color=None, alpha=0.15):
    '''
    drawing the blocks on the graph
    '''
    v = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]],
                 dtype='float')
    f = np.array([[0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7], [0, 1, 2, 3], [4, 5, 6, 7]])
    n = blocks.shape[0]
    d = blocks[:, 3:6] - blocks[:, :3]
    vl = np.zeros((8 * n, 3))
    fl = np.zeros((6 * n, 4), dtype='int64')
    for k in range(n):
        vl[k * 8:(k + 1) * 8, :] = v * d[k] + blocks[k, :3]
        fl[k * 6:(k + 1) * 6, :] = f + k * 8
    if type(ax) is Poly3DCollection:
        ax.set_verts(vl[fl])
    else:
        #h = ax.add_collection3d(Poly3DCollection(vl[fl], facecolors='black', alpha=alpha, linewidths=1, edgecolors='k'))
        h = ax.add_collection3d(Poly3DCollection(vl[fl],  alpha=alpha, linewidths=1, edgecolors='k'))
        return h

def obb_verts(obb):
    # 0.017004013061523438 for 1000 iters
    ori_body = np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1], \
                         [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, -1]])
    # P + (ori * E)
    ori_body = np.multiply(ori_body, obb.E)
    # obb.O is orthornormal basis in {W}, aka rotation matrix in SO(3)
    verts = (obb.O @ ori_body.T).T + obb.P
    return verts

def draw_obb(ax, OBB, color=None, alpha=0.15):
    f = np.array([[0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7], [0, 1, 2, 3], [4, 5, 6, 7]])
    n = OBB.shape[0]
    vl = np.zeros((8 * n, 3))
    fl = np.zeros((6 * n, 4), dtype='int64')
    for k in range(n):
        vl[k * 8:(k + 1) * 8, :] = obb_verts(OBB[k])
        fl[k * 6:(k + 1) * 6, :] = f + k * 8
    if type(ax) is Poly3DCollection:
        ax.set_verts(vl[fl])
    else:
        h = ax.add_collection3d(Poly3DCollection(vl[fl], facecolors='black', alpha=alpha, linewidths=1, edgecolors='k'))
        return h

def draw_map(ax, mapinfo):
    '''
    drawing the map
    '''
    length, width = mapinfo.shape[1], mapinfo.shape[0] #源数据，列，行，海拔最大值
    X=np.linspace(0,width,width)
    Y=np.linspace(0,length,length)
    X, Y = np.meshgrid(X, Y)    # x-y 平面的网格
    Z=mapinfo
    #plot_wireframe plot_surface
    ax.plot_surface(X, Y, Z.T, rstride=1, cstride=1, cmap=plt.get_cmap('Greens'), antialiased=True)#rainbow

    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    #ax.contourf(X,Y,Z,zdir='z',offset=-2)


def make_transparent(ax):
    # make the panes transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

def draw_line(ax, SET, visibility=1, color=None):
    if SET != []:
        for i in SET:
            xs = i[0][0], i[1][0]
            ys = i[0][1], i[1][1]
            zs = i[0][2], i[1][2]
            line = plt3d.art3d.Line3D(xs, ys, zs, alpha=visibility, color=color)
            ax.add_line(line)


def create_a_sphere(center, r):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    x, y, z = r * x + center[0], r * y + center[1], r * z + center[2]
    return (x, y, z)


def _draw_spheres(ax, balls):
    for i in balls:
        (xs, ys, zs) = create_a_sphere(i[0:3], i[-1])
        ax.plot_wireframe(xs, ys, zs, alpha=0.15, color="b")

#----------RRT connect algorithm        
def render_a_step(tree_a, tree_b, index, Path, env, final_path=None, pause=0.01):
    start = env.start
    goal = env.goal

    a_edges = _get_edges(tree_a)
    b_edges = _get_edges(tree_b)

    ax = plt.subplot(111, projection='3d')
    ax.view_init(elev=90., azim=0.)
    ax.clear()
    _draw_env(ax, env)

    _draw_paths(ax, a_edges, b_edges, Path, final_path)
    ax.plot(start[0:1], start[1:2], start[2:], 'go', markersize=10, markeredgecolor='k')#markersize=7
    ax.plot(goal[0:1], goal[1:2], goal[2:], 'ro', markersize=10, markeredgecolor='k')#markersize=7
    #set_axes_equal(ax)
    make_transparent(ax)
    ax.set_zlim(0, 500)
    #ax.set_axis_off()
    plt.pause(pause)

def _get_edges(a_tree):
    edges = []
    for i in a_tree.Parent:
        edges.append([i, a_tree.Parent[i]])
    return edges

def _draw_env(ax, env):
    mapinfo = env.mapinfo
    draw_map(ax, mapinfo)
    #_draw_spheres(ax, env.balls)
    #draw_block_list(ax, env.blocks, alpha=0.5)
    #if env.OBB is not None:
    #    draw_obb(ax, env.OBB)

def _draw_paths(ax, a_edges, b_edges, Path, final_path=None):
    draw_line(ax, a_edges, visibility=0.75, color='r') # g
    draw_line(ax, b_edges, visibility=0.75, color='y')
    draw_line(ax, Path, color='k') #r
    if final_path:
        draw_line(ax, final_path, color='g') #r
