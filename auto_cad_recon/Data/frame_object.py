#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Config.depth import INF_POINT

class FrameObject():

    def __init__(self, point_image=None, label=None, value=True):
        self.image = None
        self.depth = None
        self.point_array = []
        self.camera_point = None
        self.bbox_2d = None
        self.label_dict_list = []

        if point_image is not None and label is not None:
            self.generateData(point_image, label, value)
        return

    def generateData(self, point_image, label, value=True):
        self.image = point_image.getLabelRGB(label, value)

        self.depth = point_image.getLabelDepth(label, value)

        self.camera_point = point_image.camera_point

        assert label in point_image.bbox_2d_dict.keys()
        self.bbox_2d = point_image.bbox_2d_dict[label]

        for i, label_dict in enumerate(point_image.label_dict_list):
            if label not in label_dict.keys():
                self.point_array.append(INF_POINT)
                self.label_dict_list.append({})
                continue
            if label_dict[label] != value:
                self.point_array.append(INF_POINT)
                self.label_dict_list.append({})
                continue
            self.point_array.append(point_image.point_array[i])
            self.label_dict_list.append(point_image.label_dict_list[i])
        return True
