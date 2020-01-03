#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.2 2019/12/31 - Python 3.7

import argparse
from random import sample
from sys import argv
from ic.Algo_one import compute, verify_result


def random_instance(p: int, t: int, vmin: int = 1, vmax: int = 100) -> list:
    """Return the generate instances.

    Create t number of instances from vmin (included) to vmax (included).
    Each instances contains p elements chose randomly

    Parameters
    ----------
    p: int
        numbers of vertices in each subcomplex
    t: int
        numbers of instances to create
    vmin: int
        min value range in the whole
    vmax: int
        max value range in the whole

    Returns
    -------
    int[]:
        Array containing all the instances represented by Arrays of int

    """
    return [sample(range(vmin, vmax+1), p) for _ in range(t)]


def main():
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("-p",
                             "--vertex",
                             help="number of vertex [1, 100]",
                             type=int,
                             default=10,
                             )
    main_parser.add_argument("-t",
                             "--subcomplexes",
                             help="number of subcomplexes to create [1, +inf]",
                             type=int,
                             default=5,
                             )
    main_parser.add_argument("-d",
                             "--degree",
                             help="the minimal degree the vertices should be",
                             type=int,
                             default=3,
                             )
    main_parser.add_argument("-k",
                             "--maxedges",
                             help="the maximal numbers of edges the graph should have",
                             type=int,
                             default=3,
                             )
    main_parser.add_argument("-i",
                             "--iteration",
                             help="the number of iteration",
                             type=int,
                             default=1,
                             )
    args = main_parser.parse_args(argv[1:])
    if args.subcomplexes < 1:
        main_parser.error('--subcomplexes should not be < 1')
    if args.iteration < 1:
        main_parser.error('--iteration should not be < 1')
    if args.degree < 1:
        main_parser.error('--degree should not be < 1')
    if args.maxedges < 1:
        main_parser.error('--maxedges should not be < 1')
    if args.vertex < 1 or args.vertex > 100:
        main_parser.error('--vertex should not be between 1 and 100')

    print("p :" + str(args.vertex) + "\tt :" + str(args.subcomplexes))
    corrects = 0
    for _ in range(args.iteration):
        inst = random_instance(args.vertex, args.subcomplexes)
        # print(inst)
        if verify_result(args.degree, args.maxedges, compute(args.degree, inst)) == True:
            corrects += 1
    print(str(corrects) + "/" + str(args.iteration))


if __name__ == "__main__":
    main()


vertices = [
    [36, 34, 55, 64, 17, 2, 73, 20, 38, 39],
    [30, 41, 70, 40, 11, 95, 53, 34, 33, 48],
    [85, 27, 75, 13, 38, 40, 70, 24, 60, 55],
    [76, 47, 39, 90, 71, 57, 56, 70, 93, 22],
    [23, 73, 64, 30, 37, 69, 88, 84, 65, 5],
    [56, 15, 67, 24, 3, 86, 71, 81, 79, 38],
    [23, 61, 36, 44, 97, 45, 52, 87, 14, 8],
    [52, 75, 58, 84, 16, 32, 67, 99, 18, 59],
    [97, 32, 14, 5, 61, 34, 49, 75, 79, 78],
    [72, 43, 99, 61, 21, 100, 64, 86, 91, 28],
    [79, 25, 95, 42, 46, 3, 52, 33, 70, 66],
    [65, 29, 69, 12, 48, 20, 91, 23, 35, 25],
    [53, 65, 51, 54, 91, 20, 27, 42, 56, 96],
    [29, 100, 68, 80, 66, 5, 61, 76, 51, 10],
    [55, 34, 91, 41, 17, 78, 88, 81, 84, 100],
    [16, 97, 44, 93, 38, 40, 79, 91, 30, 63],
    [32, 61, 86, 20, 92, 80, 40, 75, 17, 19],
    [22, 72, 2, 25, 26, 63, 97, 32, 3, 83],
    [87, 7, 21, 12, 58, 56, 5, 49, 36, 2],
    [78, 29, 74, 75, 17, 30, 68, 89, 33, 86]
]
