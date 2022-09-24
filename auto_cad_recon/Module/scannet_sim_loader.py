#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../habitat-sim-manage")
from habitat_sim_manage.Data.point import Point
from habitat_sim_manage.Data.rad import Rad
from habitat_sim_manage.Data.pose import Pose
from habitat_sim_manage.Module.sim_manager import SimManager

sys.path.append("../image-to-cad")
from image_to_cad.Method.bboxes import getOpen3DBBoxFromBBox

import os
import open3d as o3d
from getch import getch
from multiprocessing import Process

from auto_cad_recon.Module.scene_object_dist_calculator import \
    SceneObjectDistCalculator


class ScanNetSimLoader(object):

    def __init__(self):
        self.sim_manager = SimManager()
        self.scene_object_dist_calculator = SceneObjectDistCalculator()

        self.scene_name = None
        return

    def reset(self):
        self.sim_manager.reset()
        self.scene_object_dist_calculator.reset()
        self.scene_name = None
        return True

    def loadSceneObject(self, object_folder_path):
        assert os.path.exists(object_folder_path)
        assert self.scene_object_dist_calculator.loadSceneObject(
            object_folder_path)
        return True

    def loadScene(self,
                  glb_file_path,
                  object_folder_path,
                  bbox_json_file_path,
                  print_progress=False):
        assert os.path.exists(glb_file_path)
        assert os.path.exists(object_folder_path)

        assert self.sim_manager.loadSettings(glb_file_path)
        assert self.scene_object_dist_calculator.loadSceneObject(
            object_folder_path, print_progress)
        assert self.scene_object_dist_calculator.loadObjectBBox(
            bbox_json_file_path)
        self.scene_name = glb_file_path.split("/")[-2]
        return True

    def setControlMode(self, control_mode):
        return self.sim_manager.setControlMode(control_mode)

    def getObjectInView(self, print_progress=True):
        observations = self.sim_manager.sim_loader.observations
        agent_state = self.sim_manager.sim_loader.getAgentState()

        point_image = self.scene_object_dist_calculator.generatePointImage(
            observations, agent_state, print_progress)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_image.point_array)
        pcd.colors = o3d.utility.Vector3dVector(
            point_image.image.reshape(-1, 3) / 255.0)

        process = Process(target=o3d.visualization.draw_geometries,
                          args=([pcd], ))
        process.start()
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
    object_folder_path = "/home/chli/chLi/ScanNet/objects/scene0474_02/"
    bbox_json_file_path = "/home/chli/chLi/ScanNet/bboxes/scene0474_02/object_bbox.json"
    control_mode = "pose"
    wait_val = 1
    print_progres = True

    scannet_sim_loader = ScanNetSimLoader()
    scannet_sim_loader.loadScene(glb_file_path, object_folder_path,
                                 bbox_json_file_path, print_progres)
    scannet_sim_loader.setControlMode(control_mode)

    #  scannet_sim_loader.sim_manager.pose_controller.pose = Pose(
    #  Point(1.7, 1.5, -2.5), Rad(0.2, 0.0))
    #  scannet_sim_loader.sim_manager.sim_loader.setAgentState(
    #  scannet_sim_loader.sim_manager.pose_controller.getAgentState())

    scannet_sim_loader.startKeyBoardControlRender(wait_val)
    return True
