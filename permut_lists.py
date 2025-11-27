import itertools as it

def list_combinations (allsets):
    combs = []
    for k in list(it.product(*allsets)):
        combs.append(list(k))
    return combs

