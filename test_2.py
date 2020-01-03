import unittest

from ic.Vertex import Vertex
from ic.Graph import Graph
from ic.Algo_two import compute

class Test2(unittest.TestCase):

    def test_compute(self):
        print("test2")
        compute(3)

    def test_init(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        v4 = Vertex(4)
        v5 = Vertex(5)
        v6 = Vertex(6)
        v7 = Vertex(7)
        g1 = Graph(1, True, [v1,v2,v3])
        g2 = Graph(2, True, [v2,v4, v5])
        g3 = Graph(3, True, [v3, v4, v5])
        g4 = Graph(4, True, [v4, v5, v6, v7])
        print(str(g1))
        print(str(g2))
        print(str(g3))
        print(str(g4))

        gGlobal = Graph(5, sub_graphs=[g1, g2, g3, g4])
        print(str(gGlobal))

if __name__ == '__main__':
    unittest.main()