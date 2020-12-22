#!/usr/bin/env python

import sys
import csv
from operator import itemgetter
import re
import math


SIMPLE_TYPES = "IIIISS"
BTAB_TYPES = "SSISSSIIIIFFIIISISIIIS"
RMOUT_TYPES = "IFFFSIISSSSSSSIS"
MAKER_TYPES = "SSSIISSSS"
MERGED_COUNTS = "SIIISISISIIISISISIIISISI"


CHR = 0
POS = 1
TOT = 3
TOT1 = 5
TOT2 = 7
ATOT = 11
A1 = 13
A2 = 15
BTOT = 19
B1 = 21
B2 = 23


# Converts entries in a table from strings to whatever format that is specified in the type list,
# for instance integers or floats. The type list is now formatted for the MUMmer show-coords
# btab format.
def tableTypeConvert(table, typeList):
    outTable = []
    for line in table:
        newLine = []
        i = 0
        for entry in line:
            if typeList[i] == "S":
                newLine.append(entry)
            elif typeList[i] == "I":
                newLine.append(int(entry))
            elif typeList[i] == "F":
                newLine.append(float(entry))
            i += 1
        
        outTable.append(newLine)
        
    return outTable

# Sorts a table in list or tuple form after several columns in reversed order
def sortTable(table, columns):
    for col in columns:
        table = sorted(table, key=itemgetter(col))
    return table

# Returns column from matrix
def getColumn(matrix,i):
    f = itemgetter(i)
    return map(f,matrix)

def catWords(wordlist, separator=", "):
    return separator.join(wordlist)

def catList(wordlist, separator=", "):
    return separator.join([str(x) for x in wordlist])

def pvalFisher(a,b,c,d):
    return (math.factorial(a+b)*math.factorial(c+d)*math.factorial(a+c)*math.factorial(b+d))/(float(math.factorial(a)*math.factorial(b)*math.factorial(c)*math.factorial(d)*math.factorial(a+b+c+d)))

    
    
tabFile = sys.argv[1]
table = tableTypeConvert([re.split('\t|:',line.rstrip("\n")) for line in open(tabFile)], MERGED_COUNTS)

out = []
for line in table:
    #oddsratio, pval = stats.fisher_exact([[line[A1], line[B1]], [line[A2], line[B2]]])
    line.append(pvalFisher(line[A1], line[B1], line[A2], line[B2]))
    print catList(line, "\t")
    #print catList([line[CHR], line[POS], pvalFisher(line[A1], line[B1], line[A2], line[B2])], "\t")
    #out.append([line[CHR], line[POS], pvalFisher(line[A1], line[B1], line[A2], line[B2])])

