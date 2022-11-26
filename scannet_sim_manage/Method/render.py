#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process

import numpy as np
import open3d as o3d

from scannet_sim_manage.Method.bbox import getOpen3DBBoxFromBBox


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

def isAnyPointInBBox(bbox, point_array):
    if len(point_array) == 0:
        return False

    mask_x = (point_array[:, 0] >= bbox.min_point.x) &\
        (point_array[:, 0] <= bbox.max_point.x)
    if True not in mask_x:
        return False

    mask_y = (point_array[:, 1] >= bbox.min_point.y) &\
        (point_array[:, 1] <= bbox.max_point.y)
    if True not in mask_y:
        return False

    mask_z = (point_array[:, 2] >= bbox.min_point.z) &\
        (point_array[:, 2] <= bbox.max_point.z)
    if True not in mask_z:
        return False

    mask = mask_x & mask_y & mask_z
    return True in mask

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
        if not isAnyPointInBBox(bbox, points):
            continue
        bbox_list.append(getOpen3DBBoxFromBBox(bbox))

    assert render([pcd] + bbox_list)
    return True
