#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../image-to-cad")
from image_to_cad.Method.bboxes import getOpen3DBBoxFromBBox

import numpy as np
import open3d as o3d
from multiprocessing import Process


def render(geometry_list):
    process = Process(target=o3d.visualization.draw_geometries,
                      args=(geometry_list, ))
    process.start()
    return True


def renderBBox(bbox_dict):
    bbox_list = []
    for bbox in bbox_dict.values():
        bbox_list.append(getOpen3DBBoxFromBBox(bbox))

    assert render(bbox_list)
    return True


def renderPointImage(point_image):
    points = point_image.point_array[np.where(
        point_image.point_array[:, 0] != float("inf"))[0]]

    colors = point_image.image.reshape(-1, 3)[np.where(
        point_image.point_array[:, 0] != float("inf"))[0]][...,
                                                           [2, 1, 0]] / 255.0

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    assert render([pcd])
    return True


def renderAll(point_image, bbox_dict):
    points = point_image.point_array[np.where(
        point_image.point_array[:, 0] != float("inf"))[0]]

    colors = point_image.image.reshape(-1, 3)[np.where(
        point_image.point_array[:, 0] != float("inf"))[0]][...,
                                                           [2, 1, 0]] / 255.0

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    bbox_list = []
    for bbox in bbox_dict.values():
        bbox_list.append(getOpen3DBBoxFromBBox(bbox))

    assert render([pcd] + bbox_list)
    return True
