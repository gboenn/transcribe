import math as m
from primes_tab import *

def digest(x):
    #modiication to 0->1 and 1->1
    #if (x == 0.):
    #    return 0.
    if (x == 0.):
        return 1.
    if (x == 1.):
        return 1.

    result = 0. 
    i = 0 
    exponent = 0 
    while (i < MAX_PRIMES): 
        prime = primes[i]
        if (x == prime):
            result += (((prime - 1)*(prime - 1)) / float(prime))
            return (result * 2.)
        while ((x % prime) == 0):
            exponent += 1
            x /= prime
        if (exponent):
            result += (exponent * (((prime - 1)*(prime - 1)) / float(prime)))
        i += 1
        exponent = 0
    return (result * 2.) 

#for k in range(17):
#    print k, digest(k)

