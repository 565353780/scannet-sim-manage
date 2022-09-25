#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../habitat-sim-manage")
from habitat_sim_manage.Module.sim_manager import SimManager

import os
from getch import getch

from auto_cad_recon.Data.point_image import PointImage

from auto_cad_recon.Method.image import saveLabelImages, saveAllSceneObjects
from auto_cad_recon.Method.render import renderPointImage, renderBBox, renderAll

from auto_cad_recon.Module.scene_object_manager import SceneObjectManager
from auto_cad_recon.Module.scene_object_dist_calculator import \
    SceneObjectDistCalculator


class ScanNetSimLoader(object):

    def __init__(self):
        self.sim_manager = SimManager()
        self.scene_object_dist_calculator = SceneObjectDistCalculator()
        self.scene_object_manager = SceneObjectManager()

        self.scene_name = None
        self.frame_idx = 0
        return

    def reset(self):
        self.sim_manager.reset()
        self.scene_object_dist_calculator.reset()
        self.scene_object_manager.reset()
        self.scene_name = None
        self.frame_idx = 0
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

        self.reset()

        assert self.sim_manager.loadSettings(glb_file_path)
        assert self.scene_object_dist_calculator.loadSceneObject(
            object_folder_path, print_progress)
        assert self.scene_object_dist_calculator.loadObjectBBox(
            bbox_json_file_path)
        self.scene_name = glb_file_path.split("/")[-2]
        return True

    def setControlMode(self, control_mode):
        return self.sim_manager.setControlMode(control_mode)

    def getLabeledPointImage(self, point_image, print_progress=False):
        # TODO: use network to do this if infer

        # use GT
        point_image = self.scene_object_dist_calculator.getLabeledPointImage(
            point_image, print_progress)
        return point_image

    def getObjectInView(self, print_progress=True):
        observations = self.sim_manager.sim_loader.observations
        agent_state = self.sim_manager.sim_loader.getAgentState()

        point_image = PointImage(observations, agent_state)

        point_image = self.getLabeledPointImage(point_image, print_progress)

        self.scene_object_manager.extractObjectsFromPointImage(
            point_image, self.frame_idx)
        self.frame_idx += 1

        #  assert saveLabelImages(point_image, "./test/point_image/")

        #  assert renderPointImage(point_image)
        #  assert renderBBox(self.scene_object_dist_calculator.bbox_dict)
        #  assert renderAll(point_image, self.scene_object_dist_calculator.bbox_dict)
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
        print("[INFO][ScanNetSimLoader::startKeyBoardControlRender")
        print("\t start save scene objects...")
        saveAllSceneObjects(self.scene_object_manager.scene_object_dict,
                            "./test/scene_objects/")
        self.sim_manager.cv_renderer.close()
        return True
