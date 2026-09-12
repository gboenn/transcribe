# cost.py
# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

from math import sqrt, fabs
from digest import *
from float_to_ratio_func import *

#s1 = [0.3333333333333333, 0.3333333333333333, 0.041666666666666664, 0.041666666666666664, 0.16666666666666666, 0.08333333333333333]
#s2 = [0.3125, 0.3125, 0.041666666666666664, 0.041666666666666664, 0.20833333333333334, 0.08333333333333333]
#s3 = [0.28125, 0.28125, 0.046875, 0.046875, 0.21875, 0.125]

def cost_fun(a):
    #accumulated durations
    #digestibility of an integer (denominator)
    #small value => high digestibility (low complexity)
    temp = []
    col = 0.
    dig = 0.
    for k in range(len(a)):
        col = col + fabs(a[k])
        temp.append(col)
    for k in range(len(temp)):
        ratio = float2ratio(temp[k])
        #print (digest(ratio[1]))
        dig = dig + digest(ratio[1])
    return dig

#print cost_fun(s1)
#print cost_fun(s2)
#print cost_fun(s3)

def cost_fun_harm(a):
    # uses Barlow's Digestibility function
    # This is my rhythmic impact measure RIM
    temp = []
    col = 0.
    dig = 0.
    for k in range(len(a)):
        col = col + fabs(a[k])
        temp.append(col)
    for k in range(len(temp)):
        ratio = float2ratio(temp[k])
        r = fabs(digest(ratio[0])) + digest(ratio[1])
        #print (r)
        dig = dig + r
    return (dig/len(a))
    
def cost_fun_harm2(a):
    # uses Barlow's Digestibility function
    # This is my rhythmic impact measure RIM
    # NEW: this version of the function is now symmetric around x = 0.5
    temp = []
    col = 0.
    dig = 0.
    for k in range(len(a)):
       col = col + fabs(a[k])
       temp.append(col)
    for k in range(len(temp)):
        d = temp[k]
        if (d < 0.5):
            d = 1. - d
        ratio = float2ratio(d)
        r = fabs(digest(ratio[0])) + digest(ratio[1])
#        print (d, ratio, r)
        dig = dig + r
    return (dig/len(a))

def cost_fun_harm3(a):
    # uses Barlow's Digestibility function
    # This is my rhythmic impact measure RIM
    # NEW: this version of the function is now symmetric around x = 0.5
    # NEW gives absolute rim val absRIM
    temp = []
    col = 0.
    dig = 0.
    for k in range(len(a)):
       col = col + fabs(a[k])
       temp.append(col)
    for k in range(len(temp)):
        d = temp[k]
        if (d < 0.5):
            d = 1. - d
        ratio = float2ratio(d)
        r = fabs(digest(ratio[0])) + digest(ratio[1])
#        print (temp[k], r)
        dig = dig + r
    return (dig) #(dig/len(a))
    
def cost_fun_euclid(a,b):
    #euclidean distance
    #small value => small distance
    if (len(a) == 1):
        #return 1.0
        return 0.1
    col = 0.
    for k in range(len(a)):
        d = a[k] - b[k]
        d = d * d
        col = col + d
    col = sqrt(col)
    return col


def cost_fun_ratios(a):
    # ratios between durations
    col = 0.
    for k in range(len(a)-1):
        ratio = fabs(a[k]) / fabs(a[k+1])
        frac = float2ratio(ratio)
        r = fabs(digest(frac[0])) + digest(frac[1])
#        print (ratio, r)
        if (r > 0.):
            col = col + (1. / r)
    return col

def cost_fun_ratios3(a):
    # ratios between durations
    col = 0.
    for k in range(len(a)-1):
        ratio = fabs(a[k]) / fabs(a[k+1])
        frac = float2ratio(ratio)
        r = fabs(digest(frac[0])) + digest(frac[1])
#        print (ratio, r)
        col = col + r
    return col

def cost_fun_ratios2(a):
    # ratios between durations
    col = 0.
    for k in range(len(a)-1):
        ratio = fabs(a[k]) / fabs(a[k+1])
        frac = float2ratio(ratio)
        r = fabs(digest(frac[0])) + digest(frac[1])
        #print (r)
        if (r > 0.):
            col = col + (1. / r)
    return (col / len(a))
    
def cost_fun_numerator(a):
    #digestibility of an integer (numerator)                     
    dig = 0.
    for k in range(len(a)):
        ratio = float2ratio(fabs(a[k]))
        #print (digest(ratio[0]))
        dig = dig + fabs(digest(ratio[0]))
    return dig


def cost_fullbar(a):
    #accumulated durations == 1?
    col = 0.
    for k in range(len(a)):
        col = col + fabs(a[k])

    return col


# def beat_align_test (d):
#     accum = [0.]
#     iacc = []
#     weight = 0.
#     for t in d:
#         last = accum[-1]
#         accum.append (fabs(t)+last)
#     for t in accum:
#         iacc.append (int(t * 10000.))

#     for t in iacc:
#         if (t == 3333 or t == 6666): #1/3 2/3
#             weight += 1.
#         elif (t == 5000 or t == 4999): #1/2
#             weight += 0.5
#         elif (t == 8332 or t == 8333): #5/6
#             weight += 0.5
#         elif (t == 1662 or t == 1666): #1/6 new
#             weight += 0.5

# #    print (iacc, weight)
#     return weight
    
def beat_align_test2 (d, s):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (fabs(t)+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for i in range(len (iacc)):
        t = iacc[i]
        r = ""
        if (i < len(s)):
            r = s[i]
        shortlong = 1.
        if (i < (len(d) - 1)):
            shortlong = d[i] - d[i+1] # mark where the next duration is shorter than the current dur
        if (t == 0 or t == 5000 or t == 4999): # 0 and 1/2
            weight += 1.
            if (shortlong < 0.):
                weight -= 0.25
        elif (t == 2500 or t == 2499): #1/4
            weight += 1.
            if (shortlong < 0.):
            # if the second dur after beat 2 is aligned with beat 3:
#                if ((shortlong + 1.) < 0.):
                weight -= 0.25
        elif (t == 7500 or t == 7499): #3/4
            weight += 1.
            if (shortlong < 0.):
                weight -= 0.25
#        elif (t == 8332 or t == 8333): #5/6
#            weight += 0 #0.25 ???
#        elif (t == 1667 or t == 1666): #1/6 new
#            weight += 0 #0.25 ???

#    print (iacc, weight)
    return weight


def beat_align_test2B (d, s):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (fabs(t)+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for i in range(len (iacc)):
        t = iacc[i]
        r = ""
        if (i < len(s)):
            r = s[i]
        if (t == 3333 or t == 6666): #1/3 2/3
            weight += 0 #0.25 ???
        elif (t == 0 or t == 5000 or t == 4999): #1/2
            weight += 1.
            if (r == "H" and t == 0):
                weight += 0.
            if (r == "H" and t == 5000):
                weight += .0
            if (t == 0 and r == "I"):
                weight += 0.
            if (r == "[.]"):
                weight -= .0
        elif (t == 2500 or t == 2499): #1/4
            weight += 1.
            if (r == "I"):
                weight += 0.
            if (r == "[.]"):
                weight -= .0
        elif (t == 7500 or t == 7499): #3/4
            weight += 1.
            if (r == "I"):
                weight += 0.
            if (r == "[.]"):
                weight -= .0
        elif (t == 8332 or t == 8333): #5/6
            weight += 0 #0.25 ???
        elif (t == 1667 or t == 1666): #1/6 new
            weight += 0 #0.25 ???
        elif (t == 1250 or t == 3750): #1/8
            weight += 1.
        elif (t == 6250 or t == 8750): #1/8
            weight += 1.
#    print (iacc, weight)
    return weight


# def beat_align_test3 (d, s):
#     accum = [0.]
#     iacc = []
#     weight = 0.
#     for t in d:
#         last = accum[-1]
#         accum.append (fabs(t)+last)
#     for t in accum:
#         iacc.append (int(t * 10000.))
# #    print (iacc)
#     for i in range(len (iacc)):
#         t = iacc[i]
#         r = ""
        
#         if (i < len(s)):
#             r = s[i]
#         shortlong = 1.
#         if (i < (len(d) - 1)):
#             shortlong = d[i] - d[i+1]
#         if (t == 0 or t == 3333 or t == 6666): #1/3 2/3
#             weight += 1.
#             if (r == "H"):
#                 weight += 0.2
#             if (shortlong < 0.):
#                 weight -= 0.5
# #        elif (t == 5000 or t == 4999): #1/2
# #            weight += 0 #0.25 ???
#         elif (t == 8332 or t == 8333): #5/6
#             weight += 0.25  # test ######## was 0.75 then 0.5
#         elif (t == 1667 or t == 1666): #1/6 new
#             weight += 0.25 # test ######## was 0.75
#             #new34_1 0.05 new34_2 0.25
    
#     return weight

def beat_align_test5 (d):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (fabs(t)+last)
    for t in accum:
        iacc.append (int(t * 10000.))

# .2 .4 .6 .8

    for t in iacc:
        if (t == 2000 or t == 4000): #1/5 2/5
            weight += 1.
        elif (t == 6000 or t == 8000): #3/5 4/5
            weight += 1.
       
#    print (iacc, weight)
    return weight

def beat_align_test68 (d):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (fabs(t)+last)
    for t in accum:
        iacc.append (int(t * 10000.))

# .2 .4 .6 .8

    for t in iacc:
        if (t == 5000): #1/2
            weight += 1.
        elif (t == 3333 or t == 6666): #3/5 4/5
            weight += .5
       
#    print (iacc, weight)
    return weight


def beat_align_test2NI (d, s):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (t+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for i in range(len (iacc)):
        t = iacc[i]
        r = ""
        if (i < len(s)):
            r = s[i]
        shortlong = 1.
        if (i < (len(d) - 1)):
            shortlong = d[i] - d[i+1]
        if (t == 0 or t == 2500 or t == 6250): #1/2
            weight += 1.
            if (shortlong < 0.):
                weight -= 0.25
        elif (t == 3750 or t == 7500): #1/4
            weight -= .5
#            if (shortlong < 0.):
#            # if the second dur after beat 2 is aligned with beat 3:
#                if ((shortlong + 1.) < 0.):
#                    weight -= 0.25
#        elif (t == 7500 or t == 7499): #3/4
#            weight += 1.
#            if (shortlong < 0.):
#                weight -= 0.25
#        elif (t == 8332 or t == 8333): #5/6
#            weight += 0 #0.25 ???
#        elif (t == 1667 or t == 1666): #1/6 new
#            weight += 0 #0.25 ???

#    print (iacc, weight)
    return weight

def beat_align_test2NIb (d, s):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (t+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for i in range(len (iacc)):
        t = iacc[i]
        r = ""
        if (i < len(s)):
            r = s[i]
        shortlong = 1.
        if (i < (len(d) - 1)):
            shortlong = d[i] - d[i+1]
        if (t == 0 or t == 3750 or t == 7500): #1/2
            weight += 1.
            if (shortlong < 0.):
                weight -= 0.25
        elif (t == 2500 or t == 6250): #1/4
            weight -= .5
#            if (shortlong < 0.):
#            # if the second dur after beat 2 is aligned with beat 3:
#                if ((shortlong + 1.) < 0.):
#                    weight -= 0.25
#        elif (t == 7500 or t == 7499): #3/4
#            weight += 1.
#            if (shortlong < 0.):
#                weight -= 0.25
#        elif (t == 8332 or t == 8333): #5/6
#            weight += 0 #0.25 ???
#        elif (t == 1667 or t == 1666): #1/6 new
#            weight += 0 #0.25 ???

#    print (iacc, weight)
    return weight

