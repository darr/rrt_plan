#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################
# File name : node.py
# Create date : 2021-05-13 01:25
# Modified date : 2021-05-13 01:25
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
#####################################

#------------------------ use a linked list to express the tree 
class Node:
    def __init__(self, data):
        self.pos = data
        self.Parent = None
        self.child = set()

