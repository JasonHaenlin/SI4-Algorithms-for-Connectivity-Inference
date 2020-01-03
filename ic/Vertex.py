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
    tag: int
        the tag of the vertex represented as a number
    adjacents: list[Vertex]
        list of adjacents vertices
    links: list[int]
        list of links that exist between multiple graph

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
    is_other_path_available(self, vertex: Vertex) -> bool
        check if the self vertex have a path back to the destination vertex
    add_link(self, link: int)
        add a new linked graphe to the vertex
    links(self)->list[int]
        return the weight of the vertex
    """

    def __init__(self, tag: int, adjacents: list[Vertex] = []):
        """
        Parameters
        ----------
        tag: int
            the tag of the vertex represented as a number
        adjacents: list[Vertex], optional
            list of adjacents vertices
        """

        self._tag = tag
        self._links = []
        self._adjacents = []
        self._adjacents = self._validate_vertices(adjacents)

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        s = str(self._tag)
        for v in self._adjacents:
            s += "(" + str(v._tag) + ")"
        if len(self._adjacents) < 1:
            s += "()"
        return s

    def __repr__(self):
        return str(self)

    def _validate_vertices(self, vertices):
        """avoid duplication adjacents vertices"""
        a = {}
        for v in self._adjacents:
            a[v] = v
        for v in vertices:
            if v is not self:
                a[v] = v
        return [v for v in a.values()]

    def _is_there_a_path(self, vertex: Vertex, marked: dict, l: set) -> bool:
        """check for the current link, if a path back exist"""
        marked[vertex] = 1
        marked[self] += 1
        if vertex.degree() < 2:
            marked[self] -= 1
            return False

        for adj in (adj for adj in vertex.get_adjacents() if l in adj.links()):
            if adj not in marked:
                if self._is_there_a_path(adj, marked, l):
                    return True
            elif adj is self and marked[self] > 1:
                return True

        marked[self] -= 1
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

        if v not in self._adjacents:
            self._adjacents.append(v)
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

        self._adjacents = self._validate_vertices(v)
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

        self._adjacents = []
        self._adjacents = self._validate_vertices(v)
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

        self._adjacents.remove(v)
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
            return len(self._adjacents)
        return len([a for a in self._adjacents if a in included])

    def highest_degree_adjacent(self,  included: list[Vertex] = [], same_link=False) -> Vertex:
        """return the adjacent vertex with the highest degree

        Parameters
        ----------
        included: list[Vertex]
            the vertices to include in the research (the other are excluded)

        same_link: bool
            check if the adjcent vertex need to have the same links (default=False)

        Returns
        -------
        Vertex:
            highest degree vertex from the included vertices
        """
        if same_link:
            def s(adj): return len(self.intersection(adj)) > 0
        else:
            def s(adj): return True
        return max(self._adjacents, key=lambda a: a.degree() if a in included and s(a) else 0)

    def is_other_path_available(self, vertex: Vertex) -> bool:
        """check if the self vertex have a path back to the destination vertex

        It's checking if a path exist for each link on the current node

        example: if if the intersection links between self and vertex are the subcomplexe 1 and 2,
        so we need to check if an other way can reach the self node, and for each links in case they
        do not have the same path

        Parameters
        ----------
        vertex: Vertex
            destination vertex where the path need to be find

        Returns
        -------
        bool:
            True if the vertex is correctly connected, False otherwise
        """
        links = self.intersection(vertex)
        for l in links:
            marked = {}
            marked[self] = 0
            if not self._is_there_a_path(vertex, marked, l):
                return False
        return True

    def get_adjacents(self) -> list:
        """return the adjacents vertices in this Vertex

        Returns
        -------
        list:
            adjacents vertices in this Vertex
        """
        return self._adjacents.copy()

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

    def intersection(self, vertex):
        """check if the links between two vertices are the same"""
        return set(self.links()).intersection(vertex.links())
