import unittest

from ic.Vertex import Vertex
from ic.Algo_one import convert, is_degree_possible, reduce_degre, compute, highest_removable_degree


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
        self.assertTrue(str(vertices[0][1]) ==
                        "2(1)(3)(4)(6)(7)(8)", "Should be True")

    def test_is_degree_possible(self):
        res = is_degree_possible(2, [[1, 2, 3, 4], [2, 6, 7, 8], [9, 1, 4, 6]])
        self.assertTrue(res, "Should be True")

    def test_reduce_degree(self):
        v1, v2, v3, v4 = Vertex(1), Vertex(2), Vertex(3), Vertex(4)
        v1.set_adjacents([v2, v3])
        self.assertTrue(reduce_degre(
            2, v1, [v2, v3]), "Should be of a good degree")
        self.assertEqual(v1.degree(), 2, "Should not have been reduced")
        self.assertTrue(reduce_degre(3, v1, [v2, v3]),
                        "Should be of a bad degree and irreducible")
        v2.set_adjacents([v1, v2, v3])
        self.assertTrue(reduce_degre(3, v1, [v2, v3]),
                        "Should be of a bad degree but reductible")
        self.assertEqual(v1.degree(), 2, "Should have been reduced")

    def test_correct_vertex(self):
        v1, v2, v3 = Vertex(1), Vertex(2), Vertex(3)
        v4, v5, v6 = Vertex(4), Vertex(5), Vertex(6)
        vertices = [v1, v2, v3, v4, v5, v6]
        v1.set_adjacents([v2, v3])
        v2.set_adjacents([v1, v4])
        v3.set_adjacents([v1])
        v4.set_adjacents([v2, v5, v6])
        v5.set_adjacents([v4])
        v6.set_adjacents([v4])
        self.assertFalse(v2.correctly_connected(
            v1, vertices), "Should be bad connected")
        v1.append(v5)
        v5.append(v1)
        self.assertTrue(v2.correctly_connected(
            v1, vertices), "Should be connected correctly")

    def test_highest_removable_degreee(self):
        v1, v2, v3 = Vertex(1), Vertex(2), Vertex(3)
        v4, v5, v6 = Vertex(4), Vertex(5), Vertex(6)
        vertices = [v1, v2, v3, v4, v5, v6]
        v1.set_adjacents([v2, v5, v6])
        v2.set_adjacents([v1, v3, v4])
        v3.set_adjacents([v2])
        v4.set_adjacents([v2])
        v5.set_adjacents([v1, v6])
        v6.set_adjacents([v1, v5])

        vertex = highest_removable_degree(v1, vertices)
        self.assertTrue(vertex is v5 or vertex is v6,
                        "Should be able to remove vertex 6 or 5")
        v7 = Vertex(7)
        v7.set_adjacents([v1, v3])
        v1.append(v7)
        v3.append(v7)

        vertex = highest_removable_degree(v1, vertices)
        self.assertTrue(vertex is v5 or vertex is v6,
                        "Should be able to remove vertex 6 or 5")

    def test_minimization(self):
        vertices = [
            [8, 5, 2, 9, 7],
            [4, 1, 5, 6, 3],
            [8, 1, 10, 9, 5],
            [1, 10, 9, 4, 7],
            [4, 7, 8, 6, 3],
        ]
        print(vertices)
        result = compute(3, vertices)
        print(result)


if __name__ == '__main__':
    unittest.main()
