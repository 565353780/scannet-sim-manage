#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from copy import deepcopy


def drawBBox(image, bbox):
    x_min, y_min, _ = bbox.min_point.toList()
    x_max, y_max, _ = bbox.max_point.toList()

    cv2.rectangle(image, (y_min, x_min), (y_max, x_max), (0, 0, 255), 2)
    return True


def saveLabelImages(point_image, save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)

    cv2.imwrite(save_folder_path + "image.png", point_image.image)
    cv2.imwrite(save_folder_path + "depth.png", point_image.depth)

    all_label_mask = point_image.getAllLabelMask()
    np.save(save_folder_path + "all_label_mask.npy", all_label_mask)
    all_label_render = point_image.getAllLabelRender()
    cv2.imwrite(save_folder_path + "all_label_render.png", all_label_render)

    label_list = []
    value_list = []
    for label_dict in point_image.label_dict_list:
        for label, value in label_dict.items():
            if label == "empty" or \
                    label in label_list or \
                    value not in ["object", True]:
                continue

            label_list.append(label)
            value_list.append(value)

    for label, value in zip(label_list, value_list):
        rgb = point_image.getLabelRGB(label, value)
        depth = point_image.getLabelDepth(label, value)

        if label not in ["background"]:
            bbox = point_image.bbox_2d_dict[label]

            drawBBox(rgb, bbox)
            drawBBox(depth, bbox)

        if "." in label:
            label = label.split(".")[0]
        cv2.imwrite(save_folder_path + label + "_rgb.png", rgb)
        cv2.imwrite(save_folder_path + label + "_depth.png", depth)
    return True


def saveSceneObject(scene_object, save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)
    for frame_idx, frame_object in scene_object.frame_object_dict.items():
        image = deepcopy(frame_object.image)
        depth = deepcopy(frame_object.depth)
        drawBBox(image, frame_object.bbox_2d)
        drawBBox(depth, frame_object.bbox_2d)

        cv2.imwrite(save_folder_path + "frame_" + frame_idx + "_image.png",
                    image)
        cv2.imwrite(save_folder_path + "frame_" + frame_idx + "_depth.png",
                    depth)
    return True


def saveAllSceneObjects(scene_object_dict, save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)

    for object_label, scene_object in scene_object_dict.items():
        scene_object_save_folder_path = save_folder_path + object_label + "/"
        assert saveSceneObject(scene_object, scene_object_save_folder_path)
    return True
