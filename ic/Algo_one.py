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

    if not is_degree_possible(vertices):
        return None
    vertices = convert(subcomplexes)


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
    for sub in subcomplexes:
        vs = [Vertex(v) for v in sub]
        sets.append([v.set_adjacents(vs) for v in vs])
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
