#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7


# I do not know if this class will be of any use

from ic.Vertex import Vertex
from ic.Edge import Edge

class Graph(object):
    """
    A class used to represent a whole graph

    The graph is not necessarily connected

    ...

    Attributes
    ----------


    Methods
    -------

    """

    def __init__(self, tag : int, is_complet:bool = False, vertices: list = [], edges : list = [], sub_graphs : list = []):
        self._tag = tag
        self._vertices = []
        self._edges = []
        
        if sub_graphs :
            for sg in sub_graphs :
                self._add_sub_graph_(sg)
        else :
            self._is_complet = is_complet
            self._add_all_vertices_(vertices)

            if is_complet :
                for i in range (0,len(self._vertices)-1) :
                    for j in range (i+1, len(self._vertices)):
                        self._add_edge_(self._vertices[i], self._vertices[j])
            else :
                self._edges = edges
        

    def _add_edge_(self, v1 : Vertex, v2 : Vertex):
        if not self._is_edge_exists_(v1, v2) :
            realV1 = self._get_vertex_(v1)
            realV2 = self._get_vertex_(v2)
            if realV1 and realV2 :
                self._edges.append(Edge(realV1,realV2))

    def _add_vertex_(self, v : Vertex) :
        if not self._is_vertex_exists_(v) :
            self._vertices.append(Vertex(v._tag))

    def _add_all_vertices_(self, vertices : list) :
        for v in vertices :
            self._add_vertex_(v)

    def _add_sub_graph_(self, graph : 'Graph') :
        for v in graph._vertices :
            self._add_vertex_(v)
        for e in graph._edges :
            self._add_edge_(e._v1, e._v2)

    def _get_vertex_(self, v:Vertex) -> Vertex:
        for vertex in self._vertices :
            if(v._tag == vertex._tag) :
                return vertex
        return None

    def _is_edge_exists_(self, v1 : Vertex, v2 : Vertex) -> bool :
        for edge in self._edges :
            if edge._is_edge_of_(v1, v2) :
                return True
        return False

    def _is_vertex_exists_(self, v : Vertex) -> bool :
        for vertex in self._vertices :
            if(vertex._tag == v._tag) :
                return True
        return False

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        strRes = "***Graph {}***\n".format(self._tag)
        strRes += "***Vertices : \n"
        for vertex in self._vertices :
            strRes += str(vertex)
            strRes += "\n"
        strRes += "***Edges : \n"
        for edge in self._edges:
            strRes += str(edge)
            strRes += "\n"
        return strRes

    def __repr__(self):
        return str("TODO")
