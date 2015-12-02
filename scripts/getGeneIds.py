#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# (+_+)

import argparse, sys, os, re, gffutils

# Create optional arguments using argparse module
parser = argparse.ArgumentParser(usage='%(prog)s --dbFile <path/to/your/db_file>',
                                 description="This script creates three column file Gene ID, Gene Name and Gene Biotype",
                                 add_help=True
                                 )
parser.add_argument('--dbFile',
                    required = True,
                    help="specify path/to/databaseFile. You can make such file using python `gffutils` library.\
                          This is augment your merged read count file with other informatin, such as\
                          Public gene names and Biotype"
                    )

parser.add_argument('--outfile',
                    help = ''
                    )

args = parser.parse_args()
dbFile = args.dbFile
outfile = args.outfile

db = gffutils.FeatureDB(dbFile, keep_order=True)
features = db.all_features()

genesAttributes = {}

for line in features:
    geneId = line.attributes['gene_id'].pop()
    geneName = line.attributes['gene_name'].pop()
    geneType = line.attributes['gene_biotype'].pop()
    if geneId not in genesAttributes:
        genesAttributes[geneId] = [geneName, geneType]


with open(outfile, 'w') as o:
    for k,v in genesAttributes.items():
        if header:
            o.write('\t'.join(("Gene.ID", "Gene.Name", "Biotype\n")))
            header = False
        items = '\t'.join(v)
        o.write('\t'.join((k, items))+'\n')
