#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from collections import Counter
from operator import itemgetter
from random import shuffle


def compute(k: int, d: int, subcomplexes: list) -> list:
    """return a new created graph

    the function is checking if the degree can be reach,
    otherwise it returns None.
    It convert the 2D list into list of vertices and unify it
    to build a unique graph which include all the subcomplexes.
    return a minimized graph

    Parameters
    ----------
    k: int
        max edges that the graph should have
    d: int
        max delta that can have a node

    subcomplexes: list
        the list of subcomplexes to build the graph

    Returns
    -------
    list:
        a new graph as a list of Vertex or None if it is not possible
    """

    # if not is_degree_possible(d, subcomplexes):
    #     return None
    subcomplexes = convert(subcomplexes)
    graph = unify(subcomplexes)
    return minimization(k, d, graph)


def convert(subcomplexes: list) -> list:
    """return the list of value into complete graphs
    Parameters
    ----------
    subcomplexes: list
        the list of subcomplexes to build the graph

    Returns
    -------
    list:
        list of vertices fully linked for each subcomplex
    """
    sets = []
    flyweight = {}
    link_count = 1
    for sub in subcomplexes:
        vs = []
        for v in sub:
            if not flyweight.get(v, None):
                flyweight[v] = Vertex(v).add_link(link_count)
            else:
                flyweight[v].add_link(link_count)
            vs.append(flyweight[v])
        sets.append([v.append_all(vs) for v in vs])
        link_count += 1
    return sets


def is_degree_possible(d: int, subcomplexes: list) -> bool:
    """return the condition result

    Parameters
    ----------
    d: int
        the maximal degree the vertices can have

    subcomplexes: list
        the list of subcomplexes to build the graph

    Returns
    -------
    bool:
        True if the degree is enough, otherwise False if is it not possible
    """
    whole = []
    [whole.extend(s) for s in subcomplexes]
    return max(Counter(whole).items(), key=itemgetter(1))[1] <= d


def minimization(k: int, d: int, graph: list)-> list:
    """try to minimize the edges to reduce the delta to at least 'd'

    Parameters
    ----------
    k: int
        the minimal edges to reduce to

    d: int
        the minimal degre to reduce to

    graph: list
        the graph with the vertices

    Returns
    -------
    list:
        list of vertices minimized or None if no solution is found
    """
    graph = graph.copy()
    graph.sort(key=lambda v: v.over_edges(), reverse=True)
    edges = sum(v.degree() for v in graph)/2
    i = 0
    while i < len(graph):
        vertex = graph[i]
        while vertex.degree() > d or edges > k:
            if not reduction(vertex, graph):
                break
            else:
                edges -= 1
            vertex = swap_if_possible(graph, i)
        i += 1

    return graph


def reduction(v: Vertex, graph):
    """reduce the vertex edges to fit the degree

    Parameters
    ----------

    v: Vertex
        the target vertex who need to be reduce

    graph: list[Vertex]
        pass the all the graph

    Returns
    -------
    bool:
        False if the vertex could not be reduced, True otherwise

    """
    highest = best_choice_to_remove(v, graph)
    if not highest:
        return False
    if highest.degree() < 2:
        return False
    v.remove(highest)
    highest.remove(v)
    return True


def swap_if_possible(graph: list, start: int)->Vertex:
    """simple function to sort element to retrieve the biggest one"""
    i = start
    while i < len(graph)-1:
        if graph[i].over_edges() < graph[i+1].over_edges():
            graph[i], graph[i+1] = graph[i+1], graph[i]
        i += 1
    return graph[start]


def best_choice_to_remove(vertex: Vertex, graph) -> Vertex:
    """try to minimize the edges to reduce the delta

    Parameters
    ----------
    vertex: Vertex
        the vertex to reduce

    graph: list
        the graph with the vertices

    Returns
    -------
    list:
        list of vertices minimized or None if no solution is found
    """
    adj = vertex.get_adjacents()
    vertex_to_test = vertex.highest_degree_adjacent(
        included=adj,
        same_link=True
    )
    while not vertex.is_other_path_available(vertex_to_test):
        adj.remove(vertex_to_test)
        if len(adj) < 1:
            return None
        vertex_to_test = vertex.highest_degree_adjacent(
            included=adj,
            same_link=True
        )
    return vertex_to_test


def unify(subcomplexes: list) -> list:
    """return a fully unified graph from the subsets

    Parameters
    ----------
    subcomplexes: list
        the list of sub graphes

    Returns
    -------
    list:
        the new graph
    """
    if not subcomplexes:
        return None
    graph = {}
    for sub in subcomplexes:
        for v in sub:
            graph[v] = v
    return [v for v in graph.values()]


def verify_result(k: int, d: int, graph: list) ->bool:
    """check if the builded graph is correct

    Parameters
    ----------
    k: int
        max edges of the graph
    d: int
        max degree of each vertex
    graph: list
        list of Vertices that represent the final graph
    """
    if not graph:
        return False
    edges = 0
    for vertex in graph:
        edges += vertex.degree()
        if vertex.degree() > d:
            return False
        origin = set(vertex.links())
        linked_to = vertex.get_adjacents()
        links = set()
        for l in linked_to:
            links = links.union(l.links())
        if len(origin.intersection(links)) != len(origin):
            return False

    # print("edges : " + str(edges/2))
    if (edges/2) > k:
        return False

    return True


def something_wrong(vo, vd):
    """testing function to check if a separation between two nodes is fine

    Testing purpose only

    """

    vos = vo.get_adjacents()
    vos.remove(vd)
    vds = vd.get_adjacents()
    vds.remove(vo)

    src = set(vo.links())
    dest = set(vd.links())
    deep_links = src.intersection(dest)

    links = set()
    for a in vos:
        links = links.union(a.links())
    if len(src.intersection(links)) != len(src):
        vos.append(vd)
        vds.append(vo)
        return True

    links = set()
    for a in vds:
        links = links.union(a.links())
    if len(dest.intersection(links)) != len(dest):
        vos.append(vd)
        vds.append(vo)
        return True

    vos.append(vd)
    vds.append(vo)
    return False
