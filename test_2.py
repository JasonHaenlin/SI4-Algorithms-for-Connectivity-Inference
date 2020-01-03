import unittest

from ic.Vertex import Vertex
from ic.Graph import Graph
from ic.Algo_two import compute

class Test2(unittest.TestCase):

    def test_compute(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        v4 = Vertex(4)
        v5 = Vertex(5)
        v6 = Vertex(6)
        v7 = Vertex(7)
        g1 = Graph(1, True, [v1, v2])
        g2 = Graph(2, True, [v3, v4])
        g3 = Graph(3, True, [v5, v6])
        g4 = Graph(4, True, [v1, v4, v7])

        compute(k=0, delta=3, sg=[g1,g2,g3,g4])

if __name__ == '__main__':
    unittest.main()