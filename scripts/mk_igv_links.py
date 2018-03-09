#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

from __future__ import print_function
import sys
import os
import argparse


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(
    usage='%(prog)s --dir <path/to/your_data>',
    description="scripts for making URL links that you can use to view your "
                "data in IGV. Several file types are supported",
    add_help=True
)
parser.add_argument(
    '--dir',
    required=True,
    help="specify directory with your data files to be made into IGV links. "
         "This directory should be located in the hostable place i.e you "
         "should be able to grab individual file on url"
)
parser.add_argument(
    '--coord',
    help="this will be your default coordinates when IGV loads "
         "for the first time when IGV loads. Pass coordinates "
         "as a string as follows chr12:24565477-24624103"
)
parser.add_argument('--host_name',
                    default='file:///',
                    help='provide your hosting server name [file:///]'
                    )
parser.add_argument(
    '--genome_id',
    help="specify your species genome id. Either IGV inbuilt "
         "onces or your own, custome made. Note if custome made genome id is "
         "used, you'll need to cache .genome file first, see --add_genome_url "
         "options for more."
),
parser.add_argument(
    '--add_genome_url',
    help="specify url to your .genome file, can do file:///"
),
parser.add_argument(
    '--igv_meta',
    type=str2bool,
    nargs='?',
    default=True,
    help="Add meta information, describes in brief what IGV is "
         "and a coupel of links to IGV resources"
)
parser.add_argument(
    '--sep',
    default='_',
    help='This is main separator within the file'
)

args = parser.parse_args()
dir = args.dir
coord = args.coord
host_name = args.host_name
genome_id = args.genome_id
genome_url = args.add_genome_url
igv_meta = args.igv_meta
sep = args.sep

if not dir.endswith("/"):
    dir = dir + '/'

allowed_files = ['bam', 'gtf', 'gff3', 'vcf', 'fa', 'fasta', 'wig', 'bw',
                 'bedGraph']


# NOTE this function going to work on our servers, by probably wont elsewhere
# due to www in the directory path
def get_url(host_name, var):
    home_var = os.getenv('HOME')
    full_path = os.path.abspath(var)
    my_url = host_name + full_path[full_path.index(home_var):]
    # my_url = my_url.replace(':', '%3A').replace("/", "%2F")
    return my_url


# NOTE this is some what a hack to make it work with custome made .genome files
# basically I'm assuming that custome made .genome file is located in some directory
# e.g igv_ref/check.genome and I'll pass it in like this --genome igv_refs/check.genome
# if I would have passed simply --genome check.genome then host_name dose not get prefixed
# and when you load your data igv assumes that there is a local copy of check.genome
# whereas with host_name prefix igv will actually download that genome.
# TODO whole custome .genome files are a little confusing. I think I got main idea.
# basically if genome=http://host_name/blah.genome, which is a keyword inside url encoding
# then igv will attemp to download this resource into its local directory, on linux ~/igv/genomes
# if genome=blah.genome then igv will search ~/igv/genomes for that file, parse and load it genome
# The trick is to download and cache custome genomes so if custome genome
# need to include line like this
# ### [download `blah_id` into local cache](http://localhost:60151/load?genome=http://host_name/blah.genome)
# that blah_id dosen't have to correspond to .genome file name, rather inside blah.genome file (which is zip archive)
# there is property.txt file and there you set id=blah_id
# really need --genome_id and --add_genome_url


igv_port = 'http://localhost:60151/'
cmd_load = 'load?'

cmd_file = 'file='
cmd_genome = 'genome='
cmd_locus = 'locus='
cmd_merge = 'merge=true'  # this is to merge tracks rather than to replace
a = '&'

list_of_files = os.listdir(dir)

if igv_meta:
    igv_header = '# IGV links page'
    igv_intro = '## Intro'
    igv_info = '''It is best to launch local instance of IGV for optimal 
    performance. However it is possible to launch over the web. To launch over 
    the web click on "launch IGV" link below, alternatively click on 
    "download/help" link and get your own copy of IGV. Once you have IGV 
    running simply click on IGV link below to load the data into the IGV.
    Please note that you don\'t have to download files for IGV to work. 
    IGV will get the right information without you downloading the files, 
    they are there simply for your own reference'''

    igv_launch = '- [Launch IGV](http://data.broadinstitute.org/igv/projects/current/igv_lm.jnlp)'
    igv_help = '- [IGV download/help page](http://software.broadinstitute.org/software/igv/download)'
    igv_links_header = '## IGV links'

    print(igv_header)
    print("")
    print(igv_intro)
    print("")
    print(igv_info)
    print("")
    print(igv_launch)
    print("")
    print(igv_help)
    print("")
    print(igv_links_header)
    print("")

if genome_url is not None:
    print("<table class='table'>")
    genome_name = os.path.basename(genome_url)
    print(
        '<tr><td>Add custome genome to local cache</td>'
        '<td>Download IGV genome file</td><tr>')
    print(
        '<tr><td><a href="%s">%s</a></td><td><a href="%s">%s</a></td></tr>' % (
            igv_port + cmd_load + cmd_genome + genome_url, genome_name,
            genome_url,
            genome_name))
    print("</table>")

header = True
print("<table class='table'>")
for f in sorted(list_of_files):
    extn = f.split(".")[-1]

    if extn in allowed_files:
        name = f.split(sep)[0]
        my_url = get_url(host_name, dir + f)

        igv_link = igv_port + \
                   cmd_load + \
                   cmd_file + \
                   my_url + \
                   a + \
                   cmd_merge

        if genome_id is not None:
            igv_link = igv_link + \
                       a + \
                       cmd_genome + \
                       genome_id

        if coord is not None:
            igv_link = igv_link + \
                       a + \
                       cmd_locus + \
                       coord

        if header:
            print('<tr><td>IGV links</td><td>Files for download</td><tr>')
            header = False

        print(
            '<tr><td><a href="%s">%s</a></td>'
            '<td><a href="%s">%s</a></td></tr>' % (igv_link, name, my_url, f))
print("</table>")
