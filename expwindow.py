import math as m

def expwin(n):
    win = []
    step = 2./n
    for k in range(n+1):
        val = -1. + k*step
        win.append(m.exp(-(val*val)))
    return win

#print expwin(128)
