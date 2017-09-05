#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Author: serine
# Date: 10/11/2016

import os
import sys
import math
import argparse

parser = argparse.ArgumentParser(usage='%(prog)s --logsDir <path/to/logFiles/directory>',
                                 description="This script summarises log files information into html table",
                                 add_help=True
                                )
parser.add_argument('--logsDir',
                     required=True,
                     help="specify directory with your BAM files, which should also hold `*Log.final.out` files"
                    )

parser.add_argument('--pattern',
                     default=".summary",
                     help="specify ending of your log files, e.g featureCounts is .summary"
                    )

parser.add_argument('--flip',
                     action='store_true',
                     help="Can flip html table 90 degress"
                    )

args = parser.parse_args()
logsDir = args.logsDir
flip = args.flip
pattern = args.pattern

#s_name = "Status"
#assign = "Assigned"
#ambig = "Unassigned_Ambiguity"
#multi_map = "Unassigned_MultiMapping"
#no_feat = "Unassigned_NoFeatures"
#unmaped = "Unassigned_Unmapped"
#un_map_qual = "Unassigned_MappingQuality"
#un_frag_len = "Unassigned_FragmentLength"
#chimer = "Unassigned_Chimera"
#secondary = "Unassigned_Secondary"
#non_junc = "Unassigned_Nonjunction"
#dups = "Unassigned_Duplicate"
#
#keys = [s_name,
#        assign,
#        ambig,
#        multi_map,
#        no_feat,
#        unmaped,
#        un_map_qual,
#        un_frag_len,
#        chimer,
#        secondary,
#        non_junc,
#        dups
#        ]

list_of_files = os.listdir(logsDir) 
data_dict = {}

def inner_flip(dd):

    flipped = {}

    l = len(list(dd.values())[0])
    k = list(dd.keys())

    flipped[k.pop(0)] = k
    for i in range(l):
        dat = [d[i] for d in dd.values()]
        flipped[dat.pop(0)] = dat

    return flipped

def make_flip(d):
    dd = {}
    for k,v in d.items():
         dd[k] = inner_flip(v)
    return dd
    
def which_strand(d):

    assigned_reads = {}
    
    for k,v in data_dict.items():
        counts = map(int, v['Assigned'])
        s = sum(counts)
        assigned_reads[k] = s
    
    forward = int(assigned_reads['ForwardStrandedCounts'])
    reverse = int(assigned_reads['ReverseStrandedCounts'])
    nonstranded = int(assigned_reads['NonStrandedCounts'])
    
    # if positive data is forward stranded
    # if negative data is reverse stranded
    strnd_val = float(forward-reverse)/float(forward+reverse)
    
    # confidence test
    non_strnd_test = (20-1)/float(20+1) #0.904
    strnd_test = (55-45)/float(55+45)   #0.1
    def sign(x):
        if x >= 0:
            return 1
        return -1
    
    if abs(strnd_val) < strnd_test:
        #print "Data is stranded %s" % sign(strnd_val)

        if strnd_val >= 0:
            return "ForwardStrandedCounts,0"
        return "ReverseStrandedCounts,0"

    elif abs(strnd_val) > non_strnd_test:
        #print "Data is non stranded %s" % sign(strnd_val)
        return "NonStrandedCounts,0"
    #NOTE default to non stranded counts, should do be ok to get through RNAsik run
    elif strnd_test < abs(strnd_val) < non_strnd_test:
        #print "It is hard to guess what strand the data is %s" % sign(strnd_val)
        return "NonStrandedCounts,1"
    else:
        #print "ERROR: This should not happend"
        return "NonStrandedCounts,1"

for text_file in list_of_files:
    if text_file.endswith(pattern):
        name = text_file.split('.')[0]
        full_path = os.path.join(logsDir, text_file)
        with open(full_path) as handler:
            for i in handler:
                line = i.strip().split("\t")
                key = line.pop(0)
                if name not in data_dict:
                    data_dict[name] = {}
                if key not in data_dict[name]:
                    data_dict[name][key] = None

                if key == "Status":
                    data_dict[name][key] = [os.path.basename(b).split("_")[0] for b in line]
                else:
                    data_dict[name][key] = line

print(which_strand(data_dict))
