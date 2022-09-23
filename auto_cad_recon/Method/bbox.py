#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getPointInBBoxIdxList(point, bbox_list):
    point_in_bbox_idx_list = []
    for i, bbox in enumerate(bbox_list):
        if bbox.isInBBox(point):
            point_in_bbox_idx_list.append(i)

    return point_in_bbox_idx_list


def getPointInBBoxIdxListDict(point_list, bbox_list):
    point_in_bbox_idx_list_dict = {}
    for i, point in enumerate(point_list):
        point_in_bbox_idx_list = getPointInBBoxIdxList(point, bbox_list)
        if len(point_in_bbox_idx_list) == 0:
            continue
        point_in_bbox_idx_list_dict[str(i)] = point_in_bbox_idx_list

    return point_in_bbox_idx_list_dict
