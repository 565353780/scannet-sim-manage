#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scannet_sim_manage.Data.point import Point


class BBox(object):

    def __init__(self, min_point=Point(), max_point=Point()):
        self.min_point = min_point
        self.max_point = max_point
        return

    @classmethod
    def fromList(cls, bbox_list):
        bbox = cls(Point.fromList(bbox_list[0]), Point.fromList(bbox_list[1]))
        return bbox

    def toList(self):
        return [self.min_point.toList(), self.max_point.toList()]

    def isInBBox(self, point):
        if point.x < self.min_point.x or point.x > self.max_point.x:
            return False
        if point.y < self.min_point.y or point.y > self.max_point.y:
            return False
        if point.z < self.min_point.z or point.z > self.max_point.z:
            return False
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[BBox]")
        print(line_start + "\t min_point:")
        self.min_point.outputInfo(info_level + 1)
        print(line_start + "\t max_point:")
        self.max_point.outputInfo(info_level + 1)
        return True
