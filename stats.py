from ic.__main__ import random_instance
from ic.Algo_one import compute, verify_result
# from ic.Algo_two import compute, verify_result


if __name__ == "__main__":
    _iteration = 100
    _p = 20
    _t = 10
    _k = {
        "start": 100,
        "end": 550,
        "step": 50,
    }

    _d = {
        "start": 2,
        "end": 10,
        "step": 1,
    }

    print("{0:<6}".format("|"), end='|')
    for k in range(_k["start"], _k["end"]+1, _k["step"]):
        print("{0:^6}".format(k), end='|')
    for d in range(_d["start"], _d["end"]+1, _d["step"]):
        print()
        print("|{0:^5}".format(d), end='|')
        for k in range(_k["start"], _k["end"]+1, _k["step"]):
            corrects = 0
            for _ in range(_iteration):
                inst = random_instance(_p, _t)
                graph = compute(k, d, inst)
                if verify_result(k, d, graph):
                    corrects += 1
            print("{0:^6}".format(corrects), end='|')
