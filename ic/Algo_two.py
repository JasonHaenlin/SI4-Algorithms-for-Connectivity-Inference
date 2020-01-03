#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from ic.Graph import Graph
from collections import Counter
from operator import itemgetter

def compute(k: int, delta : int, sg: list) -> list:
    init(k, delta, sg)
    tree1 = get_tree(sub_graphs[3])
    print(tree1)

def init(k: int, delta : int, sg: list) :
    global sub_graphs
    global big_graph
    global result
    sub_graphs = sg
    big_graph = get_all_sub_graphs_in_one()
    result = Graph("Result")
    print(str(big_graph))

def get_all_sub_graphs_in_one() -> Graph:
    for g in sub_graphs :
        print(g)
    return Graph("Global", sub_graphs=sub_graphs)

def get_tree(graph : Graph) -> Graph :
    tree = Graph("Tree")

    weight = big_graph._get_edge_(graph._edges[0]._v1, graph._edges[0]._v2)._weight
    edge = graph._edges[0]
    for i in range (1, len(graph._edges)):
        if big_graph._get_edge_(graph._edges[i]._v1, graph._edges[i]._v2)._weight > weight :
            weight = big_graph._get_edge_(graph._edges[i]._v1, graph._edges[i]._v2)._weight
            edge = graph._edges[i]
    
    tree._add_edge_(edge._v1, edge._v2)

    start = edge._v2
    change = True

    while change :
        change = False
        edges_start = graph._get_edges_from_vertex(start)
        for e in edges_start :
            end = e._get_other_vertex_(start)
            if not tree._has_vertex_(end) :
                tree._add_edge_(e._v1, e._v2)
                start = end
                change = True
                break

    return tree