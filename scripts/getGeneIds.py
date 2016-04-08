#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import argparse
import sys
import os
import re

parser = argparse.ArgumentParser(usage='%(prog)s --gtfFile <path/to/your/db_file>',
                                 description="This script creates three column file Gene ID, Gene Name and Gene Biotype",
                                 add_help=True
                                 )
parser.add_argument('--gtfFile',
                    required = True,
                    help=""
                    )

args = parser.parse_args()
gtfFile = args.gtfFile

genesAttributes = {}

biotypes = {
    "gb": 'gene_biotype',
    "gt": 'gene_type',
    "tb": 'transcript_biotype',
    "tt": 'transcript_type'
    }

typesRegex = "\s.([A-z0-9_.-]+)"

for key, value in biotypes.items():
    tweak = value + typesRegex
    biotypes[key]=tweak
    
with open(gtfFile) as features:
    for i in features:
        if not i.startswith("#"):
            ninthField = i.split('\t')[8]
            geneId = re.search('gene_id\s.([A-z0-9]+)', ninthField)
            geneName = re.search('gene_name\s.([A-z0-9_.-]+)', ninthField)
            geneBiotype = ''

            for value in biotypes.values():
                checkBiotype = re.search(value, ninthField)
                if checkBiotype:
                    geneBiotype = checkBiotype

            if geneId:
                if geneId.group(1) not in genesAttributes:
                    genesAttributes[geneId.group(1)] = []
                    genesAttributes[geneId.group(1)].append(geneName.group(1))
                    genesAttributes[geneId.group(1)].append(geneBiotype.group(1))
        
header = True
for key, value in genesAttributes.items():
    if header:
        print '\t'.join(("Gene.ID", "Gene.Name", "Biotype"))
        header = False
    print '\t'.join((key, value[0], value[1]))
