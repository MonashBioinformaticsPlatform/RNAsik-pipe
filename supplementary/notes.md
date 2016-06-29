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


Because of file names like these ones you can't really check for _1 and/or _2
It really has to be _R1 and/or _R2
RNA_10_C6HCPANXX_GGCTACAT_L003_R2.fastq.gz
RNA_10_C6HCPANXX_GGCTACAT_L004_R1.fastq.gz
RNA_10_C6HCPANXX_GGCTACAT_L004_R2.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L003_R1.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L003_R2.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L004_R1.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L004_R2.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L003_R1.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L003_R2.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L004_R1.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L004_R2.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L003_R1.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L003_R2.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L004_R1.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L004_R2.fastq.gz

