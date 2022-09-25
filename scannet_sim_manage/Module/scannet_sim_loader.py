#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from getch import getch

from habitat_sim_manage.Module.sim_manager import SimManager

from scannet_sim_manage.Data.point_image import PointImage

from scannet_sim_manage.Method.image import saveLabelImages, saveAllSceneObjects
from scannet_sim_manage.Method.render import renderPointImage, renderBBox, renderAll

from scannet_sim_manage.Module.scene_object_manager import SceneObjectManager
from scannet_sim_manage.Module.scene_object_dist_calculator import \
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

        #  assert saveLabelImages(point_image, "./test/point_image/" + str(self.frame_idx)))

        #  assert renderPointImage(point_image)
        #  assert renderBBox(self.scene_object_dist_calculator.bbox_dict)
        #  assert renderAll(point_image, self.scene_object_dist_calculator.bbox_dict)

        self.frame_idx += 1
        return True

    def saveAllSceneObjects(self, save_folder_path):
        saveAllSceneObjects(self.scene_object_manager.scene_object_dict,
                            save_folder_path)
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
