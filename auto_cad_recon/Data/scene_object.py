#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.frame_object import FrameObject


class SceneObject(object):

    def __init__(self, object_label):
        self.object_label = object_label
        self.frame_object_dict = {}
        return

    def reset(self):
        self.object_label = "Unknown"
        del self.frame_object_dict
        self.frame_object_dict = {}
        return True

    def addFrameObject(self, frame_idx, point_image, label, value=True):
        self.frame_object_dict[str(frame_idx)] = FrameObject(
            point_image, label, value)
        return True

    def getFrameObject(self, frame_idx):
        if str(frame_idx) not in self.frame_object_dict.keys():
            print("[WARN][SceneObject::getFrameObject]")
            print("\t this frame_idx [" + frame_idx + "] not exist!")
            return None

        return self.frame_object_dict[str(frame_idx)]
