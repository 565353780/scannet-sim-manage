#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../habitat-sim-manage")
from habitat_sim_manage.Data.point import Point
from habitat_sim_manage.Data.rad import Rad
from habitat_sim_manage.Data.pose import Pose

from scannet_sim_manage.Module.scannet_sim_loader import ScanNetSimLoader


def demo():
    glb_file_path = \
        "/home/chli/chLi/ScanNet/scans/scene0474_02/scene0474_02_vh_clean.glb"
    object_folder_path = "/home/chli/chLi/ScanNet/objects/scene0474_02/"
    bbox_json_file_path = "/home/chli/chLi/ScanNet/bboxes/scene0474_02/object_bbox.json"
    control_mode = "pose"
    wait_val = 1
    print_progress = True

    scene_objects_save_folder_path = "./output/scene_objects/scene0474_02/"

    scannet_sim_loader = ScanNetSimLoader()
    scannet_sim_loader.loadScene(glb_file_path, object_folder_path,
                                 bbox_json_file_path, print_progress)
    scannet_sim_loader.setControlMode(control_mode)

    scannet_sim_loader.sim_manager.pose_controller.pose = Pose(
        Point(3.7, 1.0, -2.6), Rad(0.2, 0.0))
    scannet_sim_loader.sim_manager.sim_loader.setAgentState(
        scannet_sim_loader.sim_manager.pose_controller.getAgentState())

    scannet_sim_loader.startKeyBoardControlRender(wait_val)

    scannet_sim_loader.saveAllSceneObjects(scene_objects_save_folder_path)
    return True
