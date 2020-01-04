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
        v8 = Vertex(8)
        v9 = Vertex(9)
        v10 = Vertex(10)
        g1 = Graph(1, True, [v4, v7, v6, v9, v1])
        g2 = Graph(2, True, [v1, v5, v10, v7, v9])
        g3 = Graph(3, True, [v3, v9, v4, v5, v7])
        #g4 = Graph(4, True, [v4, v5, v6, v7])
        #g5 = Graph(5, True, [v6, v8])
        #print(g1)
        compute(k=0, delta=3, sg=[], real_list=[g1,g2,g3])

if __name__ == '__main__':
    unittest.main()