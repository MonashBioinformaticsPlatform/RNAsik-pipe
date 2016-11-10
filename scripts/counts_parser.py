#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Author: serine
# Date: 10/11/2016

import os
import sys
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

    l = len(dd.values()[0])
    k = dd.keys()

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
    dd = {}

    for k, v in d.items():
        dd[k] = sum(map(int, v["Assigned"]))

    return max(dd, key=dd.get)

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

print which_strand(data_dict)

#if flip:
#    d = make_flip(data_dict)
#else:
#    d = data_dict
#
#for a, b in sorted(d.items()):
#    print "<table class='check' border=1 frame=void rules=all cellpadding=5px>"
#
#    tbl_header = b.pop("Status")
#    tbl_header.insert(0, a)
#    cell = '<td>%s</td>'
#    cells = '<tr>'+cell * len(tbl_header)+'</tr>'
#    print cells % tuple(tbl_header)
#
#    for k, v in sorted(b.items()):
#
#        tbl_data = v
#        tbl_data.insert(0, k)
#        cell = '<td>%s</td>'
#        cells = '<tr>'+cell * len(tbl_data)+'</tr>'
#        print cells % tuple(tbl_data)
#
#    print "</table>"
#    print '''<p>Some long text descriptiont goes here </p>'''
