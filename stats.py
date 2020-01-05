from ic.__main__ import random_instance
from ic.Algo_one import compute, verify_result
from multiprocessing import Process, Lock
# from ic.Algo_two import compute, verify_result


def prt(log, lock):
    with lock:
        print(log)


def task(_iteration, _t, _p, _k, _d, lock):
    log = ""
    for d in range(_d["start"], _d["end"]+1, _d["step"]):
        log += "\n"
        log += "|{0:^5}".format(d) + "|"
        for k in range(_k["start"], _k["end"]+1, _k["step"]):
            corrects = 0
            for _ in range(_iteration):
                inst = random_instance(_p, _t)
                graph = compute(k, d, inst)
                if verify_result(k, d, graph):
                    corrects += 1
            log += "{0:^6}".format(int((corrects/_iteration)*100)) + "|"
    prt(log, lock)


if __name__ == "__main__":
    _lock = Lock()
    _iteration = 5
    _t = 30
    _p = 15
    _k = {
        "start": 150,
        "end": 350,
        "step": 20,
    }

    _d = {
        "start": 5,
        "end": 20,
        "step": 2,
    }

    print("{0:<6}".format("|"), end='|')
    for k in range(_k["start"], _k["end"]+1, _k["step"]):
        print("{0:^6}".format(k), end='|')

    step = int((int((_d["end"]-_d["start"])/4))
               + ((_d["end"]-_d["start"]) % 2))
    last = _d["start"]
    processes = []
    for i in range(_d["start"], _d["end"], step):
        processes.append(Process(target=task,
                                 args=[_iteration, _t, _p, _k,
                                       {"start": last, "end": i,
                                           "step": _d["step"]},
                                       _lock,
                                       ]
                                 )
                         )
        last = i

    [process.start() for process in processes]
    [process.join() for process in processes]
