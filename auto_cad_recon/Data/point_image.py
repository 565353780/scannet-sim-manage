#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import randint

from auto_cad_recon.Method.depth import getPointArray


class PointImage(object):

    def __init__(self, observations=None, agent_state=None):
        self.image = None
        self.depth = None
        self.point_array = None
        self.camera_point = None
        self.label_dict_list = []

        if observations is not None and agent_state is not None:
            self.loadObservations(observations, agent_state)
        return

    def loadObservations(self, observations, agent_state):
        self.image = observations["color_sensor"][..., :3][..., ::-1]
        self.depth = observations["depth_sensor"]
        self.point_array, self.camera_point = getPointArray(
            observations, agent_state)
        self.label_dict_list = [{} for _ in self.point_array]

        match_x_idx = np.where(self.point_array[:,
                                                0] == self.camera_point[0])[0]
        match_x_point_array = self.point_array[match_x_idx]

        x_match_y_idx = np.where(
            match_x_point_array[:, 1] == self.camera_point[1])[0]
        match_xy_idx = match_x_idx[x_match_y_idx]
        match_xy_point_array = self.point_array[match_xy_idx]

        xy_match_z_idx = np.where(
            match_xy_point_array[:, 2] == self.camera_point[2])[0]
        match_xyz_idx = match_xy_idx[xy_match_z_idx]

        self.point_array[match_xyz_idx] = [
            float("inf"), float("inf"),
            float("inf")
        ]

        for empty_idx in match_xyz_idx:
            self.addLabel(empty_idx, "empty")
        return True

    def getArrayIdx(self, pixel_idx):
        assert self.image is not None
        return pixel_idx[0] * self.image.shape[1] + pixel_idx[1]

    def getPixelIdx(self, array_idx):
        assert self.image is not None
        return [
            int(array_idx / self.image.shape[1]),
            array_idx % self.image.shape[1]
        ]

    def addLabel(self, array_idx, label, value=True):
        assert self.image is not None
        assert array_idx < len(self.point_array)
        assert "empty" not in self.label_dict_list[array_idx].keys()
        self.label_dict_list[array_idx][label] = value
        return True

    def getLabelImage(self, label, value=True):
        label_image = np.ones(self.image.shape, dtype=np.uint8) * 255

        for i, label_dict in enumerate(self.label_dict_list):
            label_dict = self.label_dict_list[i]
            if label not in label_dict.keys():
                continue
            if label_dict[label] != value:
                continue
            pixel_idx = self.getPixelIdx(i)
            label_image[pixel_idx[0], pixel_idx[1], :] = \
                self.image[pixel_idx[0],  pixel_idx[1], :]
        return label_image

    def getAllLabelImage(self):
        all_label_image = np.ones(self.image.shape, dtype=np.uint8) * 255

        background_color = [0, 0, 0]

        label_list = []
        value_list = []
        color_list = []
        for label_dict in self.label_dict_list:
            if "empty" in label_dict.keys():
                continue
            for label, value in label_dict.items():
                if label in label_list or \
                        label == "background" or \
                        value not in ["object", True]:
                    continue

                label_list.append(label)
                value_list.append(value)
                color_list.append(
                    [randint(0, 255),
                     randint(0, 255),
                     randint(0, 255)])

        for i, label_dict in enumerate(self.label_dict_list):
            label_dict = self.label_dict_list[i]

            if "empty" in label_dict.keys():
                continue

            if "background" in label_dict.keys():
                pixel_idx = self.getPixelIdx(i)
                all_label_image[pixel_idx[0], pixel_idx[1], :] = \
                    background_color
                continue

            for j, [label, value] in enumerate(zip(label_list, value_list)):
                if label not in label_dict.keys():
                    continue
                if label_dict[label] != value:
                    continue
                if value not in ["object", True]:
                    continue
                pixel_idx = self.getPixelIdx(i)
                all_label_image[pixel_idx[0], pixel_idx[1], :] = \
                    color_list[j]
                break
        return all_label_image
