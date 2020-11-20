#!/usr/bin/env python3

# Author: serine
# Date: 10/11/2016
# Last updated: 12/12/2018

import os
import sys
import math
import argparse
import pandas as pd

parser = argparse.ArgumentParser(
    usage='%(prog)s --logs_dir <path/to/log_file> --samples_sheet <path/to/samples_sheet>',
    description="This script summarises log files information into html table",
    add_help=True
)
parser.add_argument('-d',
                    '--logs_dir',
                    metavar='FILE',
                    required=True,
                    help="specify directory with your BAM files, which should also hold "
                         "`*Log.final.out` files"
                    )
parser.add_argument('-s',
                    '--samples_sheet',
                    metavar='FILE',
                    required=True,
                    help="path to samplesSheet.txt file, format "
                         "old_prefix\tnew_prefix"
                    )
parser.add_argument('-p',
                    '--pattern',
                    metavar='STR',
                    default=".summary",
                    help="specify ending of your log files, e.g featureCounts is .summary"
)
parser.add_argument('-o',
                    '--outdir',
                    metavar='PATH',
                    default=".",
                    help="specify directory for the output, two files will be created"
                         "'strandInfoAll.txt' and 'strandInfoGuess.txt'"
                         " default currect directory"
)

args = parser.parse_args()
logs_dir = args.logs_dir
samples_sheet = args.samples_sheet
pattern = args.pattern
outdir = args.outdir

ss = open(samples_sheet).read().split("\n")
ss = [s.split("\t")[1] for s in ss if s]
sorted(ss, key=len)
ss = ss[::-1]

# Two files out
#  - strandInfoGuess.txt
#  - strandInfoAll.txt

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

def which_strand(strnd_val):

    # confidence test
    # non_strnd_test = (20-1)/float(20+1) #0.904
    # strnd_test = (55-45)/float(55+45)   #0.1
    strnd_test = float(19 - 1) / float(20 + 1)  # 0.857
    non_strnd_test = float(55 - 45) / float(55 + 45)  # 0.1

    if abs(strnd_val) > strnd_test:
        # print("Data is stranded %s" % sign(strnd_val))
        if strnd_val >= 0:
            #return "ForwardStrandedCounts,%s,0" % str(strnd_val)
            return ["ForwardStrandedCounts", strnd_val, 0]

        #return "ReverseStrandedCounts,%s,0" % str(strnd_val)
        return ["ReverseStrandedCounts", strnd_val, 0]

    elif abs(strnd_val) < non_strnd_test:
        # print("Data is non stranded %s" % sign(strnd_val))
        #return "NonStrandedCounts,%s,0" % str(strnd_val)
        return ["NonStrandedCounts", strnd_val, 0]
    # NOTE default to non stranded counts, should be ok to get through RNAsik run
    elif non_strnd_test < abs(strnd_val) < strnd_test:
        # print("It is hard to guess what strand the data is %s" % sign(strnd_val))
        return ["NonStrandedCounts", strnd_val, 1]
    else:
        sys.exit("ERROR: This should not happend")
        # return "NonStrandedCounts,1"

def get_name(raw_name, ss):
    #TODO this can be buggy when column name contains forward slash (/)
    # this function returns None when this is the case. Forward slash should be allowed in the column name
    base_name = os.path.basename(raw_name)
    for name in ss:
        if base_name.startswith(name):
            return name

    #TODO need to raise an error here if
    # it didn't exit in the for loop.
    #raise NoNameError: "Can't happen"

def get_df(f, name):
    df = pd.read_csv(f, sep = "\t")
    df2 = df.rename(columns=lambda x: get_name(x, ss), inplace=False)
    tmp = df2.iloc[0].to_frame().reset_index()
    df3 = tmp.rename(columns={tmp.columns[0]: "sample", tmp.columns[1]: name})
    # dropping second line, not too sure why, fucking pandas
    df3.drop(df3.index[:1], inplace=True)

    return df3

dfs = []

for text_file in list_of_files:
    if text_file.endswith(pattern):
        name = text_file.split('.')[0]
        full_path = os.path.join(logs_dir, text_file)

        dfs.append(get_df(full_path, name))

tmp = pd.merge(dfs[0], dfs[1], how = "left", on = 'sample')
df = pd.merge(tmp, dfs[2], how = "left", on = 'sample')

df['frac'] = (df['ForwardStrandedCounts'] - df['ReverseStrandedCounts']) / (df['ForwardStrandedCounts'] + df['ReverseStrandedCounts'])

#NOTE can return sorted table, but not sure if that will
# generically useful? one can use unix sort if needed
#df.sort_values(by=['frac'], inplace = True)

if not os.path.isdir(outdir) and not os.path.exists(outdir):
    sys.exit("ERROR: %s doesn't exists, make sure it does" % outdir)

out_fn_all = os.path.join(outdir, "strandInfoAll.txt")
out_fn_guess = os.path.join(outdir, "strandInfoGuess.txt")

df.to_csv(out_fn_all, sep = "\t", index = False)

df2 = df.drop(['sample', 'frac'], axis = 1)
df3 = df2.sum(axis = 0)
tot_frac = (df3['ForwardStrandedCounts'] - df3['ReverseStrandedCounts']) / (df3['ForwardStrandedCounts'] + df3['ReverseStrandedCounts'])

df_sum = pd.DataFrame([which_strand(tot_frac)])
df_sum.to_csv(out_fn_guess, sep = ",", index = False, header = False)
