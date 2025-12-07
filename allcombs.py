# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

from float_to_ratio_func import *
from fareytab import *
from digest import *
from expwindow import *
from permut_lists import *
from cost import *
from transcription import *
from pattern import *

from itertools import *
import math as m
import sys

if len(sys.argv) < 3:
    print("Usage: %s <number of events> <dutations pattern> <ternary flag>" % sys.argv[0])
    sys.exit(1)

#
# python3.7 multi_double_farey.py 8 '...' 1
#
# gereates all possible permutations of duration patterns within one bar
# measures RIM per bar and sorts the resulting list according to increasing RIM
# creates a demo for chunking and a pitch list too


# there are four cost functions defined in cost.py:
# cost_fun (a)
# The accumulated divisibility cost of all onsets represented as ratios

# cost_fun_harm (a)
# The rhythmic impact measure RIM

# cost_fun_numerator (a)
# Like cost_fun but evaluating the numerators instead of the denominators

# cost_fun_ratios (a)
# Evaluating the ratios of durations in pairs

# plus there is this category depending on ternary or binary meter only
# beat_align_test (d)   #1/6 #5/6 #1/2 #1/3 2/3 for ternary bars
# beat_align_test2 (d)  #1/6 #5/6 #3/4 #1/4 #1/2 #1/3 2/3 for binary
# beat_align_test3 (d)  #1/6 #5/6 #1/2 #1/3 2/3 for ternary

# test procedure:
#  python3.7 all_bars.py 5 x 0 > son_clave.txt
#  open son_clave.txt
#  chunking -m tsnmr son_clave.txt son_clave_pitch.txt 8
#  ly transcription.ly
#  pr transcription.pdf
#  timidity -T 90 transcription.midi

num_events = int(sys.argv[1])
durations_pattern = list(sys.argv[2])
ternary_flag = int(sys.argv[3])

def comb_wr (n, k, ar, x, output_a):
#combinations without repetitions
    if (x < k):
        max = 0
        if (x > 0):
            max = ar[x-1]
        i = max+1
        while (i <= n-k+x+1):
            ar[x] = i
            comb_wr (n, k, ar, x+1, output_a)
            i += 1
    else:
        #print (ar)
        b = []
        for k in ar:
            b.append(k)
        output_a.append(b)
        
#comb_wr (4, 3, a, 1)

def comb_rep (n, k, ar, x, output_a):
#combinations with repetitions
    if (x < k):
        max = 1
        if (x > 0):
            max = ar[x-1]
        i = max
        while (i <= n):
            ar[x] = i
            comb_rep (n, k, ar, x+1, output_a)
            i += 1
    else:
        #	print (ar)
        b = []
        for k in ar:
            b.append(k)
        output_a.append(b)

def perm_rep (n, k, ar, x, output_a):
#permutations with repetitions
    if (x < k):
        i = 1
        while (i <= n):
            ar[x] = i
            perm_rep (n, k, ar, x+1, output_a)
            i += 1
    else:
        #print (ar)
        b = []
        for k in ar:
            b.append(k)
        output_a.append(b)
   
def perm (k, ar, x, output_a):
    if (x < k):
        sav = ar[x]
        i = x
        while (i < k):
            ar[x] = ar[i]
            ar[i] = sav
            perm (k, ar, x+1, output_a)
            ar[i] = ar[x]
            i+=1
        ar[x] = sav
    else:
        b = []
        for k in ar:
            b.append(k)
        output_a.append(b)

def perm_wr (n, k, ar, x, output_a):
#permutations without repetitions
    if (x < k):
        max = 0
        if (x > 0):
            max = ar[x-1]
        i = max+1
        while (i <= n-k+x+1):
            ar[x] = i
            perm_wr (n, k, ar, x+1, output_a)
            i += 1
    else:
        perm (k, ar, 0, output_a)

#duration_ar = [0.16666666666666666, 0.6666666666666666, 0.3333333333333333, 0.25, 0.08333333333333333, 0.125, 0.041666666666666664]

#durations_pattern = ['H', 'I', '-', '.', '[.]']

#durations_pattern = ['[.]', '.', '-', 'I', 'H']

durations_pattern = ['H', 'I', '.', '[3 I]']

#durations_pattern = ['I', '[-]', '.'] # durations 4 3 2 for son clave, with 5 events

#durations_pattern = ['I', '[-]', '.', '[.]']

#durations_pattern = ['.', '[.]'] # ewe ternary

#durations_pattern = ['[3 H]', '[3 I]'] #ewe binary

durations_pattern = ['H', 'I', '[-]', '.']

#durations_pattern = ['[3 W]', 'I', '[3 I]', '.']

durations_pattern = ['I', '.', '[-]'] #son clave
#durations_pattern = ['.', '[-]'] # tresilio
#durations_pattern = ['.', '[-]', '[.]'] #rhythmic intervals, groove
#durations_pattern = ['I', '[-]'] #son clave
#durations_pattern = ['.', '[.]'] #ewe
#durations_pattern = ['.', '[-]', 'I', 'I~[.]', '-'] #23456 H~[.]
#durations_pattern = ['.', '[-]', 'I', '[H~-]'] #2347
#durations_pattern = ['.',  'I', '[-]', '-', 'I~[.]', 'H~[.]'] #234569 H~[.]
# chopin mazurka unique durations (testbed.py)
#durations_pattern = ['H', 'I', '.', '[-]', '[.]']
#durations_pattern = ['H', 'I', '.', '[-]', '[.]', '[4 -]', '[4 .]']

#durations_pattern = ['H', 'I', '.']
#durations_pattern = ['H~I', '.']
#durations_pattern = ['[.]', '.', '[-]', 'I', 'H'] # max onsets 9 for 4/4 meter
durations_pattern = ['[.]', '.', '[-]', 'I'] # tha
durations_pattern = ['[.]', '.', '[-]', '-', 'I', 'H'] # tha dec 6

duration_ar = transcribe_back (durations_pattern, ternary_flag)
#print (duration_ar)

resfile = open ("rcostfun_output.txt", "a")
catfile = open ("catalog_pat_output.txt", "a")
#print ("test permutations without repetitions---------------")
permlist = []
a = [0]*(2)
perm_wr (4, 2, a, 0, permlist)
#print (permlist)
#print ("---------------")

pitchlist = [69, 71, 72, 74]
pitchlist = [65, 69, 71, 72]
a = [0]*4
pl = []
perm_rep (len(pitchlist), 4, a, 0, pl)
for j in pl:
    p = []
    for i in j:
        p.append(pitchlist[i-1])
#    print (', '.join(p))
#    print (pitchlist[j-1])
#    print (p)

output_l = []
k = num_events
a = [0]*(k)
perm_rep (len (duration_ar), k, a, 0, output_l)

#print (output_l)

#make sure ony one bar lengths of patterns are returned
dur_combination = []
for k in output_l:
    sum = 0
    for j in k:
        sum += m.fabs(duration_ar[j-1]) # interested in all events, also silences
    # only those k events permutations which fit in one bar (1.0) pass the filter
    if (m.fabs(sum - 1.0) < 0.01):
        c = []
        for j in k:
            c.append (durations_pattern[j-1])
        dur_combination.append (c)

#print (dur_combination)
      
#apply cost function
rim_list = []
for k in dur_combination:
    s = transcribe_back (k, ternary_flag)
    a = []
    a.append (snmr_string(k))

# COST FUNCTIONS
# 1
    #a.append (cost_fun_harm(s))
# The rhythmic impact measure RIM

# 1.2
    a.append (cost_fun_harm2(s))
# The modifed rhythmic impact measure RIM

# 2
    #a.append (cost_fun(s))
#accumulated durations
#digestibility of an integer (denominator)
#small value => high digestibility (low complexity)

# 3
    #a.append (cost_fun_numerator (s))
#digestibility of an integer (numerator)
  
# 4
    #a.append (cost_fun_ratios(s))
# Evaluating the ratios of durations in pairs

    if (ternary_flag):
        a.append (beat_align_test3(s))
    else:
        a.append (beat_align_test2(s))

    a.append (cost_fun_ratios(s))

    a.append(k)

    rim_list.append(a)

#rim_list.sort(key=lambda x: x[1], reverse = True) # for case cost_fun_ratios(s)
rim_list.sort(key=lambda x: x[1], reverse = False) # rim

rim_list.sort(key=lambda x: x[3], reverse = True) # ratios

rim_list.sort(key=lambda x: x[2], reverse = True) # beats

print ("$ ['I', '[-]', '.'], k=5, cost_fun_harm, beat align 3")
#for k in rim_list:
#    print (k)
    
count = 1
for k in rim_list:
    print (k[0])
    resfile.write (str(count))
    resfile.write ("\t")
    resfile.write (str(k[1]))
    resfile.write ("\t")
    resfile.write (str(k[2]))
    resfile.write ("\t")
    resfile.write (str(k[3]))
    resfile.write ("\t")
    resfile.write (k[0])
    resfile.write ("\n")

    catfile.write (str(k[4]))
    catfile.write (",\n")    
    
    count += 1
    
#rim_list.reverse()
#for k in rim_list:
#    print (k[0])

        
