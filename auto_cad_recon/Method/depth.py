#!/usr/bin/env python
# -*- coding: utf-8 -*-

import quaternion
import numpy as np

from auto_cad_recon.Config.depth import K_INV, XS, YS


def getCameraPoint(observations):
    depth_obs = observations["depth_sensor"]
    depth = depth_obs.reshape(1, depth_obs.shape[1], depth_obs.shape[0])
    xys = np.vstack((XS * depth, YS * depth, -depth, np.ones(depth.shape)))
    xys = xys.reshape(4, -1)

    xy_c0 = np.matmul(K_INV, xys)
    return xy_c0


def getCameraToWorldMatrix(agent_state):
    rotation = agent_state.sensor_states['depth_sensor'].rotation
    translation = agent_state.sensor_states['depth_sensor'].position
    rotation = quaternion.as_rotation_matrix(rotation)
    T_camera_world = np.eye(4)
    T_camera_world[0:3, 0:3] = rotation
    T_camera_world[0:3, 3] = translation
    return T_camera_world


def getPointArray(observations, agent_state):
    xy_c0 = getCameraPoint(observations)

    T_camera_world = getCameraToWorldMatrix(agent_state)

    point_array = np.matmul(T_camera_world,
                            xy_c0)[:3, :].transpose(1, 0)[..., [0, 2, 1]]
    point_array[:, 1] *= -1

    camera_point = np.matmul(T_camera_world, [[0], [0], [0], [1]])[:3][[0, 2, 1]]
    camera_point[1] *= -1
    return point_array, camera_point
