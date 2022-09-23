#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_cad_recon.Data.color_point_set import ColorPointSet


def getColorPointSetInBBox(point_list, bbox):
    point_list_in_bbox = []
    for point in point_list:
        if bbox.isInBBox(point):
            point_list_in_bbox.append(point)

    return ColorPointSet(point_list_in_bbox)
