#!/usr/bin/env python
# -*- coding: utf-8 -*-

import quaternion
import numpy as np

from auto_cad_recon.Data.color_point import ColorPoint


def getCameraMatrix(hfov):
    K = np.array([[1 / np.tan(hfov / 2.), 0., 0., 0.],
                  [0., 1 / np.tan(hfov / 2.), 0., 0.], [0., 0., 1, 0],
                  [0., 0., 0, 1]])
    return K


def getCamera3DPoint(observations):
    hfov = 90. * np.pi / 180.

    depth_obs = observations["depth_sensor"]
    H, W = depth_obs.shape[:2]
    depth = depth_obs.reshape(1, W, H)
    xs, ys = np.meshgrid(np.linspace(-1, 1, W), np.linspace(1, -1, H))
    xs = xs.reshape(1, W, H)
    ys = ys.reshape(1, W, H)
    xys = np.vstack((xs * depth, ys * depth, -depth, np.ones(depth.shape)))
    xys = xys.reshape(4, -1)

    K = getCameraMatrix(hfov)

    xy_c0 = np.matmul(np.linalg.inv(K), xys)
    return xy_c0


def getCameraToWorldMatrix(agent_state):
    rotation = agent_state.sensor_states['depth_sensor'].rotation
    translation = agent_state.sensor_states['depth_sensor'].position
    rotation = quaternion.as_rotation_matrix(rotation)
    T_camera_world = np.eye(4)
    T_camera_world[0:3, 0:3] = rotation
    T_camera_world[0:3, 3] = translation
    return T_camera_world


def getColorPointList(observations, agent_state):
    xy_c0 = getCamera3DPoint(observations)

    T_camera_world = getCameraToWorldMatrix(agent_state)

    points = np.matmul(T_camera_world, xy_c0)[:3, :].transpose(1, 0)

    colors = observations["color_sensor"][..., :3].reshape(-1, 3)

    color_point_list = []
    for point, color in zip(points, colors):
        color_point = ColorPoint(point[0], point[1], point[2], color[0],
                                 color[1], color[2])
        color_point_list.append(color_point)
    return color_point_list
