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

args = parser.parse_args()
dbFile = args.dbFile

db = gffutils.FeatureDB(dbFile, keep_order=True)
features = db.all_features()

genesAttributes = {}

for i in features:
    line = i.attributes
    geneId = line['gene_id'].pop()

    if line.get('gene_name'):
        geneName = line['gene_name'].pop()
    else:
        geneName = 'NA'

    if line.get('gene_biotype'):
        geneType = line['gene_biotype'].pop()
    else:
        geneType = 'NA'

    if geneId not in genesAttributes:
        genesAttributes[geneId] = [geneName, geneType]

header = True

for k,v in genesAttributes.items():
    if header:
        print '\t'.join(("Gene.ID", "Gene.Name", "Biotype"))
        header = False
    items = '\t'.join(v)
    print '\t'.join((k, items))
