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
    for sub in subcomplexes:
        vs = []
        for v in sub:
            if flyweight.get(v, None) == None:
                flyweight[v] = Vertex(v)
            vs.append(flyweight[v])
        sets.append([v.append_all(vs) for v in vs])
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

    vertices = subcomplexes
    for sub in vertices:
        for v in sub:
            while v.degree() > k:
                if reduce_degre(k, v, sub) == False:
                    break
    return vertices


def reduce_degre(k: int, v: Vertex, sub) -> bool:
    """reduce the vertex edges to fit the degre

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
    highest = v.highest_degree_adjacent(sub)
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
