#!/usr/bin/env python

import sys
import csv

def wrap(text, width=70):
    return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

vcfFile = sys.argv[1]

vcfTable = [line.replace("*", ".").rstrip("\n").split() for line in open(vcfFile)]

strainList = vcfTable[0]

vcfDict = {}

transposeVCF = map(list,map(None,*vcfTable))

for line in transposeVCF[2::]:
    print ">" + line[0][0:-3]
    print wrap("".join(line[1::]).replace(".", "-"))

'''
for line in vcfTable:
    if line[0] in vcfDict:
        vcfDict[line[0]].append(line)
    else:
        vcfDict[line[0]] = [strainList, line]

outDict = {}

for key, value in vcfDict.iteritems():
    transposeVCF = map(list,map(None,*value))

    if key == "CHROM":
        continue

    #print transposeVCF


    for line in transposeVCF[2::]:
        if line[0][0:-3] in outDict:
            outDict[line[0][0:-3]] += "".join(line[1::])
        else:
            outDict[line[0][0:-3]] = "".join(line[1::])
        #print ">" + line[0][0:-3] + "-" + key
        #print wrap("".join(line[1::]))

for key, value in outDict.iteritems():
    print ">" + key
    print wrap(value)

'''