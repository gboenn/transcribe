# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

import itertools as it

def list_combinations (allsets):
    combs = []
    for k in list(it.product(*allsets)):
        combs.append(list(k))
    return combs

