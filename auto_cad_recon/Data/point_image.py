#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from auto_cad_recon.Method.depth import getPointArray


class PointImage(object):

    def __init__(self, observations=None, agent_state=None):
        self.image = None
        self.point_array = None
        self.label_dict_list = []

        if observations is not None and agent_state is not None:
            self.loadObservations(observations, agent_state)
        return

    def loadObservations(self, observations, agent_state):
        self.image = observations["color_sensor"][..., :3]
        self.point_array = getPointArray(observations, agent_state)
        self.label_dict_list = [{} for _ in self.point_array]
        return True

    def getArrayIdx(self, pixel_idx):
        assert self.image is not None
        return pixel_idx[0] * self.image.shape[0] + pixel_idx[1]

    def getPixelIdx(self, array_idx):
        assert self.image is not None
        return [
            int(array_idx / self.image.shape[0]),
            array_idx % self.image.shape[0]
        ]

    def addLabel(self, array_idx, label, value=True):
        assert self.image is not None
        assert array_idx < len(self.point_array)
        self.label_dict_list[array_idx][label] = value
        return True

    def getLabelImage(self, label, value=True):
        label_image = np.zeros(self.image.shape, dtype=np.uint8)

        for i, label_dict in enumerate(self.label_dict_list):
            label_dict = self.label_dict_list[i]
            if label not in label_dict.keys():
                continue
            if label_dict[label] != value:
                continue
            pixel_idx = self.getPixelIdx(i)
            label_image[pixel_idx[0]][pixel_idx[1]] = self.image[pixel_idx[0]][
                pixel_idx[1]]
        return label_image
