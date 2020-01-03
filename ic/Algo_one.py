#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7

from ic.Vertex import Vertex
from collections import Counter
from operator import itemgetter


def compute(k: int, subcomplexes: list) -> list:
    """return a new created graph

    Parameters
    ----------
    k: int
        max delta that can have a node
    subcomplexes: list
        the list of subcomplexes to build the graph

    Returns
    -------
    list:
        a new graph or None if it is not possible
    """

    if not is_degree_possible(k, subcomplexes):
        return None
    subcomplexes = convert(subcomplexes)
    graph = minimization(k, subcomplexes)
    return unify(graph)


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


def is_degree_possible(k: int, subcomplexes: list) -> bool:
    """return the condition result

    Parameters
    ----------
    k: int
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
    return max(Counter(whole).items(), key=itemgetter(1))[1] <= k


def minimization(k: int, subcomplexes: list) -> list:
    """try to minimize the edges to reduce the delta to at least 'k'

    Parameters
    ----------
    k: int
        the minimal degre to reduce to

    subcomplexes: list
        the list of sub graphes

    Returns
    -------
    list:
        list of vertices minimized or None if no solution is found
    """

    vertices = subcomplexes.copy()

    cpt = 0
    while cpt < len(vertices):
        for v in vertices[cpt]:
            while v.degree() > k:
                if reduction(k, v, vertices[cpt]) == False:
                    break
        cpt += 1
    return vertices


def reduction(k: int, v: Vertex, sub) -> bool:
    """reduce the vertex edges to fit the degree

    Parameters
    ----------
    k: int
        the degree to reach after the reduction

    v: Vertex
        the target vertex who need to be reduce

    sub: list[Vertex]
        pass the all subcomplexe to avoid touching the others

    Returns
    -------
    bool:
        False if the vertex could not be reduced, True otherwise

    """
    if v.degree() <= k:
        return True
    highest = highest_removable_degree(v, sub)
    if highest == None:
        return False
    if highest.degree() < 2:
        return False
    v.remove(highest)
    highest.remove(v)
    return True


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


def highest_removable_degree(v: Vertex, sub) -> Vertex:
    """return a node that can be remove

    Search for a node that can be deleted

    Parameters
    ----------
    v: Vertex
        the target vertex who need to be reduce

    sub: list[Vertex]
        pass the all subcomplexe to avoid touching the others

    Returns
    -------
    Vertex:
        return a vertex that can be remove or None
    """
    included = sub.copy()
    vertex_to_test = v.highest_degree_adjacent(included)
    if vertex_to_test not in included:
        return None
    while vertex_to_test.correctly_connected(v, included) == False:
        included.remove(vertex_to_test)
        if len(included) < 1:
            return None
        vertex_to_test = v.highest_degree_adjacent(included)
        if vertex_to_test not in included:
            return None
    return vertex_to_test


def verify_result(k: int, graph: list) ->bool:
    """check if the builded graph is correct

    Parameters
    ----------
    k: int
        max degree of each vertex
    graph: list
        list of Vertices that represent the final graph
    """

    if graph == None:
        return False
    for vertex in graph:
        if vertex.degree() > k:
            return False
        origin = set(vertex.links())
        linked_to = vertex.get_adjacents()
        links = set()
        for l in linked_to:
            links = links.union(l.links())
        if len(origin.intersection(links)) != len(origin):
            return False

    return True
