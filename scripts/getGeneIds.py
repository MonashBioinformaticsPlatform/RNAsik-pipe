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
                    help=""
                    )
parser.add_argument('--gffFile',
                    help="check"
                    )

args = parser.parse_args()
gtfFile = args.gtfFile
gffFile = args.gffFile

genesAttributes = {}

biotypes = {
    "gb": 'gene_biotype',
    "gt": 'gene_type',
    "tb": 'transcript_biotype',
    "tt": 'transcript_type'
    }

if gtfFile:
    typesRegex = "\s.([A-z0-9_.-]+)"
    
    for key, value in biotypes.items():
        tweak = value + typesRegex
        biotypes[key]=tweak
        
    with open(gtfFile) as features:
        for i in features:
            if not i.startswith("#"):
                line = i.split('\t')
                ninthField = line[8]
    
                geneId = re.search('gene_id\s.([A-z0-9]+)', ninthField)
                checkName = re.search('gene_name\s.([A-z0-9_.:-]+)', ninthField)
    
                geneName = 'NA'
                geneBiotype = 'NA'
    
                if checkName:
                    geneName = checkName.group(1)
    
                for value in biotypes.values():
                    checkBiotype = re.search(value, ninthField)
                    if checkBiotype:
                        geneBiotype = checkBiotype.group(1)
    
                if geneId:
                    if geneId.group(1) not in genesAttributes:
                        genesAttributes[geneId.group(1)] = []
                        genesAttributes[geneId.group(1)].append(geneName)
                        genesAttributes[geneId.group(1)].append(geneBiotype)
                        genesAttributes[geneId.group(1)].append(line[0])
           
    header = True
    for key, value in genesAttributes.items():
        if header:
            print '\t'.join(("Gene.ID", "Chrom", "Gene.Name", "Biotype"))
            header = False
        print '\t'.join((key, value[2], value[0], value[1]))

# Get gene Ids from GFF file format
if gffFile:
    typesRegex = "=([A-z0-9_.-]+)"
    
    for key, value in biotypes.items():
        tweak = value + typesRegex
        biotypes[key]=tweak
    
    with open(gffFile) as features:
        for i in features:
            line = i.strip()
            if not line.startswith('#'):
                feature = line.split('\t')
                if feature[2] == 'gene':
                    ninthField = feature[8]
    
                    geneId = re.search('ID=([A-z0-9]+)', ninthField)
                    checkName = re.search('Name=([A-z0-9_.:-]+)', ninthField)
    
                    geneName = 'NA'
                    geneBiotype = 'NA'
    
                    if checkName:
                        geneName = checkName.group(1)
    
                    for value in biotypes.values():
                        checkBiotype = re.search(value, ninthField)
                        if checkBiotype:
                            geneBiotype = checkBiotype.group(1)
    
                    if geneId:
                        if geneId.group(1) not in genesAttributes:
                            genesAttributes[geneId.group(1)] = []
                            genesAttributes[geneId.group(1)].append(geneName)
                            genesAttributes[geneId.group(1)].append(geneBiotype)
                            genesAttributes[geneId.group(1)].append(feature[0])
           
    header = True
    for key, value in genesAttributes.items():
        if header:
            print '\t'.join(("Gene.ID", "Chrom", "Gene.Name", "Biotype"))
            header = False
        print '\t'.join((key, value[2], value[0], value[1]))
