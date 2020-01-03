#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.0 2020/01/01 - Python 3.7
from __future__ import annotations


class Vertex(object):
    """
    A class used to represent a node of a graph with a value
    and a set of adjacent Vertex

    ...

    Attributes
    ----------
    tag : int
        the tag of the vertex represented as a number
    adjacent : list[Vertex]
        list of adjacents vertices

    Methods
    -------
    append(v : Vertex)
        append a new none existing edge as an adjacent vertex
    remove(v : Vertex)
        remove a existing vertex
    adjacent_count() -> int
        return the numbers of edges on that vertex
    highest_degree_adjacent(included : list[Vertex]) -> Vertex
        return the adjacent vertex with the highest degree
    get_adjacents() -> list[Vertex]
        return the adjacents vertices in this Vertex
    correctly_connected(dest_vertex: Vertex, included: list[Vertex] = []) -> bool
        check if the self vertex have a path back to the destination vertex
    """

    def __init__(self, tag: int, adjacent: list[Vertex] = []):
        """
        Parameters
        ----------
        tag: int
            the tag of the vertex represented as a number
        adjacent: list[Vertex], optional
            list of adjacents vertices
        """

        self._tag = tag
        self._links = []
        self._adjacent = []
        self._adjacent = self._validate_vertices(adjacent)

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        s = str(self._tag)
        for v in self._adjacent:
            s += "(" + str(v._tag) + ")"
        if len(self._adjacent) < 1:
            s += "()"
        return s

    def __repr__(self):
        return str(self)

    def _validate_vertices(self, vertices):
        a = {}
        for v in self._adjacent:
            a[v] = v
        for v in vertices:
            if v is not self:
                a[v] = v
        return [v for v in a.values()]

    def _helper_correctly_connected(self, marked: dict, dest_vertex: Vertex, included: list[Vertex] = []) -> bool:
        marked[self] = 1
        marked[dest_vertex] += 1
        if self.degree(included + [dest_vertex]) < 2:
            marked[dest_vertex] -= 1
            return False

        for a in (a for a in self._adjacent if a in included):
            if a not in marked:
                if a._helper_correctly_connected(marked, dest_vertex, included) == True:
                    return True
            elif a is dest_vertex and marked[dest_vertex] > 1:
                return True

        marked[dest_vertex] -= 1
        return False

    def append(self, v: Vertex):
        """append a new adjacent vertex

        if the vertex already exist, it will not be added

        Parameters
        ----------
        v: Vertex
            new adjacent vertex to add

        Returns
        -------
        Vertex:
            self
        """

        if v not in self._adjacent:
            self._adjacent.append(v)
        return self

    def append_all(self, v: list[Vertex]):
        """add all the adjacents vertices to the vertex

        Parameters
        ----------
        v: list[Vertex]
            new adjacent vertices to add

        Returns
        -------
        Vertex:
            self
        """

        self._adjacent = self._validate_vertices(v)
        return self

    def set_adjacents(self, v: list[Vertex]):
        """set the adjacent vertices for the vertex

        this will reset the current vertices

        Parameters
        ----------
        v: list[Vertex]
            new adjacent vertices to add

        Returns
        -------
        Vertex:
            self
        """

        self._adjacent = []
        self._adjacent = self._validate_vertices(v)
        return self

    def remove(self, v: Vertex):
        """remove a adjacent vertex

        Parameters
        ----------
        v: Vertex
            adjacent vertex to remove

        Raises
        ------
        ValueError
            if no vertex of the hash exist

        Returns
        -------
        Vertex:
            self
        """

        self._adjacent.remove(v)
        return self

    def degree(self, included: list[Vertex] = []) -> int:
        """return the number of adjacents vertices

        count the number of edges linked to the current vertex

        Parameters
        ----------
        included: list[Vertex]
            the vertices to include in the research (the other are excluded)

        Return
        ------
        int:
            count of edges
        """
        if len(included) == 0:
            return len(self._adjacent)
        return len([a for a in self._adjacent if a in included])

    def highest_degree_adjacent(self, included: list[Vertex] = []) -> Vertex:
        """return the adjacent vertex with the highest degree

        Parameters
        ----------
        included: list[Vertex]
            the vertices to include in the research (the other are excluded)

        Returns
        -------
        Vertex:
            highest degree vertex from the included vertices
        """
        if len(self._links) > 1:
            def s(dests, srcs): return len(set(dests).intersection(srcs)) <= 1
        else:
            def s(dests, srcs): return True
        return max(self._adjacent, key=lambda a: a.degree() if a in included and s(a.links(), self._links) else 0)

    def get_adjacents(self) -> list:
        """return the adjacents vertices in this Vertex

        Returns
        -------
        list:
            adjacents vertices in this Vertex
        """
        return self._adjacent

    def correctly_connected(self, dest_vertex: Vertex, included: list[Vertex] = [])->bool:
        """check if the self vertex have a path back to the destination vertex

        Parameters
        ----------
        dest_vertex: Vertex
            destination vertex where the path need to be find

        included: list[Vertex]
            the vertices to include in the research (the other are excluded)

        Returns
        -------
        bool:
            True if the vertex is correctly connected, False otherwise
        """
        to_check = included.copy()
        marked = {}
        marked[dest_vertex] = 0
        return self._helper_correctly_connected(marked, dest_vertex, to_check)

    def add_link(self, link: int):
        """add a new link

        Returns
        -------
        Vertex:
            self
        """

        self._links.append(link)
        return self

    def links(self)->list[int]:
        """return the weight of the vertex"""
        return self._links
