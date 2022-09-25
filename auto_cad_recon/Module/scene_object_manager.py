#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.scene_object import SceneObject


class SceneObjectManager(object):

    def __init__(self):
        self.scene_object_list = []
        return

    def reset(self):
        del self.scene_object_list
        self.scene_object_list = []
        return True

    def haveThisLabel(self, object_label):
        if len(self.scene_object_list) == 0:
            return False
        for scene_object in self.scene_object_list:
            if scene_object.object_label == object_label:
                return True
        return False

    def addSceneObject(self, object_label):
        if self.haveThisLabel(object_label):
            return True

        self.scene_object_list.append(SceneObject(object_label))
        return True

    def getSceneObjectLabelList(self):
        return [
            scene_object.object_label
            for scene_object in self.scene_object_list
        ]

    def addFrameObject(self, color_point_set, image, object_label):
        self.addSceneObject(object_label)
        for scene_object in self.scene_object_list:
            if scene_object.object_label != object_label:
                continue

            scene_object.addFrameObject(color_point_set, image)
            return True

    def getFrameObjectList(self, object_label):
        for scene_object in self.scene_object_list:
            if scene_object.object_label != object_label:
                continue
            return scene_object.frame_object_list

        print("[WARN][SceneObjectManager::getFrameObjectList]")
        print("\t this object [" + object_label + "] not exist!")
        return []
