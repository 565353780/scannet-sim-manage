#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.frame_object import FrameObject


class SceneObject(object):

    def __init__(self, object_label):
        self.object_label = object_label
        self.frame_object_list = []

    def addFrameObject(self, color_point_set, image):
        self.frame_object_list.append(FrameObject(color_point_set, image))
        return True
