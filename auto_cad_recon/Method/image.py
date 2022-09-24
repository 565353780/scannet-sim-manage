#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2


def saveLabelImages(point_image, save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)

    cv2.imwrite(save_folder_path + "image.png", point_image.image)
    cv2.imwrite(save_folder_path + "depth.png", point_image.depth)

    all_label_image = point_image.getAllLabelImage()
    cv2.imwrite(save_folder_path + "all_label_image.png", all_label_image)

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
        if "." in label:
            label = label.split(".")[0]
        cv2.imwrite(save_folder_path + label + "_rgb.png", rgb)
        cv2.imwrite(save_folder_path + label + "_depth.png", depth)
    return True
