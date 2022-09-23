#!/usr/bin/env python
# -*- coding: utf-8 -*-

import quaternion
import numpy as np
import open3d as o3d


def get3DPointCloud(observations, agent_state):
    rgb_obs = observations["color_sensor"][..., :3]

    depth_obs = observations["depth_sensor"]

    hfov = 90. * np.pi / 180.
    W = 480
    H = 360

    K = np.array([[1 / np.tan(hfov / 2.), 0., 0., 0.],
                  [0., 1 / np.tan(hfov / 2.), 0., 0.], [0., 0., 1, 0],
                  [0., 0., 0, 1]])

    rotation = agent_state.sensor_states['depth_sensor'].rotation
    translation = agent_state.sensor_states['depth_sensor'].position
    rotation = quaternion.as_rotation_matrix(rotation)
    T_world_camera = np.eye(4)
    T_world_camera[0:3, 0:3] = rotation
    T_world_camera[0:3, 3] = translation

    xs, ys = np.meshgrid(np.linspace(-1, 1, W), np.linspace(1, -1, H))
    depth = depth_obs.reshape(1, W, H)
    xs = xs.reshape(1, W, H)
    ys = ys.reshape(1, W, H)
    xys = np.vstack((xs * depth, ys * depth, -depth, np.ones(depth.shape)))
    xys = xys.reshape(4, -1)
    xy_c0 = np.matmul(np.linalg.inv(K), xys)
    point_array = np.matmul(T_world_camera, xy_c0)

    point_list = []
    for i in range(W * H):
        point_list.append(point_array[:3, i])

    points = np.array(point_list)
    color_list = []
    for i in range(rgb_obs.shape[0]):
        for j in range(rgb_obs.shape[1]):
            color_list.append(rgb_obs[i][j])
    colors = np.array(color_list)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors / 255.0)
    return pcd
