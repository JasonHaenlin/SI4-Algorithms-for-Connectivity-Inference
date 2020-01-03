#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7
from __future__ import annotations
from ic.Vertex import Vertex

class Edge(object):

    def __init__(self, v1 : Vertex, v2 : Vertex):
        if v1._tag != v2._tag :
            if v1._tag < v2._tag :
                self._v1 = v1
                self._v2 = v2
            else :
                self._v1 = v2
                self._v2 = v1
            self._v1.append(v2)
            self._v2.append(v1)

    def _is_edge_of_(self, v1 : Vertex, v2 : Vertex) -> bool:
        if v1._tag == self._v1._tag and v2._tag == self._v2._tag:
            return True
        if v1._tag == self._v2._tag and v2._tag == self._v1._tag:
            return True
        return False

    def __str__(self):
        return str("edge({},{})".format(self._v1._tag, self._v2._tag))