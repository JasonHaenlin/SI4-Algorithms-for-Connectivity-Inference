# SI4-Algorithms-for-Connectivity-Inference

Algorithms for Connectivity Inference with application in computational structural biology

## About

The objective of this project is to develop efficient algorithms to determine the contacts between proteins of the same molecular assembly.

As part of a university project within the Polytech Nice Sophia Engineering School, France.

## Directory

    - ic
        - __main__.py (genarte random instances and run the algorithm)
        - Graph.py (used by algo 2)
        - Edge.py (used by algo 2)
        - Vertex.py (used by algo 1 and 2)
        - Algo_two.py
        - Algo_one.py
    - stats.py (automated statistics over a range of values)
    - test_algo_one.py (file used to test the first algorithm)
    - test_algo_two.py (file used to test the second algorithm)

## Module

### requirement

**Python** need to be at least **version 3.7**

install numpy

```bash
# windows
pip install numpy
# or
pip3 install numpy
```

### usage

```bash
# help
python -m ic -h
# execute first algo
python -m ic -i 100 -p 10 -t 20 -d 5 -k 150 -a 1
# execute first algo
python -m ic -i 100 -p 10 -t 20 -d 5 -k 150 -a 2
```

`-i 100` : to run the algorithm 100 times

`-p 10` : to create each subcomplexes with 10 vertex

`-t 20` : to create 20 subcomplexes

`-d 5` : the minimum degree the final graph should have

`-k 150` : the maximum number of edges the graph should have

`-a 2` : to run the second algorithm

## supervisors

>Johny Bond
>
>Dorian Mazauric
>
>Christophe Papazian
>
>Stéphane Pérenne

## Team

>Myriam Zekri : [github/Myriam19](https://github.com/Myriam19)
>
>Charles Roger : [github/CharlesRoger62](https://github.com/CharlesRoger62)
>
>Florian Aïnadou : [github/FlorianAinadou](https://github.com/FlorianAinadou)
>
>Jason Haenlin : [github/JasonHaenlin](https://github.com/JasonHaenlin)
