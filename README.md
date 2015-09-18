# `RNAsik-pipe` easy and quick RNA-seq(uencing) pipeline

> RNAsik-pipe is written in pure [BigDataScrip](http://pcingola.github.io/BigDataScript/) (BDS) language
> There are many advantages in using BDS, but the main ones are:
>  1. One script works on your local machine, on your remote server and on you cluster
>  2. Checkpoints - never need to run your job from the start in case it stopped. Start from where you left off
>  3. Remote access to your data. Do need to worry about scping you data to your server, just point RNAsik-pipe
> to your cloude store if you like
> As for RNAsik-pipe itself it just makes your life easy. One script solves many problems. Simply give your
> raw data to RNAsik-pipe and provide with the reference files and press go ! [Enter]

## Content

- [Introduction](#introduction)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)

## Introduction

1. Get your FASTQ files

  Your raw data will always come in FASTQ format. The number of FASTQ files will depend on many things
  including:

  - Number of samples 
  - Number of replicates 
  - Your sample was split into different lanes
  - Your are sequencing paired-end data

  Your FASTQ files might reside in one directory e.g directory per experiment

  ![fqDir](supplementary/rawDataDir.png)

  In this example sample 14-09157, which might WT is split across two lanes `L001` and `L002`, which is 
  typical of Illumina sequencing. That is two files, one for each lane. We can also see that this is
  paire end data. That means for each file there has to be a pair file, that is R1 and R2. In summary
  single sample, e.g WT is covered by four FASTQ files:
     - 14-09157_L001_R1.fastq.gz
     - 14-09157_L001_R2.fastq.gz
                 AND 
     - 14-09157_L002_R1.fastq.gz
     - 14-09157_L002_R2.fastq.gz
  you can use `cat` command to concatenate files across different lanes
  e.g `cat 14-09157_L001_R1.fastq.gz 14-09157_L002_R1.fastq.gz > 14-09157_merged.fastq.gz` or you can merge
  BAM files with `samtools` later. `STAR` aligner can merger on the fly and what RNAsik-pipe is using.

  OR 

  Each sample might be put into its own subdirectory e.g

  ![test](supplementary/rawDataDirs.png)
  
  In this example each sample is placed into its own directory. Now we can see directory `Sample_14-09157`, 
  which will hold four files for described above.

  `RNAsik-pipe` can work with either of those two options. Specify your "root" directory either with `-fqDir`
  or `-fqDirs` options.

2. Get RNA-sequencing metrics with RNA-SeQC report

  [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) requires you BAM to be sorted,
  reordered and have duplicates marked. Here is detailed [instructions](supplementary/RNAseQC-manual.pdf)
  for how to prepare your BAMs files for RNAseQC, BUT the good news is you don't even need to worry about this!
  `RNAsik-pipe` takes care of long and laborious BAM file manipulation for RNA-SeQC tools, just flag 
  `-prePro` to get your BAMS in the right shape and `-RNAseQC` to get the actual report

3. Get you read counts

  Do you want to do differential gene expression analysis..? just flag `-count` and you will get your counts

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc)
- [featureCounts](http://subread.sourceforge.net/)

## Installation

Make sure to install [BigDataScript](http://pcingola.github.io/BigDataScript/) first. Follow [BDS installation instructions](http://pcingola.github.io/BigDataScript/download.html)

**Recomended** 

Get [latest stable release](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/releases) by 
downloading `*tar.gz` file.

1. Locate your `*tar.gz` file
2. `tar zxvf *tar.gz file` 
3. You `RNAsik-pipe` executable file is located in `src` directory
 
**If you like to get developing version**

`git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe.git`

3. Run it !

  - To align `RNAsik-pipe -star -fqRegex A -genomeIndex path/to/yourIndexDirectory` 
  - To get counts `RNAsik-pipe -count -gtfFile path/to/yourGTFfile`
  - To get RNA-SeQC report `RNAsik-pipe -prePro -fastaRef path/to/yourFASTAreference-file -RNAseQC`

You should really specify all options at the start and let `RNAsik-pipe` to take of everything else

## Quick start

- If you have a `module` system on you server/cluster make sure to module load all required tools e.g `module load STAR`

- run `RNAsik-pipe` by pointing to the executable file. e.g if you downloaded `*tar.gz` file into `Downlaods`
directory and unpacked there, then run `RNAsik-pipe` from anywhere as such `~/Downloads/RNAsik-pipe/src/RNAsik-pipe`

- Then simply add all the options you need. `RNAsik-pipe` will guide you through. `RNAsik-pipe` will let you know if you have forgotten any files needed for your run. 

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
