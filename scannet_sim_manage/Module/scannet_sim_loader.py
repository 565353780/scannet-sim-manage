#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from getch import getch
from copy import deepcopy

from habitat_sim_manage.Data.pose import Pose

from habitat_sim_manage.Module.sim_manager import SimManager

from detectron2_detect.Module.detector import Detector as MaskRCNNDetector

from scannet_sim_manage.Data.point_image import PointImage

from scannet_sim_manage.Method.image import saveLabelImages, saveAllSceneObjects
from scannet_sim_manage.Method.render import renderPointImage, renderBBox, renderAll

from scannet_sim_manage.Module.scene_object_manager import SceneObjectManager
from scannet_sim_manage.Module.scene_object_dist_calculator import \
    SceneObjectDistCalculator
from scannet_sim_manage.Module.scene_object_bbox_manager import SceneObjectBBoxManager

mode_list = ['gt', 'mask_rcnn']
mode = 'gt'


class ScanNetSimLoader(object):

    def __init__(self):
        self.sim_manager = SimManager()
        self.scene_object_dist_calculator = SceneObjectDistCalculator()
        self.scene_object_manager = SceneObjectManager()

        self.scene_name = None
        self.frame_idx = 0

        if mode == 'mask_rcnn':
            mask_rcnn_model_file_path = "/home/chli/chLi/detectron2/model_final_2d9806.pkl"
            mask_rcnn_config_name = "X_101_32x8d_FPN_3x"
            self.mask_rcnn_detector = MaskRCNNDetector(
                mask_rcnn_model_file_path, mask_rcnn_config_name)
            self.scene_object_bbox_manager = SceneObjectBBoxManager()
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
                  print_progress=False,
                  valid_object_file_name_list=None):
        assert os.path.exists(glb_file_path)
        assert os.path.exists(object_folder_path)

        self.reset()

        assert self.sim_manager.loadSettings(glb_file_path)
        assert self.scene_object_dist_calculator.loadSceneObject(
            object_folder_path, print_progress, valid_object_file_name_list)
        assert self.scene_object_dist_calculator.loadObjectBBox(
            bbox_json_file_path, valid_object_file_name_list)
        self.scene_name = glb_file_path.split("/")[-2]
        return True

    def setControlMode(self, control_mode):
        return self.sim_manager.setControlMode(control_mode)

    def setAgentPose(self, xyz_list, urf_list):
        self.sim_manager.pose_controller.pose = Pose.fromList(
            xyz_list, urf_list)
        self.sim_manager.sim_loader.setAgentState(
            self.sim_manager.pose_controller.getAgentState())
        return True

    def getLabeledPointImage(self, point_image, print_progress=False):
        if mode == 'gt':
            point_image = self.scene_object_dist_calculator.getLabeledPointImage(
                point_image, print_progress)
            return point_image

        if mode == 'mask_rcnn':
            point_image_copy = deepcopy(point_image)
            image = point_image_copy.image
            result_dict = self.mask_rcnn_detector.detect_image(image)

            for i in range(result_dict['pred_classes'].shape[0]):
                score = result_dict['scores'][i]
                if score < 0.1:
                    continue

                class_idx = result_dict['pred_classes'][i]
                mask = result_dict['pred_masks'][i]

                point_image_copy.addLabelMask(mask, str(class_idx), "object")

            point_image_copy.updateAllLabelBBox2D()

            valid_label_value_list = point_image_copy.getValidLabelValueList()
            for label, value in valid_label_value_list:
                # TODO: use label and value to select points and generate bbox, merge them then
                print(label, value)
            return point_image_copy

    def getObjectInView(self, print_progress=True):
        observations = self.sim_manager.sim_loader.observations
        agent_state = self.sim_manager.sim_loader.getAgentState()

        point_image = PointImage(observations, agent_state)

        point_image = self.getLabeledPointImage(point_image, print_progress)

        self.scene_object_manager.extractObjectsFromPointImage(
            point_image, self.frame_idx)

        saveLabelImages(point_image,
                        "./test/point_image/" + str(self.frame_idx) + "/")

        renderAll(point_image, self.scene_object_dist_calculator.bbox_dict)

        self.frame_idx += 1
        return True

    def saveAllSceneObjects(self, save_folder_path, bbox_image_width,
                            bbox_image_height, bbox_image_free_width):
        return saveAllSceneObjects(self.scene_object_manager.scene_object_dict,
                                   save_folder_path, bbox_image_width,
                                   bbox_image_height, bbox_image_free_width)

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
            if input_key == "v":
                self.getObjectInView()
                continue
            if not self.sim_manager.keyBoardControl(input_key):
                break

        self.sim_manager.cv_renderer.close()
        return True
