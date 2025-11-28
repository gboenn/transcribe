# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

from catalog import *

def remove_dups (reslist):
    return list (dict.fromkeys(reslist))

def flatten_list (input_list):
    flat_list = []
    for sublist in input_list:
        for item in sublist:
            flat_list.append(item)
    return flat_list
        
#--------------------------------------------------------------------------------

pat_catalog = {
    'tha2' : tha2,
    'tha': tha,
    'bach_prel_1_gould': bach_prel_1_gould,
    'amen': amen,
    'impeach': impeach,
    'apache': apache,
    'bigbeat': bigbeat,
    'newday': newday,
    'thinkaboutit': thinkaboutit,
    'synthetic': synthetic,
    'hihache': hihache,
    'saltofearth': saltofearth,
    'barrywhite': barrywhite,
    'twinkle': twinkle,
    'haenschen': haenschen,
    'muehle': muehle,
    'ravel': ravel,
    'alala': alala,
    'weber': weber,
    'voegel1': voegel1,
    'bach_aria_goldberg': bach_aria_goldberg,
    'gymnopedie1': gymnopedie1,
    'gymnopedie1_2': gymnopedie1_2,
    'brahms': brahms,
    'happy_birthday': happy_birthday,
    'happy_birthday2': happy_birthday2,
    'bach_prel_1_gilbert': bach_prel_1_gilbert,
    'bach_prel_1_gulda': bach_prel_1_gulda,
    'bach_prel_2': bach_prel_2,
    'bach_prel_2_gilbert' : bach_prel_2_gilbert,
    'bach_prel_2_mcgregor' : bach_prel_2_mcgregor,
    'bach_prel_2_schiff' : bach_prel_2_schiff,
    'beethoven': beethoven,
    'chopin': chopin,
    'chopin_francois': chopin_francois,
    'twinkle2' : twinkle2
}

bpatterns = bach_prel_1_gould

def set_patterns (p):
    global bpatterns
    bpatterns = pat_catalog[p]
    print ("set_patterns", bpatterns)

#--------------------------------------------------------------------------------

def find_pattern (s, strict):
    if (strict == 1):
        return find_pattern_strict (s)
    len_s = len(s)
    for b in bpatterns:
        len_b = len(b)
        end = s[(len_s - len_b):]
        #print end, " == ", list(b)
        if (end == list(b)):
            return b
    return ""

def find_pattern_strict (s):
    for b in bpatterns:
        if (s == list(b)):
            return b
    return ""

def beat_align_test (d):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (t+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for t in iacc:
        if (t == 3333 or t == 6666): #1/3 2/3
            weight += 1.
        elif (t == 5000 or t == 4999): #1/2
            weight += 0.5
        elif (t == 8332 or t == 8333): #5/6
            weight += 0.5
        elif (t == 1662 or t == 1666): #1/6 new
            weight += 0.5

    # print (iacc, weight)
    return weight
    
def beat_align_test2 (d):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (t+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for t in iacc:
        if (t == 3333 or t == 6666): #1/3 2/3
            weight += 0.25
        elif (t == 5000 or t == 4999): #1/2
            weight += 1.
        elif (t == 2500 or t == 2499): #1/4
            weight += 1.
        elif (t == 7500 or t == 7499): #3/4
            weight += 1.
        elif (t == 8332 or t == 8333): #5/6
            weight += 0.25
        elif (t == 1662 or t == 1666): #1/6 new
            weight += 0.25

    # print (iacc, weight)
    return weight


def beat_align_test3 (d):
    accum = [0.]
    iacc = []
    weight = 0.
    for t in d:
        last = accum[-1]
        accum.append (t+last)
    for t in accum:
        iacc.append (int(t * 10000.))

    for t in iacc:
        if (t == 3333 or t == 6666): #1/3 2/3
            weight += 1.
        elif (t == 5000 or t == 4999): #1/2
            weight += 0.25
        elif (t == 8332 or t == 8333): #5/6
            weight += 0.75
        elif (t == 1662 or t == 1666): #1/6 new
            weight += 0.75

    # print (iacc, weight)
    return weight
