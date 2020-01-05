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

    def __init__(self, name: str, is_complet: bool = False, vertices: list = [], edges: list = [], sub_graphs: list = []):
        #print("creating {}".format(name))
        self._name = name
        self._vertices = []
        self._edges = []

        if sub_graphs:
            for sg in sub_graphs:
                self._add_sub_graph_(sg)
            self._update_sub_graphs_weights_(sub_graphs)
        else:
            self._is_complet = is_complet

            if vertices:
                self._add_all_vertices_(vertices)

            if is_complet:
                for i in range(0, len(self._vertices)-1):
                    for j in range(i+1, len(self._vertices)):
                        #print("add edge {} {}".format(self._vertices[i], self._vertices[j]))
                        self._add_edge_(
                            v1=self._vertices[i], v2=self._vertices[j])
                        #print ("{}\n{}".format(self._vertices[i], self._vertices[j]))
            else:
                self._edges = edges

    def _add_edge_(self, v1: Vertex = None, v2: Vertex = None, e: Edge = None, compute_weight: bool = False):
        if e:
            v1 = e._v1
            v2 = e._v2

        if not self._has_edge_(v1, v2):
            self._add_vertex_(v1)
            self._add_vertex_(v2)
            realV1 = self._get_vertex_(v1)
            realV2 = self._get_vertex_(v2)
            if realV1 and realV2:
                self._edges.append(Edge(realV1, realV2))
        elif compute_weight:
            real_edge = self._get_edge_(v1, v2)
            if real_edge:
                real_edge._increment_weight()

    def _add_vertex_(self, v: Vertex, compute_weight: bool = False):
        if not v:
            return
        if not self._has_vertex_(v):
            self._vertices.append(Vertex(v._tag))
        elif compute_weight:
            real_vertex = self._get_vertex_(v)
            if real_vertex:
                real_vertex._increment_weight()

    def _add_all_vertices_(self, vertices: list):
        for v in vertices:
            self._add_vertex_(v)

    def _add_sub_graph_(self, graph: 'Graph'):
        for v in graph._vertices:
            self._add_vertex_(v, compute_weight=True)
        for e in graph._edges:
            self._add_edge_(e=e, compute_weight=True)

    def delete_edge(self, e: Edge):
        if not e:
            return

        real_edge = self._get_edge_(e._v1, e._v2)
        if not real_edge:
            return

        real_edge._v1.remove(real_edge._v2)
        real_edge._v2.remove(real_edge._v1)
        self._edges.remove(real_edge)

    def _update_sub_graphs_weights_(self, sub_graphs: list):
        for sg in sub_graphs:
            for edge in sg._edges:
                real_edge = self._get_edge_(edge._v1, edge._v2)
                edge._weight = real_edge._weight
                edge._v1._weight = real_edge._v1._weight
                edge._v2._weight = real_edge._v2._weight

    def _get_vertex_(self, v: Vertex) -> Vertex:
        if not v:
            return None
        for vertex in self._vertices:
            if(v._tag == vertex._tag):
                return vertex
        return None

    def _get_edge_(self, v1: Vertex, v2: Vertex) -> Edge:
        for edge in self._edges:
            if(edge._is_edge_of_(v1, v2)):
                return edge
        return None

    def _get_edges_from_vertex(self, v: Vertex) -> list:
        edges = []
        for edge in self._edges:
            if edge._has_vertex_(v):
                edges.append(edge)
        return edges

    def _has_edge_(self, v1: Vertex, v2: Vertex) -> bool:
        if not v1:
            return False
        if not v2:
            return False
        for edge in self._edges:
            if edge._is_edge_of_(v1, v2):
                return True
        return False

    def _has_vertex_(self, v: Vertex) -> bool:
        if not v:
            return False
        if self._vertices:
            for vertex in self._vertices:
                if vertex._tag == v._tag:
                    return True
        return False

    def is_useful_edge(self, e: Edge, sg: 'Graph') -> bool:
        if not e:
            return False
        if not self._has_edge_(e._v1, e._v2):
            return False
        if not sg._has_edge_(e._v1, e._v2):
            return False
        if not self._exists_indirect_way_(e._v1, e._v2, sg):
            return True
        return False

    def is_connexe(self, sg : 'Graph') -> bool :
        if self._vertices and sg and sg._vertices and len(sg._vertices) > 0 :
            source = sg._vertices[0]
            #print("source : {}".format(source))
            for v in sg._vertices :
                if source._tag != v._tag :
                    #print("checking for : {}".format(v))
                    if not self._exists_way_([], source, v, sg) :
                        return False
            return True


    def _exists_indirect_way_(self, v1: Vertex, v2: Vertex, sg: 'Graph') -> bool:
        if not v1 or not v2:
            return False

        v1 = self._get_vertex_(v1)
        v2 = self._get_vertex_(v2)

        adjacents = v1._adjacents
        if len(adjacents) == 1 or len(v2._adjacents) == 1:
            return False

        if adjacents and len(adjacents) > 1:
            forbidden_vertices = []
            forbidden_vertices.append(v1)
            for adj in adjacents:
                if(adj._tag != v2._tag) and sg._has_vertex_(adj):
                    exist_way = self._exists_way_(
                        forbidden_vertices, adj, v2, sg)
                    if exist_way:
                        return True
        return False

    def _exists_way_(self, forbidden_vertices: list, v1: Vertex, v2: Vertex, sg: 'Graph') -> bool:
        #print("check {} and {}".format(v1,v2))
        if not v1 or not v2:
            return False

        v1 = self._get_vertex_(v1)
        v2 = self._get_vertex_(v2)

        adjacents = v1._adjacents
        adjacents_to_check = []

        if adjacents:
            for adj in adjacents:
                if adj._tag == v2._tag:
                    return True
                if not self._is_forbidden_vertex_(forbidden_vertices, adj) and sg._has_vertex_(adj):
                    adjacents_to_check.append(adj)

        if len(adjacents_to_check) == 0:
            return False

        forbidden_vertices.append(v1)
        for a in adjacents_to_check:
            exist_way = self._exists_way_(forbidden_vertices, a, v2, sg)
            if exist_way:
                return True
        return False

    def _is_forbidden_vertex_(self, forbidden_vertices: list, v1: Vertex) -> bool:
        if not forbidden_vertices:
            return False
        if not v1:
            return False
        for v in forbidden_vertices:
            if v1._tag == v._tag:
                return True
        return False

    def _reset_(self):
        self._vertices = []
        self._edges = []

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        strRes = "***Graph {}***\n".format(self._name)
        strRes += "***Vertices : \n"
        for vertex in self._vertices:
            strRes += str(vertex)
            strRes += "\n"
        strRes += "***Edges : \n"
        for edge in self._edges:
            strRes += str(edge)
            strRes += "\n"
        return strRes

    def __repr__(self):
        return str(self._name)
