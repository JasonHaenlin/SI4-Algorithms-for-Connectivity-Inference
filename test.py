import unittest

from ic.Vertex import Vertex
from ic.Algo_one import convert, is_degree_possible, compute, verify_result, reduction


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

    def test_reduction(self):
        v1, v2, v3, v4 = Vertex(1), Vertex(2), Vertex(3), Vertex(4)
        v1.set_adjacents([v2, v3])
        self.assertFalse(reduction(v1, [v2, v3]), "Should be of a good degree")
        self.assertEqual(v1.degree(), 2, "Should not have been reduced")
        self.assertEqual(v1.degree(), 2, "Should have been reduced")

    def test_minimization(self):
        vertices = [
            [1, 2, 6],
            [1, 3, 5],
            [3, 4, 5],
        ]
        result = compute(2, vertices)

        vertices = [
            [1, 8, 4],
            [7, 3, 2],
            [7, 3, 8],
        ]

        result = compute(2, vertices)

        vertices = [
            [8, 5, 2, 9, 7],
            [4, 1, 5, 6, 3],
            [8, 1, 10, 9, 5],
            [1, 10, 9, 4, 7],
            [4, 7, 8, 6, 3],
        ]
        result = compute(5, vertices)

        vertices = [
            [12, 51, 58, 73, 39, 52, 57, 11, 4, 22, 28, 85, 44, 24, 9],
            [71, 90, 7, 23, 11, 31, 14, 53, 55, 2, 91, 28, 98, 37, 88],
            [16, 95, 43, 76, 12, 44, 90, 55, 28, 6, 20, 94, 100, 79, 4],
            [58, 14, 97, 77, 59, 11, 43, 57, 64, 35, 38, 17, 40, 48, 79],
            [25, 65, 83, 99, 59, 100, 28, 43, 92, 50, 58, 44, 69, 79, 67],
            [71, 39, 17, 93, 4, 85, 11, 8, 95, 27, 28, 31, 81, 12, 72],
            [16, 88, 78, 82, 59, 40, 93, 51, 76, 21, 8, 90, 44, 67, 1],
            [82, 50, 32, 17, 4, 48, 8, 58, 87, 71, 94, 84, 19, 38, 20],
            [75, 25, 85, 36, 23, 13, 55, 73, 10, 91, 60, 41, 5, 28, 72],
            [31, 32, 78, 68, 46, 72, 71, 54, 45, 66, 13, 23, 81, 14, 43],
            [56, 13, 18, 5, 30, 40, 1, 61, 69, 99, 24, 55, 11, 47, 9],
            [13, 17, 78, 32, 8, 69, 30, 94, 96, 24, 82, 73, 58, 50, 62],
            [6, 60, 5, 47, 76, 37, 24, 44, 40, 63, 59, 39, 15, 21, 83],
            [67, 12, 84, 23, 86, 57, 9, 21, 52, 27, 8, 51, 49, 69, 95],
            [8, 40, 77, 46, 30, 18, 33, 81, 44, 71, 20, 27, 45, 43, 83],
            [97, 35, 31, 14, 80, 8, 85, 29, 66, 5, 76, 33, 60, 84, 2],
            [11, 82, 15, 55, 19, 20, 33, 91, 74, 65, 81, 84, 72, 31, 80],
            [20, 78, 95, 68, 32, 25, 86, 70, 76, 23, 77, 98, 26, 63, 44],
            [95, 87, 86, 25, 78, 32, 55, 29, 71, 61, 3, 28, 11, 76, 47],
            [96, 27, 55, 42, 88, 33, 100, 37, 26, 45, 95, 53, 18, 65, 51]
        ]
        print(vertices)
        result = compute(10, vertices)
        print(verify_result(10, 10000, result))


if __name__ == '__main__':
    unittest.main()
