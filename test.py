import unittest

from ic.Vertex import Vertex
from ic.Algo_one import convert, is_degree_possible, reduce_degre, compute


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
        self.assertTrue(str(vertices[0][1]) == "2(1)(3)(4)", "Should be True")

    def test_is_degree_possible(self):
        res = is_degree_possible(2, [[1, 2, 3, 4], [2, 6, 7, 8], [9, 1, 4, 6]])
        self.assertTrue(res, "Should be True")

    def test_reduce_degree(self):
        v1, v2, v3, v4 = Vertex(1), Vertex(2), Vertex(3), Vertex(4)
        v1.set_adjacents([v2, v3])
        self.assertTrue(reduce_degre(2, v1), "Should be of a good degree")
        self.assertEqual(v1.degree(), 2, "Should not have been reduced")
        self.assertTrue(reduce_degre(3, v1),
                        "Should be of a bad degree and irreducible")
        v2.set_adjacents([v1, v2, v3])
        self.assertTrue(reduce_degre(3, v1),
                        "Should be of a bad degree but reductible")
        self.assertEqual(v1.degree(), 2, "Should have been reduced")

    def test_minimization(self):
        # vertices = [[8, 5, 2, 9, 7],
        #             [4, 1, 5, 6, 3],
        #             [8, 1, 10, 9, 5],
        #             [1, 10, 9, 4, 7],
        #             [4, 7, 8, 6, 3]]
        vertices = [[1, 2, 3],
                    # [4, 5, 6],
                    [1, 5, 6, 3]]
        print(vertices)
        result = compute(2, vertices)
        print(result)


if __name__ == '__main__':
    unittest.main()
