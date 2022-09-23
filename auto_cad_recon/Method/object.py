#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json

from auto_cad_recon.Data.bbox import BBox

from auto_cad_recon.Method.bbox import getPointInBBoxIdxListDict


def getInViewObjectFileNameList(bbox_json_file_path, color_point_list):
    assert os.path.exists(bbox_json_file_path)

    in_view_object_file_list = []

    with open(bbox_json_file_path, "r") as f:
        data = f.read()
        bbox_json = json.loads(data)

    bbox_dict = {}
    for object_file_name, bbox_list in bbox_json.items():
        bbox_dict[object_file_name] = BBox.fromList(bbox_list)

    point_in_bbox_idx_list_dict = getPointInBBoxIdxListDict(
        color_point_list, list(bbox_dict.values()))

    return bbox_dict.values()
