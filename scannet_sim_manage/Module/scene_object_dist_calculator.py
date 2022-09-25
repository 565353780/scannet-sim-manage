#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from tqdm import tqdm

from mesh_manage.Module.channel_mesh import ChannelMesh

from scannet_sim_manage.Data.bbox import BBox
from scannet_sim_manage.Data.point import Point


class SceneObjectDistCalculator(object):

    def __init__(self,
                 object_folder_path=None,
                 bbox_json_file_path=None,
                 dist_error_max=0.1,
                 print_progress=False):
        self.dist_error_max = dist_error_max

        self.channel_mesh_dict = {}
        self.bbox_dict = {}

        if object_folder_path is not None:
            self.loadSceneObject(object_folder_path, print_progress)
        if bbox_json_file_path is not None:
            self.loadObjectBBox(bbox_json_file_path)
        return

    def reset(self):
        del self.channel_mesh_dict
        self.channel_mesh_dict = {}
        self.bbox_dict = {}
        return True

    def loadSceneObject(self, object_folder_path, print_progress=False):
        assert os.path.exists(object_folder_path)
        object_file_name_list = os.listdir(object_folder_path)
        for_data = object_file_name_list
        if print_progress:
            print("[INFO][SceneObjectDistCalculator::loadSceneObject]")
            print("\t start load scene objects...")
            for_data = tqdm(for_data)
        for object_file_name in for_data:
            object_file_path = object_folder_path + object_file_name
            self.channel_mesh_dict[object_file_name] = ChannelMesh(
                object_file_path)
        return True

    def loadObjectBBox(self, bbox_json_file_path):
        assert os.path.exists(bbox_json_file_path)

        with open(bbox_json_file_path, "r") as f:
            data = f.read()
            bbox_json = json.loads(data)

        self.bbox_dict = {}
        for object_file_name, bbox_list in bbox_json.items():
            self.bbox_dict[object_file_name] = BBox.fromList(bbox_list)
        return True

    def generateBBoxLabel(self, point_image, print_progress=False):
        for_data = point_image.point_array
        if print_progress:
            print("[INFO][SceneObjectDistCalculator::generateBBoxLabel]")
            print("\t start add bbox label...")
            for_data = tqdm(for_data)
        for i, [x, y, z] in enumerate(for_data):
            point = Point(x, y, z)
            for object_file_name, bbox in self.bbox_dict.items():
                if bbox.isInBBox(point):
                    point_image.addLabel(i, object_file_name, "bbox")
        return point_image

    def generateObjectLabel(self, point_image, print_progress=False):
        for_data = point_image.point_array
        if print_progress:
            print("[INFO][SceneObjectDistCalculator::generateObjectLabel]")
            print("\t start add object label...")
            for_data = tqdm(for_data)
        for i, [x, y, z] in enumerate(for_data):
            for object_file_name in self.bbox_dict.keys():
                if object_file_name not in point_image.label_dict_list[i].keys(
                ):
                    continue

                dist = self.channel_mesh_dict[object_file_name].getNearestDist(
                    x, y, z)
                if dist <= self.dist_error_max:
                    point_image.addLabel(i, object_file_name, "object")
        return point_image

    def generateBackgroundLabel(self, point_image):
        for i, label_dict in enumerate(point_image.label_dict_list):
            if "empty" in label_dict.keys():
                continue
            is_background = True
            for value in label_dict.values():
                if value == "object":
                    is_background = False
                    break
            if is_background:
                point_image.addLabel(i, "background")
        return point_image

    def getLabeledPointImage(self, point_image, print_progress=False):
        point_image = self.generateBBoxLabel(point_image, print_progress)

        point_image = self.generateObjectLabel(point_image, print_progress)

        point_image = self.generateBackgroundLabel(point_image)

        point_image.updateAllLabelBBox2D()
        return point_image
