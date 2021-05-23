#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : tree.py
# Create date : 2021-05-09 19:48
# Modified date : 2021-05-09 19:53
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

class Tree():

    def __init__(self, node):
        self.V = []
        self.Parent = {}
        self.V.append(node)

    def add_vertex(self, node):
        if node not in self.V:
            self.V.append(node)

    def add_edge(self, parent, child):
        self.Parent[child] = parent

