#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from collections import Counter
from operator import itemgetter


def compute(d: int, subcomplexes: list) -> list:
    """return a new created graph

    Parameters
    ----------
    d: int
        max delta that can have a node
    subcomplexes: list
        the list of subcomplexes to build the graph

    Returns
    -------
    list:
        a new graph or None if it is not possible
    """

    if not is_degree_possible(d, subcomplexes):
        return None
    subcomplexes = convert(subcomplexes)
    graph = unify(subcomplexes)
    mini_graph = minimization(d, graph)
    return mini_graph


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
            if flyweight.get(v, None) == None:
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


def minimization(d: int, graph: list)-> list:
    """try to minimize the edges to reduce the delta to at least 'd'

    Parameters
    ----------
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
    reductible = True
    while reductible == True:
        for vertex in graph:
            reductible = False
            if try_to_reduct(vertex, graph) == True:
                reductible = True
    return graph


def try_to_reduct(v: Vertex, graph):
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
    if highest == None:
        return False
    if highest.degree() < 2:
        return False
    v.remove(highest)
    highest.remove(v)
    return True


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
    if vertex.is_other_path_available(vertex_to_test) == False:
        return None
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
    if subcomplexes == None:
        return None
    graph = {}
    for sub in subcomplexes:
        for v in sub:
            graph[v] = v
    return [v for v in graph.values()]


def verify_result(d: int, k: int, graph: list) ->bool:
    """check if the builded graph is correct

    Parameters
    ----------
    d: int
        max degree of each vertex
    k: int
        max edges of the graph
    graph: list
        list of Vertices that represent the final graph
    """
    if graph == None:
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

    if (edges/2) > k:
        return False

    return True


def something_wrong(vo, vd):
    """testing function to check if a separation between two nodes is fine"""
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
