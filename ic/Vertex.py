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
        self._adjacent = self._validate_vertices(adjacent)

    def __hash__(self):
        return hash(self._tag)

    def __str__(self):
        return str(self._tag)

    def __repr__(self):
        return str(self._tag)

    def __eq__(self, e):
        return self._tag == e._tag

    def _validate_vertices(self, vertices):
        return [v for v in vertices if v != self]

    def append(self, v: Vertex):
        """append a new adjacent vertex

        if the vertex already exist, it will not be added

        Parameters
        ----------
        v: Vertex
            new adjacent vertex to add
        """

        if v not in self._adjacent:
            self._adjacent.append(v)
        return self

    def set_adjacents(self, v: list[Vertex]):
        """set the adjacent vertices for the vertex

        this will reset the current vertices

        Parameters
        ----------
        v: list[Vertex]
            new adjacent vertices to add
        """

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
        """

        self._adjacent.remove(v)
        return self

    def degree(self) -> int:
        """return the number of adjacents vertices

        count the number of edges linked to the current vertex

        Return
        ------
        int:
            count of edges
        """

        return len(self._adjacent)
