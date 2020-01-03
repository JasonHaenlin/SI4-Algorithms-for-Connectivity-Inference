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

    def __init__(self, name : str, is_complet:bool = False, vertices: list = [], edges : list = [], sub_graphs : list = []):
        self._name = name
        self._vertices = []
        self._edges = []
        
        if sub_graphs :
            for sg in sub_graphs :
                self._add_sub_graph_(sg)
            self._update_sub_graphs_weights_(sub_graphs)
        else :
            self._is_complet = is_complet

            if vertices :
                self._add_all_vertices_(vertices)

            if is_complet :
                for i in range (0,len(self._vertices)-1) :
                    for j in range (i+1, len(self._vertices)):
                        self._add_edge_(v1=self._vertices[i], v2=self._vertices[j])
            else :
                self._edges = edges
        

    def _add_edge_(self, v1 : Vertex = None, v2 : Vertex = None, e : Edge = None, compute_weight : bool = False):
        if e :
            v1 = e._v1
            v2 = e._v2

        if not self._has_edge_(v1, v2) :
            self._add_vertex_(v1)
            self._add_vertex_(v2)
            realV1 = self._get_vertex_(v1)
            realV2 = self._get_vertex_(v2)
            if realV1 and realV2 :
                self._edges.append(Edge(realV1,realV2))
        elif compute_weight :
            real_edge = self._get_edge_(v1, v2)
            if real_edge :
                real_edge._increment_weight()


    def _add_vertex_(self, v : Vertex) :
        if not v :
            return
        if not self._has_vertex_(v) :
            self._vertices.append(Vertex(v._tag))

    def _add_all_vertices_(self, vertices : list) :
        for v in vertices :
            self._add_vertex_(v)

    def _add_sub_graph_(self, graph : 'Graph') :
        for v in graph._vertices :
            self._add_vertex_(v)
        for e in graph._edges :
            self._add_edge_(e=e, compute_weight=True)

    def _update_sub_graphs_weights_(self, sub_graphs : list) :
        for sg in sub_graphs :
            for edge in sg._edges :
                edge._weight = self._get_edge_(edge._v1, edge._v2)._weight

    def _get_vertex_(self, v:Vertex) -> Vertex:
        if not v :
            return None
        for vertex in self._vertices :
            if(v._tag == vertex._tag) :
                return vertex
        return None

    def _get_edge_(self, v1:Vertex, v2:Vertex) -> Edge:
        for edge in self._edges :
            if(edge._is_edge_of_(v1, v2)) :
                return edge
        return None
    
    def _get_edges_from_vertex(self, v : Vertex) -> list:
        edges = []
        for edge in self._edges :
            if edge._has_vertex_(v) :
                edges.append(edge)
        return edges

    def _has_edge_(self, v1 : Vertex, v2 : Vertex) -> bool :
        if not v1 : 
            return False
        if not v2 :
            return False
        for edge in self._edges :
            if edge._is_edge_of_(v1, v2) :
                return True
        return False

    def _has_vertex_(self, v : Vertex) -> bool :
        if not v :
            return False
        if self._vertices :
            for vertex in self._vertices :
                if vertex._tag == v._tag :
                    return True
        return False

    def _reset_(self) :
        self._vertices = []
        self._edges = []

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        strRes = "***Graph {}***\n".format(self._name)
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
