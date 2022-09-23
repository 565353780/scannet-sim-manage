#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.color_point_set import ColorPointSet

class FrameObject(object):
    def __init__(self, color_point_set=ColorPointSet(), image):
        self.color_point_set = color_point_set
        self.image = image
        return
