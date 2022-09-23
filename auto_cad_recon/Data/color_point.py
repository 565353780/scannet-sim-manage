#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.point import Point


class ColorPoint(Point):

    def __init__(self, x=0.0, y=0.0, z=0.0, r=255, g=255, b=255):
        super().__init__(x, y, z)
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def fromList(cls, xyzrgb_list):
        color_point = cls(xyzrgb_list[0], xyzrgb_list[1], xyzrgb_list[2],
                          xyzrgb_list[3], xyzrgb_list[4], xyzrgb_list)
        return color_point

    def toList(self):
        return [self.x, self.y, self.x, self.r, self.g, self.b]
