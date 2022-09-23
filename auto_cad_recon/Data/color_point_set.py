#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class ColorPointSet(object):

    def __init__(self, color_point_list=[]):
        self.color_point_list = color_point_list
        return

    def reset(self):
        self.color_point_list = []

    def toArray(self):
        color_point_array = np.array(color_point.toList()
                                     for color_point in self.color_point_list)
        points = color_point_array[:, :3]
        colors = color_point_array[:, 3:] / 255.0
        return points, colors

    def addColorPoint(self, color_point):
        self.color_point_list.append(color_point)
