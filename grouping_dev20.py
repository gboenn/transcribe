# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

import concurrent.futures
import math
import sys
import time

import cProfile

# it is sufficient to understand compound rhythms in order to solve the quantization problem
# the problem is to know the local tempo of a piece and to predict when the next downbeat is going to happen
# the downbeat prediction can be achieved by successfully transcribing the compound rhythmic pattern that occurs within a bar. The local tempo within that bar can then be calculated easily by using the time that has elapsed between the previous downbeat and the next downbeat, whose position in time is a result of a succesful quantization of the compund rhythm within the bar, and the mapping of the quantized rhythm back to its original occurence on the timeline.
# one can build a memory, or a database of compound rhythms, based on previous results of transcribing the same piece of music.

from float_to_ratio_func import *
from fareytab import *
from digest import *
from expwindow import * 
from permut_lists import *
from cost import *
from transcription import *
from pattern import *

onsetsA = []

def find_pattern_in_memory (s, memory, bar):
    b = eval(memory[bar][3])
    # because the list at memory[bar][3] comes from a text file
    # eval is used to convert string back to python list
    if (s == b):
        return True
    return False

def downbeat_time (onsetlist, index):
    if (index > 0) and (index < len(onsetlist)):
        return onsetlist[index]
    else:
        return -1


def quantize(markers):
    # qdebug = 0
    n_ = markers[0]
    onsets = markers[1] #onsetsA[i1:i2]
    onsets0 = []
    durations = []
    threshold = markers.pop()
    ternary = markers.pop()
    # print ("onsets:")
    # print (onsets)
    # print ("duration ratios from onsets:")
    # print (dur_ratios(onsets))

    sum_durs = 0.

    for k in range(len(onsets) -1):
        o1 = onsets[k]
        o2 = onsets[k+1]
        odiff = o2-o1
        durations.append(odiff)
        onsets0.append(odiff)
        sum_durs += odiff

    #print "length of window = ", sum_durs, " s."

    #print "IOTs:"
    #print durations
    onsets = durations

    #print dur_ratios(onsets)

    onsets.sort()

    #print onsets

    groups = []
    groups.append([])
    gc = 0
    groups[gc].append(onsets[0])
    for k in range(len(onsets)-1):
        o1 = onsets[k]
        o2 = onsets[k+1]
        if (o2-o1) < threshold:
            groups[gc].append(o2)
    #        print o1, o2
        else:
    #        print "new"
            gc += 1
            groups.append([])
            groups[gc].append(o2)

    #print ("groups:")
    #print (groups, " has ", gc+1, " groups.") 


    durclasses = []
    norm_durclasses = []
    length_durclasses = []
    order_classes = []
    for o in range(len(onsets0)):
        for k in range(gc+1):
            count = 0
            for m in range(len(groups[k])):
                if (onsets0[o] == groups[k][m]):
                    durclasses.append([k,onsets0[o]])
                    norm_durclasses.append([k,onsets0[o]/sum_durs])
                    order_classes.append(k)
                    count += 1
                    break

    for k in range(gc+1):
        length_durclasses.append(len(groups[k]))

    #print "duration classes:"   
    #print durclasses
    #print "normalized classes:"
    #print norm_durclasses            
    #print length_durclasses
    #print ("order of classes")
    #print (order_classes)

    mean_classes = []
    for k in range(gc+1):
        temp = []
        for i in range(len(norm_durclasses)):
            if (norm_durclasses[i][0] == k):
                temp.append(norm_durclasses[i][1])
        mean_dur = 0.
        if (len(temp) > 0):
            for i in range(len(temp)):
                mean_dur += temp[i]
            mean_dur /= len(temp)
        mean_classes.append([k,mean_dur])
    #    order_classes.append(k)

    #print ("means of normalized classes:")
    #print (mean_classes)

    #print "means as fractions:"
    #for i in range(len(mean_classes)):
    #    print float2ratio(mean_classes[i][1])


    #ternary meter ratios
    ratio3 = [2,3,1,1,5,6,1,3,1,2,5,12,7,12,1,6,1,4,5,24,7,24,1,12,1,8,7,48,1,24,1,16,7,96,1,48,1,32,8,9,4,9,2,9,1,9,1,18,1,36,4,15,2,15,1,15,1,30,1,60]

#binary meter ratios
    ratio4=[1, 18, 1, 36, 1, 2, 3, 4, 5, 8, 1, 4, 3, 8, 5, 16, 7, 8, 7, 16, 1, 8, 3, 16, 5, 32, 7, 32, 1, 16, 3, 32, 7, 64, 1, 32, 3, 64, 7, 128, 1, 64, 3, 128, 2, 3, 1, 3, 1, 6, 1, 12, 1, 24, 1, 48, 1, 5, 1, 10, 1, 20, 1, 40, 1, 80]

    #ternary-----------------------------------------

    # . = 1 6 eighth
    # I = 1 3 quarter
    # H = 2 3 half
    # [-] = 1 4 dotted eighth
    # [.] = 1 12 sixteenth
    # [4 -] = 1 8 dotted sixteenth
    # [4 .] = 1 24 32nd


    ratio_experiment_chopin = [1, 6, 2, 3, 1, 3, 1, 4, 1, 12, 1, 8, 1, 24]
    
    ratio_experiment_schiff = [1, 3, 1, 6, 1, 9, 2, 9, 2, 15]

    ratio_experiment_gilbert = [1, 3, 1, 6, 1, 9, 2, 9, 2, 15, 1, 15]

    ratio_backhaus = [1, 3, 1, 6, 2, 3, 1, 12, 1, 4, 1, 8, 1, 1, 1, 15, 1, 24, 7, 24]

    ratio_ravel = [1, 3, 1, 6, 1, 1, 1, 18]

    ratio_twinkle = [1, 1, 1, 2, 1, 4, 3, 4]

    ratio_muehle = [1, 6, 1, 3, 5, 6, 1, 12]

    ratio_alala = [1, 1, 1, 2, 1, 4, 3, 4, 1, 8, 3, 8, 1, 16, 1, 32, 3, 16, 1, 12]
    #-------------------------------------

    fareytabletest=ratio4
    beats = 4.
    if ternary:
        #fareytabletest=ratio_experiment
        fareytabletest=ratio3 #ratio_experiment_chopin
        beats = 3.

    fareydigest = []
    for i in range(0, len(fareytabletest), 2):
        p = float(fareytabletest[i])
        q = float(fareytabletest[i+1])
            #if (q == 2 and ternary == 1) or (q == 4 and ternary == 1):
            #fareydigest.append([(p/q), digest(6), p, q])
            #print p, q, digest(6)
            #else:
        fareydigest.append([(p/q), digest(q), p, q])
#print p, q, digest(q)
    gauss_table_length = 1024
    win = expwin(gauss_table_length)
    #print win

    solutions = []

    #num_qdurs = 8 with larger list of fareytabletest
    #allow for num_qdurs durations per class
    # performance is faster with lower num_qdurs 
    num_qdurs = 6
    for k in range(len(mean_classes)):
        srange = mean_classes[k][1] # change from 1.0 to 1.25 (Francois Mazurka)
            #if (length_durclasses > 1):
            #srange = 1. * mean_classes[k][1]
            #else:
            #srange = 1. * mean_classes[k][1]
        if (srange > 0.03):
            max = mean_classes[k][1] + 0.5 * srange
            min = mean_classes[k][1] - 0.5 * srange
        else:
            max = mean_classes[k][1] + 0.6 * srange
            min = mean_classes[k][1] - 0.6 * srange
        if max > 1.0: max = 1.
        if min < 0.0: min = 0.
        #print "search area:"
        #print min, mean_classes[k][1], max
        quant_cand = list()
        for el in fareydigest:
            #modification and el[1] != 0.):
            if (el[0] >= min and el[0] <= max): # and el[1] != 0.):
#                print el
                n = int(float(gauss_table_length) * (el[0] - min)/(max - min))
                w = win[n]
                quant_cand.append([el[0], w/el[1], el[2], el[3], w])
        quant_cand.sort(key=lambda x: x[1])
        quant_cand.reverse()
        count = 0
        slist = []
        #if (True):
            #print ("solutions:")
        for p in quant_cand:
            p.append(k)
            #if (True):
            #    print (p)
            slist.append(p)
            count += 1
            if (count > (num_qdurs-1)):
                break
        solutions.append(slist)

    #print (solutions)

    # create all combinations of possible durations per class
    #print "there are ", len(solutions), " duration classes"
    slist = []
    for l in solutions:
        contrib = []
        for m in l:
            contrib.append(m[0])
        slist.append(contrib)

    #print(slist)
    clist =  list_combinations(slist)
    #print(clist)
    #map clist to normalized duration classes: norm_durclasses via order_classes
    dlist = []
    #qdebug2 = False
    for c in clist:
        d = []
        s = 0.
        for k in order_classes:
            d.append(c[k])
            s = s + c[k]
            # print(d, s)
        #if (qdebug2):
        #    dlist.append(d)
        #else: # possible performance enhancement
        if (math.fabs(s - 1.0) < 0.0001):
                #print "tru", s
            dlist.append(d)
            #print d, s
            s = 0.

    # print len(dlist)
    #print(dlist)
    orig = []
    for k in norm_durclasses:
        orig.append(k[1])

    #print "original durations:"
    #print orig
    #print "quantized:"
    reslist = []
    for d in dlist:
        c = cost_fun(d)
        cr = c / float(len(d))
        ch = cost_fun_harm(d)
        cf = cost_fullbar(d)
        reslist.append([d, c, cr, cf, cost_fun_euclid(d,orig), ch, cost_fun_numerator(d), n_, (60./(sum_durs/beats))])
    #                   0  1  2   3    4                       5    6                      7       8
        # 7: the onset index of the start of the next bar
        # 8: bpm

    return reslist

def q_process (i1_, ternary_, offset_, numversions_, threshold_):
    # profiler = cProfile.Profile()
    # profiler.enable()

    global onsetsA

    i2 = i1_ + offset_
    windowres = []
    
    onset_list = []
    for k in range(numversions_):
        i2 = i2 + 1
        # print (i1_, ":", i2, " : ", onsetsA[i1_:i2])
        if (len(onsetsA[i1_:i2]) > 1):
            onset_list.append([i2-1, onsetsA[i1_:i2], ternary_, threshold_])

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(quantize, onset_list)
        for result_ in results:
            for l in result_:
                windowres.append(l)

    if (False):
        for k in windowres:
            t = transcribe(k[0], ternary_)
            print ("result: ", k, t)

    windowres.sort(key=lambda x: x[2])

    weighted_results = []
    for r in windowres:
        #print r[0]
        r2 = []
        r2.append(r[0])
        w = beat_align_test(r[0])
        w *= -1.
        r2.append (w)
        #print r
        r2.append(i1_ + (len(r[0])))
        r2.append(r[4])
        r2.append(r[-1])
        weighted_results.append(r2)


    #print "------------------------------"
    #print "sorted after beat alignment weight"
    weighted_results.sort(key=lambda x: x[1])
    score_results = []
    for k in weighted_results:
        t = transcribe(k[0], ternary_)
        #print snmr_string(t), k[1], " n = ", k[2], " next downbeat is at = ", onsetsA[k[2]]
        # print(t)
        #bpatterns could be a third argument for find_pattern()
        # p = find_pattern(t,strict)
        p = find_pattern_strict(t)
        if p:
            oneres = []
            oneres.append(snmr_string(t))
            oneres.append(k[1])
            oneres.append(k[2])
            oneres.append(downbeat_time (onsetsA, k[2]))
            oneres.append(p)
            oneres.append(k[3])
            oneres.append(k[4])
            #print snmr_string(t), k[1], " n = ", k[2], " next downbeat is at = ", downbeat_time (onsetsA, k[2])
            #print "found: ", p, " euclid. dist.: ", k[3], " bpm: ", k[4]
            score_results.append (oneres)

### Nov 14 2025 if no match with patterns found, use first quantization
    # if (False):
    #     if (len(score_results) == 0):
    #         k = weighted_results[0]
    #         # print(k[0])
    #         t = transcribe(k[0], ternary_)
    #         # print(t)
    #         # print(snmr_string(t))
    #         oneres = []
    #         oneres.append(snmr_string(t))
    #         oneres.append(k[1])
    #         oneres.append(k[2])
    #         oneres.append(downbeat_time (onsetsA, k[2]))
    #         oneres.append(list(t))
    #         oneres.append(k[3])
    #         oneres.append(k[4])
    #         #print snmr_string(t), k[1], " n = ", k[2], " next downbeat is at = ", downbeat_time (onsetsA, k[2])
    #         #print "found: ", p, " euclid. dist.: ", k[3], " bpm: ", k[4]
    #         score_results.append (oneres)

    # profiler.disable()
    # profiler.dump_stats(f"profile_worker_{i1_}.prof")
    return len(score_results), score_results
#
# collect all n, downbeat_time, and 'found' p from main program
# store into list
# proceed to n that appears most frequent in results or just to the n for which there was a pattern found in the database

# collect all the n's that led to the next solution and reconstruct score from connecting adjacent results. It is assumed that adjacent results represent adjacent bars in the score

# meter detection is implicit and initially starts with the user chosing either a binary or a ternary meter as the basic assumption for the first analysis
#
# final chord problem: a final chord occurs starting at the last full bar.
# solution it is is recognized that there is only one onset left and the note offset.
# therefore a final chord has been recognized and the last bar is printed as a whole note of one quarter with fermata and rests according to meter.

#++++++++++++++++ main program +++++++++++++++++++++++++++++++
def main ():
    
    #<filename>     <threshold>         start> 
    # onsets        for dur classes     1st onset on downbeat
    #<bpm> <ternary>    <offset>           <range> 
    # bpm   0,1         min num onsets     maximum range plus offset onsets  
    #<pattern> name of database list of patterns
    if len(sys.argv) < 8:
        print("Usage: %s <filename> <threshold> <start> <bpm> <ternary> <offset> <range> <pattern>" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    threshold = float(sys.argv[2])
    i1 = int(sys.argv[3])
    first_bpm = float(sys.argv[4])
    ternary = int(sys.argv[5])
    offset = int(sys.argv[6])
    numversions = int(sys.argv[7])
    cat_pattern = sys.argv[8]


    print (filename, threshold, i1, first_bpm, ternary, offset, numversions, cat_pattern)

    #print (pat_catalog.keys())
    #print (pat_catalog.values())

    set_patterns(cat_pattern) # sets variable bpatterns defined in pattern.py

    # only if we wanted to compare data with previous analysis output (t_analysis.txt)
    #recallB = []
    #with open(file2) as k:
    #    for line in k:
    #        data = line.split("\t")
    #        lform = []
    #        for y in data:
    #            lform.append (y)
    #        recallB.append(lform)

    # the onset file, one value per line
    with open(filename) as f:
        for line in f:
            #one onset time in seconds per line
            if not('#' in line): # lines starting with # ignored 
                onsetsA.append(float(line))


    start = time.perf_counter()

    # result output files
    anafile = open ("t_analysis.txt", "w")
    newonsets = open ("t_onsets.txt", "w")

    bpmratio = 1.
    prevbpm = 1.
    if (first_bpm != 0.):
        prevbpm = first_bpm
    barnumber = 1
    accum_time = 0.

    # analysis loop q_process runs multiple processes inside
    while True:
        lenres, q_results = q_process (i1, ternary, offset, numversions, threshold)
        # print ("------------------------------")
        # print ("results found:")
        # print(q_results)
        ########################
        ######## new idea: see line 523 below 
        ######## multiply: euclid. dist * abs ( 1 - bpmratio)
        ######### the smaller this value the better the fit
        ###### absolute veraenderung des tempos in prozent
        ###### percentage change of tempo relative to first bar tempo
        ## if the perc change of tempo is very small ( just above or below 1 ) then the product becomes very small too if the euclid distance is < 1
        #########################
        if (lenres > 0):
            for q in q_results:
                bpmratio = q[6] / prevbpm
                if (prevbpm == 1.):
                    bpmratio = 1.
                q.append(bpmratio)
                q.append(prevbpm)
                #            q.append(q[5] * (math.fabs (1. - q[7])))
                q.append(q[5] * (math.fabs (1. - q[7])) / len(q[4])) # modification
                q.append(math.fabs (1. - q[7]))
                # the longer the found pattern the more fit the result
                # print (q[0], q[1], " n = ", q[2], " next downbeat is at = ", q[3])
                # print ("found: ", q[4], " euclid. dist.: ", q[5], " bpm: ", q[6])
                # print (" bpm: ", q[6], " bpmratio: ", q[7], " prevbpm: ", q[8], " fitness: ", q[9])
                # print ("bpm change: ", q[10])

################ Dec 11: q[2] and q[3] of selected result to be used to make predictopn about the next bars' downbeats
        #use sort for efficiency: .sort(key=lambda x: x[5])
        q_results.sort(key=lambda x: x[5]) # sort after euclid dist.
        q_results.sort(key=lambda x: x[9]) # sort after new fitness parameter

        resid = 0
        print ("------------------------------")
        print ("result selected:")
        if (lenres > 0):
            qr = q_results[resid]
            #bpmratio = qr[6] / prevbpm
            print ("bar ", barnumber)
            print (qr[0], qr[1], " n = ", qr[2], " next downbeat is at = ", qr[3])
            print ("found: ", qr[4], " euclid. dist.: ", qr[5])
            print (" bpm: ", qr[6], " bpmratio: ", qr[7], " prevbpm: ", qr[8], " fitness: ", qr[9])
            fit1 = qr[9]
            fit2 = 100.
            # evaluate the next best result:
            if (resid+1 < lenres):
                qr2 = q_results[resid+1]
            #bpmratio = qr2[6] / prevbpm
                print ("bar ", barnumber)
                print (qr2[0], qr2[1], " n = ", qr2[2], " next downbeat is at = ", qr2[3])
                print ("found: ", qr2[4], " euclid. dist.: ", qr2[5])
                print (" bpm: ", qr2[6], " bpmratio: ", qr2[7], " prevbpm: ", qr2[8], " fitness: ", qr2[9])
                fit2 = qr2[9]
            
            # if the second fittest solustion is only max. 30% away from the first, pick the one
            # that has more duration classes
            # meaning: pick one of first two fittest that contains more information
            if (lenres > 2 and barnumber > 1):
                if (fit1 != 0.):
                    fitperc = fit2 / fit1
                    if (fitperc < 1.3): # was 1.45, testing required for this threshold
                        alist = q_results[resid+1][4]
                        blist = q_results[resid][4]
                        if (len(remove_dups (alist)) > len(remove_dups (blist))):
                            qr = q_results[resid+1]
                            print ("pick one of first two fittest that contains more information")
                    
            #if (lenres > 1): # modification: always test the memory if there is a choice between two patterns
            if (lenres > 5  and barnumber > 1): # modification
                # other idea: if there are that many results pick the one with the smallest difference in bpm compared to previous bar Feb 20 2020, success with McGregor performance of Bach Fsharp maj prelude
                
    #            if (False):
    #                cres = 0
    #                for k in q_results:
    #                    if (find_pattern_in_memory (k[4], recallB, barnumber-1)):
    #                        qr = q_results[cres]
    #                        print ("found this transcription in memory:")
    #                        print (recallB[barnumber-1])
    #                    cres += 1

                #for k in q_results:
                #    k.append(math.fabs (1. - q[7])) # modification

                q_results.sort(key=lambda x: x[10]) # sort after bpm change
                print ("found this transcription to be the fittest because of low abs(1 - bpm_ratio):")
                qr = q_results[0]
                print (qr, qr[10])

            anafile.write (str(barnumber)) # n
            anafile.write ("\t")
            anafile.write (str(qr[2])) # n
            anafile.write ("\t")
            anafile.write (str(qr[0])) # quantized rhythm
            anafile.write ("\t")
            anafile.write (str(qr[4])) # found pattern
            anafile.write ("\t")
            anafile.write (str(qr[6])) # bpm
            anafile.write ("\t")
            anafile.write (str(qr[3])) # next downbeat time in sec
            anafile.write ("\t")
            anafile.write (str(qr[7])) # current bpm / previous bpm
            anafile.write ("\t")
            ## create here a global list of future downbeats in seconds
        ## i1 + (1-bar period), i1 + 2(1-bar period), ...
        ## 1-bar period := 60./prevbpm * 4 (if binary) or * 3 (if ternary)
            future_ones = []
            cur_one = onsetsA[i1] #i1 is an index into the global onset list, i.e. the current beat one
            pfac = [1,2,3]
            if (ternary):
                future_ones = [(x)*(60./qr[6]*3)+cur_one for x in pfac]
            else:
                future_ones = [(x)*(60./qr[6]*4)+cur_one for x in pfac]
            # future_ones[0] and future_ones[1] constitute a prediction
            # of the time-frame of the next bar, which is going to be tried for quantization
            # with q_process
            anafile.write (str(future_ones)) 
            anafile.write ("\n")

            n_onsets = transcribe_back(qr[4], ternary)
            
            for k in n_onsets:
                # newonsets.write (str(k))
                # newonsets.write ("\t")
                newonsets.write (str(accum_time))
                accum_time += k
                newonsets.write ("\n")
            
            # once found the solution which starts a new path will update the vars:
            # i1 and prevbpm
            #if (barnumber == 1):
            #    start_bpm = qr[6]
            i1 = qr[2]
            prevbpm = qr[6]
        
        else:
            print ("no results - finished analysis.")
            break

        barnumber += 1

    #end while(True):


    # ...
    end = time.perf_counter()
    print ("program ran for ", (end - start), " seconds.")


if __name__ == "__main__":
    main ()