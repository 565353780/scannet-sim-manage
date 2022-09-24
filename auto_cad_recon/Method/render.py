#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../image-to-cad")
from image_to_cad.Method.bboxes import getOpen3DBBoxFromBBox

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
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_image.point_array)
    pcd.colors = o3d.utility.Vector3dVector(
        point_image.image.reshape(-1, 3)[..., [2, 1, 0]] / 255.0)

    assert render([pcd])
    return True


def renderAll(point_image, bbox_dict):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_image.point_array)
    pcd.colors = o3d.utility.Vector3dVector(
        point_image.image.reshape(-1, 3)[..., [2, 1, 0]] / 255.0)

    bbox_list = []
    for bbox in bbox_dict.values():
        bbox_list.append(getOpen3DBBoxFromBBox(bbox))

    assert render([pcd] + bbox_list)
    return True
