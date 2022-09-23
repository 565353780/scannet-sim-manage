#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
from tqdm import tqdm


def getPointDist2(point_1, point_2):
    x_diff = point_1.x - point_2.x
    y_diff = point_1.y - point_2.y
    z_diff = point_1.z - point_2.z
    return x_diff * x_diff + y_diff * y_diff + z_diff * z_diff


def getPointDist(point_1, point_2):
    return sqrt(getPointDist2(point_1, point_2))


def getNearestDistToMeshDict(point, mesh_dict):
    min_dist = float("inf")
    min_dist_key = None

    for key, mesh in mesh_dict.items():
        current_dist = mesh.getNearestDist(point.x, point.y, point.z)
        if current_dist >= min_dist:
            continue
        min_dist = current_dist
        min_dist_key = key

    return min_dist, min_dist_key


def getNearestDistListToMeshDict(point_list, mesh_dict, print_progress=False):
    nearest_dist_list = []
    nearest_dist_key_list = []

    for_data = point_list
    if print_progress:
        print("[INFO][dist::getNearestDistListToMeshDict]")
        print("\t start compute nearest dists to meshes...")
        for_data = tqdm(for_data)
    for point in for_data:
        min_dist, min_dist_key = getNearestDistToMeshDict(point, mesh_dict)
        nearest_dist_list.append(min_dist)
        nearest_dist_key_list.append(min_dist_key)
    return nearest_dist_list, nearest_dist_key_list
