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

- [Introduction](#introduction)
  - [FASTQ files explained](#fastq-files-explained)
    - [Directory with FASTQ files](#directory-with-fastq-files)
    - [Directory with subdirectories with FASTQ files](#directory-with-subdirectories-with-fastq-files)
  - [Get RNAseq metrics](#get-rnaseq-metrics)
  - [get your counts](#get-your-counts)

## Introduction

Your standard [RNA-seq](https://en.wikipedia.org/wiki/RNA-Seq) workflow as follows:

1. get [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) reads
2. align them to your reference genome (your reference genome is given in [FASTA](https://en.wikipedia.org/wiki/FASTA_format) file). [STAR aligner](https://github.com/alexdobin/STAR) is used in `RNAsik-pipe` for that
3. count how many reads have mapped to the gene feature. You need [SAM/BAM files](https://samtools.github.io/hts-specs/SAMv1.pdf) for this. [featureCounts](http://subread.sourceforge.net/) is used in `RNAsik-pipe` for that
4. Then you can choose to use [limma](https://bioconductor.org/packages/release/bioc/html/limma.html) and [edgeR](https://bioconductor.org/packages/release/bioc/html/edgeR.html) in [R](https://en.wikipedia.org/wiki/R_programming_language) to do differential gene expression analysis Or you can simply upload your counts file to [Degust](http://victorian-bioinformatics-consortium.github.io/degust/), which is interactive and user friendly web tool

**OR you can just use** `RNAsik-pipe`

`RNAsik-pipe` is a simple tools that wraps several other tools together to obstruct away the same repetitive work of retyping the same commands over the same number of tools just to get your differentially expressed genes. Simply provide `RNAsik-pipe` with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files directory and your reference files such as [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and [GTF](http://mblab.wustl.edu/GTF22.html) and press Go !

Even though most tools used inside `RNAsik-pipe` can handle [GFF](https://en.wikipedia.org/wiki/General_feature_format) at this stage only [GTF](http://mblab.wustl.edu/GTF22.html) file is supported by the pipeline.

One important note about [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files, `RNAsik-pipe` assumes that if the data is paired-end than it will have upper case **R** following by the number 1 or 2. `RNAsik-pipe` further assumes that both **R1** and **R2** have and underscore prefix - `_R1`, `_R2`. If your data is single-end and just has `_R1` in the file name, this is fine and `RNAsik-pipe` will handle those files correctly. `RNAsik-pipe` will also handle single-end data without any of **R's** in the file name correctly, but you might have to specify your own `-fqRegex` for more refer to [User manual](supplementary/docs.md).

### FASTQ files explained

Your raw data will always come in [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) format. The number of [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files will depend on many things including:

  - Number of samples 
  - Number of replicates 
  - Your sample was split into different lanes
  - Your are sequencing paired-end data

#### Directory with FASTQ files

Your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files might reside in one directory e.g directory per experiment

![fqDir](supplementary/rawDataDir.png)

In this example sample _14-09157_, which might be _WT_ sample was split across two lanes `L001` and `L002` during sequencing, this is some what typical of Illumina data. Therefore one sample is represented by two files, one for each lane. We can also see that this is paired end data, which means for each file there has to be a pair file, that is _R1_ and _R2_. In summary single sample, e.g _WT_ is covered by four FASTQ files:

  - *14-09157_L001_R1.fastq.gz*
  - *14-09157_L001_R2.fastq.gz*

   And 

  - *14-09157_L002_R1.fastq.gz*
  - *14-09157_L002_R2.fastq.gz*

The files for the same sample that were split across multiple lanes need to be merged together at some point during analysis. There are at least two most common ways to go about merging them together:

  1. Using `cat` command to concatenate files across different lanes e.g `cat 14-09157_L001_R1.fastq.gz 14-09157_L002_R1.fastq.gz > 14-09157_merged.fastq.gz`

  2. Let your aligner (if it is capable) to merge your files for you on the fly (during alignment step). [STAR aligner](https://github.com/alexdobin/STAR) can merger [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) on the fly.

#### Directory with subdirectories with FASTQ files

Your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files might also reside in their own subdirectory e.g  subdirectory per sample inside directory per experiment

![test](supplementary/rawDataDirs.png)

In this example each sample is placed into its own directory. Now we can see directory `Sample_14-09157`, 
which will hold four files described above.

**`RNAsik-pipe` can work with either of those two options. Specify your "root" directory either with `-fqDir` or `-fqDirs` options.**

### Get RNAseq metrics

  [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) requires you BAM to be sorted,
  reordered and have duplicates marked. Here is detailed [instructions](supplementary/RNAseQC-manual.pdf)
  for how to prepare your BAMs files for RNAseQC, BUT the good news is you don't even need to worry about this!
  `RNAsik-pipe` takes care of long and laborious BAM file manipulation for RNA-SeQC tools, just flag 
  `-prePro` to get your BAMS in the right shape and `-RNAseQC` to get the actual report

### Get your read counts

  Do you want to do differential gene expression analysis..? just flag `-count` and you will get your counts


