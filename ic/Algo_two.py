#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from ic.Edge import Edge
from ic.Graph import Graph
from collections import Counter
from operator import itemgetter

import time


def compute(k: int, delta: int, sg: list, real_list: list = []) -> Graph:
    #print("compute algo 2")
    init(k, delta, sg, real_list)
    if sub_graphs:
        global trees
        for sub in sub_graphs:
            # print(sub)
            tree = get_tree(sub)
            trees.append(tree)
            # print(tree)
            result._add_sub_graph_(tree)
            calculate_delta()
    # print(result)
    delete_unuseful_edges()
    #print("edges deleted")
    # print(result)
    return result


def init(k: int, delta: int, sg: list, real_list: list = []):
    global sub_graphs
    global big_graph
    global result
    global actual_delta
    global vertices_with_delta_max
    global trees
    trees = []
    actual_delta = 0
    vertices_with_delta_max = []
    sub_graphs = []
    if real_list:
        sub_graphs = real_list
        # for s in sub_graphs :
        # print(s)
    else:
        i = 1
        if sg:
            for g in sg:
                list_vertices = []
                #print("*******************\nSubgraph {}\n*******************".format(i))
                for v in g:
                    real_vertex = Vertex(v)
                    # print(real_vertex)
                    list_vertices.append(real_vertex)
                real_graph = Graph("Subgraph", True, vertices=list_vertices)
                sub_graphs.append(real_graph)
                i += 1
    big_graph = get_all_sub_graphs_in_one()
    result = Graph("Result")
    result._reset_()
    # print(str(big_graph))


def verify_result(k: int, d: int, graph: Graph) ->bool:
    if not graph:
        return False
    if not graph._vertices:
        return False
    if len(graph._edges) > k:
        return False
    for v in graph._vertices:
        if v.degree() > d:
            return False
    return True


def get_all_sub_graphs_in_one() -> Graph:
    return Graph("Global", sub_graphs=sub_graphs)


def calculate_delta():
    global actual_delta
    actual_delta = 0
    global vertices_with_delta_max
    vertices_with_delta_max = []
    for vertex in result._vertices:
        tmp_delta = vertex.degree()
        if tmp_delta > actual_delta:
            actual_delta = tmp_delta
            vertices_with_delta_max = []
            vertices_with_delta_max.append(vertex)
        elif tmp_delta == actual_delta:
            vertices_with_delta_max.append(vertex)


def is_vertex_with_max_delta(v: Vertex) -> bool:
    if not v:
        return False
    if vertices_with_delta_max:
        for vertex in vertices_with_delta_max:
            if vertex._tag == v._tag:
                return True
    return False


def get_tree(graph: Graph) -> Graph:
    #print("actual delta : {} / vertices {}".format(actual_delta, vertices_with_delta_max))
    tree = Graph("Tree")
    tree._reset_()
    edge = get_first_best_edge(graph._edges)
    tree._add_edge_(e=edge)
    #print("first edge : {}".format(edge))

    v1 = edge._v1
    v2 = edge._v2

    v1_edges = graph._get_edges_from_vertex(v1)
    v2_edges = graph._get_edges_from_vertex(v2)

    best_edge_v1 = get_edge_with_max_weight(v1_edges, tree, v1)
    best_edge_v2 = get_edge_with_max_weight(v2_edges, tree, v2)

    is_v1_max_delta = is_vertex_with_max_delta(v1)
    is_v2_max_delta = is_vertex_with_max_delta(v2)
    #print("best {} edge : {}".format(v1._tag, best_edge_v1))
    #print("best {} edge : {}".format(v2._tag, best_edge_v2))
    #print("is {} max delta : {}".format(v1._tag, is_v1_max_delta))
    #print("is {} max delta : {}".format(v2._tag, is_v2_max_delta))
    # time.sleep(5)

    start = None
    best_edge = None
    if best_edge_v1:
        start = v1
        best_edge = best_edge_v1
    elif best_edge_v2:
        start = v2
        best_edge = best_edge_v2

    if start == v1 and best_edge_v2:
        is_weight_greater = best_edge_v2._weight > best_edge_v1._weight
        is_vertex_weight_lower = best_edge_v2._weight == best_edge_v1._weight and v2._weight < v1._weight
        is_not_max_delta = best_edge_v2._weight == best_edge_v1._weight and v2._weight == v1._weight and is_v1_max_delta and not is_v2_max_delta
        if is_weight_greater or is_vertex_weight_lower or is_not_max_delta:
            start = v2
            best_edge = best_edge_v2

    change = False
    #print("best choosen edge : {}".format(best_edge))
    if start and best_edge:
        tree._add_edge_(e=best_edge)
        start = best_edge._get_other_vertex_(start)
        change = True

    while change:
        change = False
        edges_start = graph._get_edges_from_vertex(start)
        best_edge = get_edge_with_max_weight(edges_start, tree, start)
        #print("best edge : {}".format(best_edge))
        if best_edge:
            tree._add_edge_(e=best_edge)
            start = best_edge._get_other_vertex_(start)
            change = True

    return tree


def get_first_best_edge(edges: list) -> Edge:
    #print("tree : {}".format(tree))
    edge = None
    if edges:
        edge = edges[0]
        weight = edge._weight
        v1_weight = edge._v1._weight
        v2_weight = edge._v2._weight
        max_vertex_weight = v1_weight
        min_vertex_weight = v2_weight
        if v2_weight > v1_weight:
            max_vertex_weight = v2_weight
            min_vertex_weight = v1_weight
        is_v1_delta_max = is_vertex_with_max_delta(edge._v1)
        is_v2_delta_max = is_vertex_with_max_delta(edge._v2)
        max_delta = 0
        if (not (is_v1_delta_max and is_v2_delta_max)) and (is_v1_delta_max or is_v2_delta_max):
            max_delta = 1

        i = 1
        while i < len(edges):
            tmp_weight = edges[i]._weight
            v1_weight = edges[i]._v1._weight
            v2_weight = edges[i]._v2._weight
            tmp_max_vertex_weight = v1_weight
            tmp_min_vertex_weight = v2_weight
            if v2_weight > v1_weight:
                tmp_max_vertex_weight = v2_weight
                tmp_min_vertex_weight = v1_weight
            is_v1_delta_max = is_vertex_with_max_delta(edge._v1)
            is_v2_delta_max = is_vertex_with_max_delta(edge._v2)
            tmp_max_delta = 0
            if (not (is_v1_delta_max and is_v2_delta_max)) and (is_v1_delta_max or is_v2_delta_max):
                tmp_max_delta = 1
            #print("compare v1 {} : {}".format(edges[i]._v1, tree._has_vertex_(edges[i]._v1)))
            #print("compare v2 {} : {}".format(edges[i]._v2, tree._has_vertex_(edges[i]._v2)))
            # print("*****")
            is_weight_greater = tmp_weight > weight
            is_max_vertex_weight_greater = tmp_weight == weight and tmp_max_vertex_weight > max_vertex_weight
            is_min_vertex_weight_lower = tmp_weight == weight and tmp_max_vertex_weight == max_vertex_weight and tmp_min_vertex_weight < min_vertex_weight
            is_max_delta_greater = tmp_weight == weight and tmp_max_vertex_weight == max_vertex_weight and tmp_min_vertex_weight == min_vertex_weight and tmp_max_delta > max_delta

            if is_weight_greater or is_max_vertex_weight_greater or is_min_vertex_weight_lower or is_max_delta_greater:
                edge = edges[i]
                weight = tmp_weight
                max_vertex_weight = tmp_max_vertex_weight
                min_vertex_weight = tmp_min_vertex_weight
                max_delta = tmp_max_delta
                #print("choose !")
            i += 1
    return edge


def get_edge_with_max_weight(edges: list, tree: Graph, source: Vertex) -> Edge:
    #print("tree : {}".format(tree))
    edge = None
    if edges:
        i = 0
        while not edge and i < len(edges):
            # "print("choosing first one")
            #print("v1 {} : {}".format(edges[i]._v1, tree._has_vertex_(edges[i]._v1)))
            #print("v2 {} : {}".format(edges[i]._v2, tree._has_vertex_(edges[i]._v2)))
            # print("*****")
            # time.sleep(1)
            if not tree:
                edge = edges[i]
            elif not tree._has_vertex_(edges[i]._v1) or not tree._has_vertex_(edges[i]._v2):
                edge = edges[i]
            i += 1

        while i < len(edges):
            #print("compare v1 {} : {}".format(edges[i]._v1, tree._has_vertex_(edges[i]._v1)))
            #print("compare v2 {} : {}".format(edges[i]._v2, tree._has_vertex_(edges[i]._v2)))
            # print("*****")
            if not tree or (not tree._has_vertex_(edges[i]._v1) or not tree._has_vertex_(edges[i]._v2)):
                actual_vertex_weight = edge._get_other_vertex_(source)._weight
                tmp_vertex_weight = edges[i]._get_other_vertex_(source)._weight
                if edges[i]._weight > edge._weight or (edges[i]._weight == edge._weight and tmp_vertex_weight < actual_vertex_weight):
                    edge = edges[i]
                    #print("choose !")
            i += 1
    return edge


def delete_unuseful_edges():
    if result and result._edges:
        for edge in result._edges:
            if not is_useful_edge(edge):
                result.delete_edge(edge)


def is_useful_edge(e: Edge) -> bool:
    if not e:
        return False

    if sub_graphs:
        for sg in sub_graphs:
            useful = result.is_useful_edge(e, sg)
            if useful:
                return True
    return False
