import unittest

from ic.Vertex import Vertex
from ic.Algo_one import convert, is_degree_possible


class Test(unittest.TestCase):

    def test_vertex_adjacents(self):
        v1 = Vertex(1)
        self.assertEqual(v1.degree(), 0, "Should be 0")

        v2 = Vertex(2, [v1])
        v3 = Vertex(3, [v1, v2, v2])
        self.assertEqual(v3.degree(), 2, "Should be 2")

        v4 = Vertex(4, [v1, v2, v3])
        v1.set_adjacents([v1, v2, v3, v4])

        self.assertEqual(v3.highest_degree_adjacent(), v1, "Should be v1")

    def test_convert(self):
        vertices = convert([[1, 2, 3, 4], [2, 6, 7, 8]])
        self.assertTrue(vertices[0][1] is vertices[1][0], "Should be True")

    def test_is_degree_possible(self):
        res = is_degree_possible(2, [[1, 2, 3, 4], [2, 6, 7, 8], [9, 1, 4, 6]])
        self.assertTrue(res, "Should be True")


if __name__ == '__main__':
    unittest.main()
