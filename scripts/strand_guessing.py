#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Author: serine
# Date: 10/11/2016

from __future__ import print_function
import os
import sys
import math
import argparse

parser = argparse.ArgumentParser(
    usage='%(prog)s --logs_dir <path/to/log_files/directory>',
    description="This script summarises log files information into html table",
    add_help=True
)
parser.add_argument(
    '--logs_dir',
    required=True,
    help="specify directory with your BAM files, which should also hold "
         "`*Log.final.out` files"
)

parser.add_argument(
    '--pattern',
    default=".summary",
    help="specify ending of your log files, e.g featureCounts is .summary"
)

args = parser.parse_args()
logs_dir = args.logs_dir
pattern = args.pattern

# s_name = "Status"
# assign = "Assigned"
# ambig = "Unassigned_Ambiguity"
# multi_map = "Unassigned_MultiMapping"
# no_feat = "Unassigned_NoFeatures"
# unmaped = "Unassigned_Unmapped"
# un_map_qual = "Unassigned_MappingQuality"
# un_frag_len = "Unassigned_FragmentLength"
# chimer = "Unassigned_Chimera"
# secondary = "Unassigned_Secondary"
# non_junc = "Unassigned_Nonjunction"
# dups = "Unassigned_Duplicate"
#
# keys = [s_name,
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

list_of_files = os.listdir(logs_dir)
data_dict = {}


# def sign(x):
#    if x >= 0:
#        return 1
#    return -1

def which_strand(d):
    assigned_reads = {}

    for k, v in list(data_dict.items()):
        counts = list(map(int, v['Assigned']))
        s = sum(counts)
        assigned_reads[k] = s

    forward = int(assigned_reads['ForwardStrandedCounts'])
    reverse = int(assigned_reads['ReverseStrandedCounts'])
    # nonstranded = int(assigned_reads['NonStrandedCounts'])

    # TODO account for when assignment has zero counts in all of the conditions
    # then this becomes division by zero with error
    #    strnd_val = float(forward-reverse)/float(forward+reverse)
    #  ZeroDivisionError: float division by zero
    try:
        strnd_val = float(forward - reverse) / float(forward + reverse)
    except ZeroDivisionError:
        sys.exit("ERROR: Looks like you've got zero read counts against "
                 "features, check that your FASTA and annotation files "
                 "corresponds")
    # TODO not particular happy with this work around / fixture
    # I want getStrandInfo task to stop pipeline run since fair few steps
    # depend on strand information, but was having tech difficulties with bds
    # so leave it as is for now

    # confidence test
    # non_strnd_test = (20-1)/float(20+1) #0.904
    # strnd_test = (55-45)/float(55+45)   #0.1
    strnd_test = float(20 - 1) / float(20 + 1)  # 0.904
    non_strnd_test = float(55 - 45) / float(55 + 45)  # 0.1

    if abs(strnd_val) > strnd_test:
        # print("Data is stranded %s" % sign(strnd_val))
        if strnd_val >= 0:
            return "ForwardStrandedCounts,%s,0" % str(strnd_val)

        return "ReverseStrandedCounts,%s,0" % str(strnd_val)

    elif abs(strnd_val) < non_strnd_test:
        # print("Data is non stranded %s" % sign(strnd_val))
        return "NonStrandedCounts,%s,0" % str(strnd_val)
    # NOTE default to non stranded counts, should be ok to get through RNAsik run
    elif non_strnd_test < abs(strnd_val) < strnd_test:
        # print("It is hard to guess what strand the data is %s" % sign(strnd_val))
        return "NonStrandedCounts,%s,1" % str(strnd_val)
    else:
        sys.exit("ERROR: This should not happend")
        # return "NonStrandedCounts,1"


for text_file in list_of_files:
    if text_file.endswith(pattern):
        name = text_file.split('.')[0]
        full_path = os.path.join(logs_dir, text_file)
        with open(full_path) as handler:
            for i in handler:
                line = i.strip().split("\t")
                key = line.pop(0)
                if name not in data_dict:
                    data_dict[name] = {}
                if key not in data_dict[name]:
                    data_dict[name][key] = None

                if key == "Status":
                    data_dict[name][key] = [os.path.basename(b).split("_")[0]
                                            for b in line]
                else:
                    data_dict[name][key] = line

print(which_strand(data_dict))
