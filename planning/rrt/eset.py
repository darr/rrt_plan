#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : eset.py
# Create date : 2021-05-13 01:29
# Modified date : 2021-05-13 01:30
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

class edgeset(object):
    def __init__(self):
        self.E = {}

    def add_edge(self, edge):
        x, y = edge[0], edge[1]
        if x in self.E:
            self.E[x].add(y)
        else:
            self.E[x] = set()
            self.E[x].add(y)

    def remove_edge(self, edge):
        x, y = edge[0], edge[1]
        self.E[x].remove(y)

    def get_edge(self, nodes = None):
        edges = []
        if nodes is None:
            for v in self.E:
                for n in self.E[v]:
                    # if (n,v) not in edges:
                    edges.append((v, n))
        else: 
            for v in nodes:
                for n in self.E[tuple(v)]:
                    edges.append((v, n))
        return edges

    def isEndNode(self, node):
        return node not in self.E
