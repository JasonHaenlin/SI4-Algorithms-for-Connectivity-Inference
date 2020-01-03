#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from ic.Edge import Edge
from ic.Graph import Graph
from collections import Counter
from operator import itemgetter

import time

def compute(k: int, delta : int, sg: list) -> list:
    init(k, delta, sg)
    tree1 = get_tree(sub_graphs[0])
    tree2 = get_tree(sub_graphs[1])
    tree3 = get_tree(sub_graphs[2])
    tree4 = get_tree(sub_graphs[3])
    result._add_sub_graph_(tree1)
    result._add_sub_graph_(tree2)
    result._add_sub_graph_(tree3)
    result._add_sub_graph_(tree4)
    print(result)

def init(k: int, delta : int, sg: list) :
    global sub_graphs
    global big_graph
    global result
    sub_graphs = sg
    big_graph = get_all_sub_graphs_in_one()
    result = Graph("Result")
    result._reset_()
    print(str(big_graph))

def get_all_sub_graphs_in_one() -> Graph:
    return Graph("Global", sub_graphs=sub_graphs)

def get_tree(graph : Graph) -> Graph :
    tree = Graph("Tree")
    tree._reset_()
    edge = get_edge_with_max_weight(graph._edges, tree)
    tree._add_edge_(e=edge)
    #print("first edge : {}".format(edge))

    v1 = edge._v1
    v2 = edge._v2

    v1_edges = graph._get_edges_from_vertex(v1)
    v2_edges = graph._get_edges_from_vertex(v2)

    best_edge_v1 = get_edge_with_max_weight(v1_edges, tree)
    best_edge_v2 = get_edge_with_max_weight(v2_edges, tree)
    #print("best v1 edge : {}".format(best_edge_v1))
    #print("best v2 edge : {}".format(best_edge_v2))
    #time.sleep(5)

    start = None
    best_edge = None
    if best_edge_v1 :
        start = v1
        best_edge = best_edge_v1
    if (not start) or (best_edge_v2 and best_edge_v2._weight > best_edge_v1._weight): 
        start = v2
        best_edge = best_edge_v2

    change = False
    #print("best choosen edge : {}".format(best_edge))
    if start and best_edge :
        tree._add_edge_(e=best_edge)
        start = best_edge._get_other_vertex_(start)
        change = True

    while change :
        change = False
        edges_start = graph._get_edges_from_vertex(start)
        best_edge = get_edge_with_max_weight(edges_start, tree)
        #print("best edge : {}".format(best_edge))
        if best_edge :
            tree._add_edge_(e=best_edge)
            start = best_edge._get_other_vertex_(start)
            change = True

    return tree

def get_edge_with_max_weight(edges : list, tree : Graph) -> Edge :
    #print("tree : {}".format(tree))
    edge = None
    if edges :
        i=0
        while not edge and i < len(edges):
            #"print("choosing first one")
            #print("v1 {} : {}".format(edges[i]._v1, tree._has_vertex_(edges[i]._v1)))
            #print("v2 {} : {}".format(edges[i]._v2, tree._has_vertex_(edges[i]._v2)))
            #print("*****")
            #time.sleep(1)
            if not tree :
                edge = edges[i]
            elif not tree._has_vertex_(edges[i]._v1) or not tree._has_vertex_(edges[i]._v2) :
                edge = edges[i]
            i += 1

        while i < len(edges) :
            #print("compare v1 {} : {}".format(edges[i]._v1, tree._has_vertex_(edges[i]._v1)))
            #print("compare v2 {} : {}".format(edges[i]._v2, tree._has_vertex_(edges[i]._v2)))
            #print("*****")
            if not tree or (not tree._has_vertex_(edges[i]._v1) or not tree._has_vertex_(edges[i]._v2)) :
                if edges[i]._weight > edge._weight :
                    edge = edges[i]
                    #print("choose !")
            i += 1
    return edge