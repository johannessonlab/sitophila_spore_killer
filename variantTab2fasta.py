#!/usr/bin/env python


import sys
import os
import argparse
from Bio import SeqIO


def tabContig(contig, copies):
    tab = [contig] * copies
    return map(list,map(None,*tab))

def wrap(text, width=70):
    return '\n'.join(text[i:i+width] for i in range(0, len(text), width))

def printContig(table, contigname):
    oFN = args.output + "." + contigname + ".fasta"
    outfile = open(oFN, "w")
    
    if len(strains) > 1:
        transTab = map(list,map(None,*table))
    else:
        transTab = [[]]
        for x,i in enumerate(table):
            #print x, i
            transTab[0].append(i[0])
    
    #print transTab[0:10]
    
    for x, line in enumerate(transTab):
        lineStr = "".join(line)
        outfile.write(">" + allStrains[x].split(args.splitter)[0] + "\n")
        outfile.write(wrap(lineStr.replace(".", "-")) + "\n")
    
    if args.reference:
        refcontig = str(contigDict[contigname])
        outfile.write(">" + args.reference + "\n")
        outfile.write(wrap(refcontig.replace(".", "-")) + "\n")
        
    
    outfile.close()

def dashedContig(cdict):
    outdict = {}
    for key, val in cdict.iteritems():
        outdict[key] = "-"*len(val.seq)
    return outdict

def seqContig(cdict):
    outdict = {}
    for key, val in cdict.iteritems():
        outdict[key] = val.seq
    return outdict

parser = argparse.ArgumentParser(description='Script that converts a GATK VariantsToTable file to an aligned fasta.')
parser.add_argument('filename', help='Variant table file name')
#parser.add_argument('-s','--size',help='Chromosome size. Default: Last line in file.', type=int)
#parser.add_argument('-w','--window',help='Sliding window size. Default: 2000', type=int, default=2000)
#parser.add_argument('-p','--step',help='Sliding window step length. Default: 2000', type=int, default=2000)
parser.add_argument('-g','--genome',help='Genome fasta file.')
parser.add_argument('-n','--nomissing',help='Outputs sites missing in the VCF file as dashes (-).', dest='nomissing', action='store_true')
parser.add_argument('-c','--contigs',help='List of contigs to export in quotations.')
#parser.add_argument('-o','--contig',help='Specify one contig to limit the analysis to.')
#parser.add_argument('-r', '--reference', dest='reference', action='store_true')
parser.add_argument('-r', '--reference',help='Includew reference genome. Reference strain name as parameter.')
#parser.add_argument('-s','--strains',help='List of strains to export in quotations.')
parser.add_argument('-o','--output',help='Output file name.')
parser.add_argument('-s','--splitter',help='Character that splits out strain name. Default=.', default=".")
args = parser.parse_args()

if args.reference:
    print "Include reference genome. Reference name: " + args.reference
else:
    print "Reference genome not included."

print "Reading genome..."
cDict = SeqIO.to_dict(SeqIO.parse(args.genome, "fasta"))

if args.nomissing:
    contigDict = dashedContig(cDict)
else:
    contigDict = seqContig(cDict)
    
    
#strainList = [line.rstrip("\n").split() for line in args.strains]
#contigList = [line.rstrip("\n").split() for line in args.contigs]

tfile = open(args.filename)

allStrains = tfile.readline().rstrip("\n").split("\t")[2:]

strains = allStrains

print allStrains

prevContig = ""

for line in tfile:
    ll = line.replace("*", ".").rstrip("\n").split()

    if ll[0] != prevContig:
        if prevContig:
            #print contTab[0:10]
            printContig(contTab, prevContig)

        print "Parsing " + ll[0]
        contTab = tabContig(contigDict[ll[0]], len(strains))
        #contTab = tabContig(str(contigDict[ll[0]].seq), len(strains))
        
        lout =[]
        for i in ll[2:]:
            if len(i) > 1:
                lout.append(".")
            else:
                lout.append(i)
                
        contTab[int(ll[1])-1] = lout
        prevContig = ll[0]
    else:
        lout=[]
        for i in ll[2:]:
            if len(i) > 1:
                lout.append(".")
            else:
                lout.append(i)
        contTab[int(ll[1])-1] = lout

printContig(contTab, prevContig)
