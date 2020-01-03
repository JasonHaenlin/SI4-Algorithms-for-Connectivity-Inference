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
