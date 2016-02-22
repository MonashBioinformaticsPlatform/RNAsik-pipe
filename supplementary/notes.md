Strandedness: By default, the counting script assumes your library to be strand-specific, i.e., reads are
aligned to the same strand as the gene they originate from. If you have used a library preparation
protocol that does not preserve strand information (i.e., reads from a given gene can appear equally
likely on either strand), you need to inform the script by specifying the option “-s no”. If your library
preparation protocol reverses the strand (i.e., reads appear on the strand opposite to their gene of
2The possibility to process paired-end data from a file sorted by position is based on recent contributions of PaulTheodor
Pyl to HTSeq.
Inferring differential exon usage in RNA-Seq data with the DEXSeq package 6
origin), use “-s reverse”. In case of paired-end data, the default (-s yes) means that the read from
the first sequence pass is on the same strand as the gene and the read from the second pass on the
opposite strand (“forward-reverse” or “fr” order in the parlance of the Bowtie/TopHat manual) and the
options -s reverse specifies the opposite case.
SAM and BAM files: By default, the script expects its input to be in plain-text SAM format. However,
it can also read BAM files, i.e., files in the the compressed binary variant of the SAM format. If you
wish to do so, use the option “-f bam”. This works only if you have installed the Python package
pysam, which can be found at https://code.google.com/p/pysam/.
Alignment quality: The scripts takes a further option, -a to specify the minimum alignment quality (as
given in the fifth column of the SAM file). All reads with a lower quality than specified (with default
-a 10) are skipped.
Help pages: Calling either script without arguments displays a help page with an overview of all options
and arguments.

### Get RNAseq metrics
[RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) requires you BAM to be sorted,
reordered and have duplicates marked. Here is detailed [instructions](supplementary/RNAseQC-manual.pdf)
for how to prepare your BAMs files for RNAseQC, BUT the good news is you don't even need to worry about this!
`RNAsik-pipe` takes care of long and laborious BAM file manipulation for RNA-SeQC tools, just flag 
`-prePro` to get your BAMS in the right shape and `-RNAseQC` to get the actual report
