# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

import math as m

def expwin(n):
    win = []
    step = 2./n
    for k in range(n+1):
        val = -1. + k*step
        win.append(m.exp(-(val*val)))
    return win

#print expwin(128)
