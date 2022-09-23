#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../habitat-sim-manage")
from habitat_sim_manage.Data.point import Point
from habitat_sim_manage.Data.rad import Rad
from habitat_sim_manage.Data.pose import Pose
from habitat_sim_manage.Module.sim_manager import SimManager

import os
from getch import getch


class ScanNetSimLoader(object):

    def __init__(self):
        self.sim_manager = SimManager()
        return

    def reset(self):
        self.sim_manager.reset()
        return True

    def loadScene(self, glb_file_path):
        assert os.path.exists(glb_file_path)
        self.sim_manager.loadSettings(glb_file_path)
        return True

    def setControlMode(self, control_mode):
        return self.sim_manager.setControlMode(control_mode)

    def getObjectInView(self):
        observations = self.sim_manager.sim_loader.observations

        rgb_obs = observations["color_sensor"]
        rgb_obs = rgb_obs[..., 0:3]

        depth_obs = observations["depth_sensor"]

        print(rgb_obs.shape)
        print(depth_obs.shape)
        return True

    def startKeyBoardControlRender(self, wait_val):
        #  self.sim_manager.resetAgentPose()
        self.sim_manager.cv_renderer.init()

        while True:
            if not self.sim_manager.cv_renderer.renderFrame(
                    self.sim_manager.sim_loader.observations):
                break
            self.sim_manager.cv_renderer.waitKey(wait_val)

            agent_state = self.sim_manager.sim_loader.getAgentState()
            print("agent_state: position", agent_state.position, "rotation",
                  agent_state.rotation)

            input_key = getch()
            if input_key == "x":
                self.getObjectInView()
                continue
            if not self.sim_manager.keyBoardControl(input_key):
                break
        self.sim_manager.cv_renderer.close()
        return True


def demo():
    glb_file_path = \
        "/home/chli/chLi/ScanNet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    control_mode = "pose"
    wait_val = 1

    scannet_sim_loader = ScanNetSimLoader()
    scannet_sim_loader.loadScene(glb_file_path)
    scannet_sim_loader.setControlMode(control_mode)

    scannet_sim_loader.sim_manager.pose_controller.pose = Pose(
        Point(1.7, 1.5, -2.5), Rad(0.2, 0.0))
    scannet_sim_loader.sim_manager.sim_loader.setAgentState(
        scannet_sim_loader.sim_manager.pose_controller.getAgentState())

    scannet_sim_loader.startKeyBoardControlRender(wait_val)
    return True
