"""
https://www.biostars.org/p/152517/

Example of how to work with Ensembl release 81 GTF files, which:

    1) already have genes and transcripts included

    2) have unique IDs for genes, transcripts, and exons in the corresponding
       "<featuretype>_id" attribute

    3) do not have unique IDs for CDS, stop_codon, start_codon, UTR.

See background info at on database IDs at:
    https://pythonhosted.org/gffutils/database-ids.html


GTF file from

ftp://ftp.ensembl.org/pub/release-81/gtf/mus_musculus/Mus_musculus.GRCm38.81.gtf.gz

"""

import gffutils
import time
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('input', help='Ensembl Release 81 GTF file')
ap.add_argument('database', help='Database to be created')
ap.add_argument('--testN', type=int,
              help='Run a test using only the first N features, and then '
                'print out some example feature IDs and their attributes')
ap.add_argument('--force', action='store_true',
                help='Overwrite an existing database')
args = ap.parse_args()


def first_n_features(data, n=5000):
    """
    Useful for testing: only use the first `n` features of source data
    """
    for i, feature in enumerate(gffutils.iterators.DataIterator(data)):
        if i > n:
            break
        yield feature


# Note: this function is optional; if you don't want these IDs then comment out 
# the lines at [1] below
def subfeature_handler(f):
    """
    Given a gffutils.Feature object (which does not yet have its ID assigned),
    figure out what its ID should be.

    This is intended to be used for CDS, UTR, start_codon, and stop_codon
    features in the Ensembl release 81 GTF files.  I figured a reasonable
    unique ID would consist of the parent transcript and the feature type,
    followed by an autoincrementing number.

    See https://pythonhosted.org/gffutils/database-ids.html#id-spec for
    details and other options.
    """
    return ''.join(
        ['autoincrement:',
         f.attributes['transcript_id'][0],
         '_',
         f.featuretype])


# gffutils can spend a lot of time trying to decide on a unique ID for each
# feature. So we have to give it hints of where to look in the attributes.
#
# We also tell it to use our subfeature_handler function for featuretypes with
# no unique IDs.
id_spec = {
    'exon': 'exon_id',
    'gene': 'gene_id',
    'transcript': 'transcript_id',

    # [1] These aren't needed for speed, but they do give nicer IDs.
    'CDS': [subfeature_handler],
    'stop_codon': [subfeature_handler],
    'start_codon': [subfeature_handler],
    'UTR':  [subfeature_handler],
}

if args.testN is None:
    data = args.input
else:
    data = first_n_features(args.input, args.testN)

t0 = time.time()
db = gffutils.create_db(
    data,
    args.database,

    # Since Ensembl GTF files now come with genes and transcripts already in
    # the file, we don't want to spend the time to infer them (which we would
    # need to do in an on-spec GTF file)
    disable_infer_genes=True,
    disable_infer_transcripts=True,

    # Here's where we provide our custom id spec
    id_spec=id_spec,

    # "create_unique" runs a lot faster than "merge"
    # See https://pythonhosted.org/gffutils/database-ids.html#merge-strategy
    # for details.
    merge_strategy='create_unique',
    verbose=True,
    force=args.force,
)
t1 = time.time()

if args.testN is not None:
    for ex in ['CDS', 'start_codon', 'stop_codon', 'UTR']:
        c = db.features_of_type(ex).next()
        print '-----------------------------'
        print 'Example "{0}" feature; ID="{1}"'.format(ex, c.id)
        print 'Attributes:\n{0}'.format(c.attributes)

print "\n\n{0:.1f}s to create database".format(t1 - t0)
