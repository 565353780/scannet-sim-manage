#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np


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
