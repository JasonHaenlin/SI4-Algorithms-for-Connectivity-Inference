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
    mini_graph = minimization_graph(d, graph)
    # mini_graph = minimization_graph(d, mini_graph)
    # graph = minimization(d, subcomplexes)
    return graph


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


def minimization_graph(d: int, graph: list)-> list:
    """just a test right now"""
    graph = graph.copy()
    reductible = True
    while reductible == True:
        for vertex in graph:
            reductible = False
            if try_to_reduct(vertex, graph) == True:
                reductible = True
    return graph


def try_to_reduct(v: Vertex, graph):
    highest = best_choice_to_remove(v, graph)
    if highest == None:
        return False
    if highest.degree() < 2:
        return False
    v.remove(highest)
    highest.remove(v)
    return True


def best_choice_to_remove(vertex: Vertex, graph) -> Vertex:
    adj = vertex.get_adjacents()
    vertex_to_test = vertex.highest_degree_adjacent(
        included=adj,
        same_link=True
    )
    if vertex.is_other_path_available(vertex_to_test) == False:
        return None
    return vertex_to_test


def minimization(d: int, subcomplexes: list) -> list:
    """try to minimize the edges to reduce the delta to at least 'd'

    Parameters
    ----------
    d: int
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
            while v.degree() > d:
                if reduction(d, v, vertices[cpt]) == False:
                    break
        cpt += 1
    return vertices


def reduction(d: int, v: Vertex, sub) -> bool:
    """reduce the vertex edges to fit the degree

    Parameters
    ----------
    d: int
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
    if v.degree() <= d:
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
    while vertex_to_test.correctly_connected(v) == False:
        included.remove(vertex_to_test)
        if len(included) < 1:
            return None
        vertex_to_test = v.highest_degree_adjacent(included)
        if vertex_to_test not in included:
            return Nones
    return vertex_to_test


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
