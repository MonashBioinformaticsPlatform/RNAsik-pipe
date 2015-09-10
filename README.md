# `RNAsik-pipe` easy and quick RNA-seq(uencing) pipeline

## Content

- [Introduction](#introduction)
- [Quick start](#quickstart)
- [Prerequisites](#prerequisites)

## Introduction

1. Get your FASTQ files

Your raw data will always come in FASTQ format. The number of FASTQ files will really depend on many things
including:

  - Number of samples 
  - Number of replicates 
  - Your sample was split into different lanes
  - Your are sequencing paired-end data

Also your FASTQ files might reside in one directory - directory per experiment 
OR 
Each sample might be put into its own subdirectory 

Well, `RNAsik-pipe` can either take your project directory with FASTQ files with `-fqDir` parameter
OR `RNAsik-pipe` can take your project directory with sub-directories for you replicates perphaps with 
`-fqDirs` parameter

2. Get RNA-seq metrics with RNA-SeQC report

`RNAsik-pipe` takes care of long and laborious BAM file manipulation for RNA-SeQC tools, just flag 
`-prePro` to get your BAMS in the right shape and `-RNAseQC` to get actual report

3. Get you read counts

Do you want to do differential gene expression analysis..? just flag `-count` and you will get your counts

## Quick start


1. Get [BigDataScript](http://pcingola.github.io/BigDataScript/)

You need to have installed BDS first, which is rather straight forward just follow [BDS installation instructions](http://pcingola.github.io/BigDataScript/download.html)

2. Get the pipeline

`git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe.git` and you can run `RNAsik-pipe`
simply by typing it in the command line. 

Optionally you can add `RNAsik-pipe/` directory to the path 

3. Run it !

- To align `RNAsik-pipe -star -fqRegex A -genomeIndex path/to/yourIndexDirectory` 
- To get counts `RNAsik-pipe -count -gtfFile path/to/yourGTFfile`
- To get RNA-SeQC report `RNAsik-pipe -prePro -fastaRef path/to/yourFASTAreference-file -RNAseQC`

You should really specify all options at the start and let `RNAsik-pipe` to take of everything else

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc)
- [featureCounts](http://subread.sourceforge.net/)

## Caveats 

- At the moment `STAR aligner` has fixed options, here is the default:

```BASH
STAR --runThreadN 26 \
     --genomeDir $genomeIndex \
     --outSAMtype BAM Unsorted \
     --outSAMattrRGline ID:001 CN:AGRF DS:RNA-seq PL:ILLUMINA PM:MiSeq SM:$uniqueName \
     --outSAMunmapped Within \
     --readFilesCommand zcat \
     --readFilesIn $read1 $read2 \
     --outFileNamePrefix $preFix
```

- Right now only `featureCounts` is supported for read counting
- At the moment there isn't an option to choose the strand direction for read counts. `RNAsik-pipe` simply
counts using both stranded NO and stranded REVERSE options

