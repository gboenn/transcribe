# Copyright (c) 2025 Georg Boenn
# Attribution-NonCommercial-ShareAlike 4.0 International
# See license.txt in the transcribe distribution

import math as m

transcript = [
[0.016666666666666666, 11.066666666666666, 1.0, 60.0, "[10 .]", "\\tuplet 5/4 {sn64}"],
[0.020833333333333332, 6.666666666666666, 1.0, 48.0, "[8 .]", "sn64"],
[0.027777777777777776, 7.333333333333333, 1.0, 36.0, "[6 .]", "\\tuplet 3/2 {sn32}"],
[0.03125, 5.0, 1.0, 32.0, "[16 -]", "sn64."],
[0.03333333333333333, 10.066666666666666, 1.0, 30.0, "[5 .]", "\\tuplet 5/4 {sn32}"],
[0.041666666666666664, 5.666666666666666, 1.0, 24.0, "[4 .]", "sn32"],
[0.05555555555555555, 6.333333333333333, 1.0, 18.0, "[3 .]", "\\tuplet 3/2 {sn16}"],
[0.0625, 4.0, 1.0, 16.0, "[8 -]", "sn32."],
[0.06666666666666667, 9.066666666666666, 1.0, 15.0, "[5 I]", "\\tuplet 5/4 {sn16}"],
[0.07291666666666667, 7.666666666666666, 7.0, 96.0, "[16 H~-]", "sn32.."],
[0.08333333333333333, 4.666666666666666, 1.0, 12.0, "[.]", "sn16"],
[0.1111111111111111, 5.333333333333333, 1.0, 9.0, "[3 I]", "\\tuplet 3/2 {sn8}"],
[0.125, 3.0, 1.0, 8.0, "[4 -]", "sn16."],
[0.13333333333333333, 9.066666666666666, 2.0, 15.0, "[5 H]", "\\tuplet 5/4 {sn8}"],
[0.14583333333333334, 6.666666666666666, 7.0, 48.0, "[8 H~-]", "sn16.."],
[0.16666666666666666, 3.6666666666666665, 1.0, 6.0, ".", "sn8"],
[0.20833333333333334, 5.666666666666666, 5.0, 24.0, ".~[4.]", "sn8~sn32"],
[0.2222222222222222, 5.333333333333333, 2.0, 9.0, "[3 H]", "\\tuplet 3/2 {sn4}"],
[0.25, 2.0, 1.0, 4.0, "[-]", "sn8."],
[0.26666666666666666, 9.066666666666666, 4.0, 15.0, "[5 W]", "\\tuplet 5/4 {sn}"],
[0.2916666666666667, 5.666666666666666, 7.0, 24.0, "[4 H~-]", "sn8.."],
[0.3333333333333333, 2.6666666666666665, 1.0, 3.0, "I", "sn4"],
[0.4166666666666667, 4.666666666666666, 5.0, 12.0, "I~[.]", "sn4~sn16"],
[0.4444444444444444, 5.333333333333333, 4.0, 9.0, "[3 W]", "\\tuplet 3/2 {sn2}"],
[0.5, 1.0, 1.0, 2.0, "-", "sn4."],
[0.5833333333333334, 4.666666666666666, 7.0, 12.0, "[H~-]", "sn4.."],
[0.6666666666666666, 2.6666666666666665, 2.0, 3.0, "H", "sn2"],
[0.8333333333333334, 3.6666666666666665, 5.0, 6.0, "H~.", "sn2~sn8"],
[0.8888888888888888, 5.333333333333333, 8.0, 9.0, "[3 W~W]", "\\tuplet 3/2 {sn1}"],
[1.0, 0.0, 1.0, 1.0, "H~I", "sn2."]
]

# 0.0555556     : 1/18     : 6.33333

transcript4 = [
[0.0125, 10.4, 1.0, 80.0, "[10 .]", "sn1"],
[0.015625, 6.0, 1.0, 64.0, "[8 .]", "sn1"],
[0.020833333333333332, 6.666666666666666, 1.0, 48.0, "[6 .]", "sn1"],
[0.0234375, 7.0, 3.0, 128.0, "[16 -]", "sn1"],
[0.025, 9.4, 1.0, 40.0, "[5 .]", "sn1"],
[0.0277778, 7.33333, 1.0, 36.0, "[9 I]", "sn1"],
[0.03125, 5.0, 1.0, 32.0, "[4 .]", "sn1"],
[0.041666666666666664, 5.666666666666666, 1.0, 24.0, "[3 .]", "sn1"],
[0.046875, 6.0, 3.0, 64.0, "[8 -]", "sn1"],
[0.05, 8.4, 1.0, 20.0, "[5 I]", "sn1"],
[0.0546875, 7.0, 7.0, 128.0, "[16 H~-]", "sn1"],
[0.0555556, 6.33333, 1.0, 18.0, "[9 H]", "sn1"],
[0.0625, 4.0, 1.0, 16.0, "[.]", "sn1"],
[0.08333333333333333, 4.666666666666666, 1.0, 12.0, "[3 I]", "sn1"],
[0.09375, 5.0, 3.0, 32.0, "[4 -]", "sn1"],
[0.1, 7.4, 1.0, 10.0, "[5 H]", "sn1"],
[0.109375, 6.0, 7.0, 64.0, "[8 H~-]", "sn1"],
[0.125, 3.0, 1.0, 8.0, ".", "sn1"],
[0.15625, 5.0, 5.0, 32.0, "[I~.]", "sn1"],
[0.16666666666666666, 3.6666666666666665, 1.0, 6.0, "[3 H]", "sn1"],
[0.1875, 4.0, 3.0, 16.0, "[-]", "sn1"],
[0.2, 6.4, 1.0, 5.0, "[5 W]", "sn1"],
[0.21875, 5.0, 7.0, 32.0, "[4 H~-]", "sn1"],
[0.25, 2.0, 1.0, 4.0, "I", "sn1"],
[0.3125, 4.0, 5.0, 16.0, "I~.", "sn1"],
[0.3333333333333333, 2.6666666666666665, 1.0, 3.0, "[3 W]", "sn1"],
[0.375, 3.0, 3.0, 8.0, "-", "sn1"],
[0.4375, 4.0, 7.0, 16.0, "[H~-]", "sn1"],
[0.5, 1.0, 1.0, 2.0, "H", "sn2"],
[0.625, 3.0, 5.0, 8.0, "H~.", "sn1"],
[0.6666666666666666, 2.6666666666666665, 2.0, 3.0, "[3 W~W]", "sn1"],
[0.75, 2.0, 3.0, 4.0, "H~I", "sn1"],
[0.875, 3.0, 7.0, 8.0, "H~-", "sn1"],
[1.0, 0.0, 1.0, 1.0, "W", "sn1"]
]


def transcribe(a, tern):
    result = []
    durs = a
#    print durs
    if tern:
        for f in range(len(durs)):
            for t in transcript:
                if (m.fabs(durs[f] - t[0]) < 0.00001):
                    result.append(t[4])
    else:
        for f in range(len(durs)):
            for t in transcript4:
                if (m.fabs(durs[f] - t[0]) < 0.00001):
                    result.append(t[4])
    return result

def transcribe_back (t, tern):
    result = []
    if tern:
        for k in range(len(t)):
            for s in transcript:
                if (t[k] == s[4]):
                    result.append(s[0])
    else:
        for k in range(len(t)):
            for s in transcript4:
                if (t[k] == s[4]):
                    result.append(s[0])
    return result
    
def transcribe_to_ratios (t, tern):
    result = []
    if tern:
        for k in range(len(t)):
            for s in transcript:
                if (t[k] == s[4]):
                    result.append(int(s[2]))
                    result.append(int(s[3]))
    else:
        for k in range(len(t)):
            for s in transcript4:
                if (t[k] == s[4]):
                    result.append(int(s[2]))
                    result.append(int(s[3]))
    return result

def snmr_string(a):
    return ''.join(a)



def encode_lily(durs):
    result = []
    for f in range(len(durs)):
        for t in transcript:
            if (m.fabs(durs[f] - t[0]) < 0.00001):
               result.append(t[5])
    return result


def dur_ratios(w):
#take list of onstes and analyse duration ratios (IOT ratios)
    result = []
    durs = []
    for k in range(len(w)-1):
        iot = w[k+1] - w[k]
        durs.append(iot)
    for k in range(len(durs)-1):
        r = durs[k+1] / durs[k]
        result.append(r)
    return result
        
def start_lily():
    return "\\version \"2.18.2\" \\score { \\new DrumStaff  \\drummode{"

def end_lily():
    return "} \\layout {} \\midi {\\tempo 8 = 90 }}"


def write_lily(snmr, filename, meter):
    fquant = open(filename, 'w+')
    fquant.write(start_lily())
    fquant.write("\n")
    meterstr = "\\time " + meter + " "
    fquant.write(meterstr)
    for k in snmr:
        for s in transcript:
#            print "==",k,s[4]
            if (k==s[4]):
                fquant.write(s[5])
                fquant.write(" ")
    fquant.write("\n")
    fquant.write(end_lily())
    fquant.close()


