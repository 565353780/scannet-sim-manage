#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append("../mesh-manage")

import os

import numpy as np
from mesh_manage.Module.channel_mesh import ChannelMesh
from tqdm import tqdm

from auto_cad_recon.Data.color_point_set import ColorPointSet
from auto_cad_recon.Method.dist import getNearestDistListToMeshDict


class SceneObjectDistCalculator(object):

    def __init__(self,
                 object_folder_path=None,
                 dist_error_max=0.1,
                 print_progress=False):
        self.dist_error_max = dist_error_max

        self.channel_mesh_dict = {}

        if object_folder_path is not None:
            self.loadSceneObject(object_folder_path, print_progress)
        return

    def reset(self):
        del self.channel_mesh_dict
        self.channel_mesh_dict = {}
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

    def getColorPointSetDict(self, point_list, print_progress=False):
        nearest_dist_list, nearest_dist_key_list = getNearestDistListToMeshDict(
            point_list, self.channel_mesh_dict, print_progress)

        nearest_dist_array = np.array(nearest_dist_list)
        nearest_dist_key_array = np.array(nearest_dist_key_list)
        color_point_set_dict = {}
        for object_file_name in self.channel_mesh_dict.keys():
            match_object_point_idx_list = np.where(
                nearest_dist_key_array == object_file_name)[0]
            match_point_idx_list = match_object_point_idx_list[np.where(
                nearest_dist_array[match_object_point_idx_list] <=
                self.dist_error_max)[0]]

            match_point_list = [
                point_list[match_point_idx]
                for match_point_idx in match_point_idx_list
            ]
            color_point_set_dict[object_file_name] = ColorPointSet(
                match_point_list)
        return color_point_set_dict
