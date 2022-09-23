#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def getObjectImage(point_idx_list, image):
    object_image = np.zeros(image.shape)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel_idx = i * image.shape[0] + j
            if pixel_idx not in point_idx_list:
                continue
            object_image[i][j] = image[i][j]
    return object_image
