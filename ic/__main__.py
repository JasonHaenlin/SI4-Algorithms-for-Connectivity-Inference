#!/usr/bin/python
# -*- coding: UTF-8 -*-

# V1.2 2019/12/31 - Python 3.X

import argparse
from random import sample
from sys import argv

VMIN = 1
VMAX = 100


def random_instance(p, t):
    return [sample(range(VMIN, VMAX+1), p) for _ in range(t)]


def main():
    main_parser = argparse.ArgumentParser()
    main_parser.add_argument("-v",
                             "--vertex",
                             help="number of vertex [1, 100]",
                             type=int,
                             default=10,
                             )
    main_parser.add_argument("-c",
                             "--subcomplexes",
                             help="number of subcomplexes to create [1, +inf]",
                             type=int,
                             default=5,
                             )
    args = main_parser.parse_args(argv[1:])
    if args.subcomplexes < 1:
        main_parser.error('--subcomplexes should not be < 1')
    if args.vertex < 1 or args.vertex > 100:
        main_parser.error('--vertex should not be between 1 and 100')

    inst = random_instance(args.vertex, args.subcomplexes)

    print(inst)


if __name__ == "__main__":
    main()
