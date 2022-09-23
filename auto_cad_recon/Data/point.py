#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Point(object):

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
        return

    @classmethod
    def fromList(cls, xyz_list):
        point = cls(xyz_list[0], xyz_list[1], xyz_list[2])
        return point

    def toList(self):
        return [self.x, self.y, self.z]
