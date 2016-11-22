# RNAsik pipeline docs

<div class="grid grid-fluid">
<div class="row">
<div class="col-2">

## Content

- [Quick start](#quick-start)
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [User input](#user-input)
- [Directories and files explained](#directories-and-files-explained)
- [Command line optioins](#command-line-options)

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>

</div>

<div class="col-10">
## Quick start

##### Align raw reads

```BASH
RNAsik -align star \
       -fastaRef /path/to/reference.fasta \
       -fqDir /path/to/raw-data/directory
```

##### Count gene features

```BASH
RNAsik -count \
       -gtfFile path/to/annotation.gtf
```
##### The lot

```BASH
RNAsik -align star \
       -fastaRef /path/to/reference.fasta \
       -fqDir /path/to/raw-data/directory \
       -count \
       -gtfFile path/to/your/annotation/file \
       -prePro \
       -fastqc \
       -multiqc \
       -exonicRate \
       -threads 15
```

## Introduction

`RNAsik` does alignment AND read counting, which makes Degust analysis one upload away AND BAM file pre-processing for IGV AND diagnostic QC metrics. `RNAsik` wraps [these tools](#prerequisites) making your RNAseq analysis more streamline. `RNAsik` has also "sanity checks" inbuilt, checking command line options, checking if options are valid files/directories and it will talk to you so don't sweat :) and read the error message.

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [subread](http://subread.sourceforge.net/)
- [samtools](http://www.htslib.org/download/)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [QualiMap](http://qualimap.bioinfo.cipf.es/)
- [MultiQC](http://multiqc.info/) 
- [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

## Installation

Follow [ansible installation guid](http://docs.ansible.com/ansible/intro_installation.html) to get ansible then:

```BASH
git clone https://github.com/serine/bio-ansible --branch from-scratch
cd bio-ansible/
ansible-playbook -i host bio.yml --tags bds,rnasik,star,subread,samtools,htslib,picard,qualimap,fastqc
```
[Need more help?](http://github.com/serine/bio-ansible)

## User input

##### Reference files

It is highly recommended that both of those files come from the same distributor. Most common distributors are [Ensembl](), [USCS]() and [NCBI]().

<table class="table table-striped">
<tr><thead> <td>Input</td><td>Explained</td></thead></tr>
<tr><td class="args">FASTA file</td><td>Most often this is your genomic reference sequence. FASTA file holds raw DNA (or amino acid) sequence where different features e.g chromosomes are labeled uniquely</td></tr>
<tr><td class="args">GTF or GFF file</td><td> This is your annotation file i.e coordinates of your genes, exons and other genomic feature</td></tr>
</table>

##### Raw data

`RNAsik` can handle nested directories as long as your data is homogeneous i.e all data belongs to the same library type e.g paired-end. 

<table class="table table-striped">
<tr><thead> <td>Input</td><td>Explained</td></thead></tr>
<tr><td class="args">FASTQ file</td><td>These are your raw files that are provided by the sequencing facilities to you </td></tr>
</table>

## Directories and files explained

##### Directories explained

<table class="table table-striped">
<tr><thead> <td>Directories</td><td>Explained</td></thead></tr>
<tr><td class="args">refFiles/</td><td> Holds several reference files (FASTA and GTF) and indices (aligner index) </td></tr>
<tr><td class="args">bamFiles/</td><td> Hold "raw" BAM files, outputed from an alinger. Also may hold additional files from alignment run e.g aligner specific log files </td></tr>
<tr><td class="args">countFiles/</td><td> Hold counts files, "raw" - from `featureCounts`, degust ready counts and filtered for protein_coding features only</td></tr>
<tr><td class="args">markedBams/</td><td> Hold pre-processed BAM files, these BAMs have beep sorted, reordered and duplicates marked as well as indexed, all using picard tools. These BAMs are [IGV reads](http://software.broadinstitute.org/software/igv/) </td></tr>
<tr><td class="args">fastqReport/</td><td> Hold HTML reports for individual FASTQ file</td></tr>
<tr><td class="args">qualiMapResults/</td><td> Hold int(ra|er)genic rates per BAM files. Each BAM has its own directory with metric files. These results generated using `QualiMap rnaseq` command</td></tr>
</table>

##### Files explained

<table class="table table-striped">
<tr><thead> <td>Files</td><td>Explained</td></thead></tr>
<tr><td class="args">logFile.txt</td><td> Keeps log of `RNAsik` events, including FASTQ to BAM mapping and file in use. It doesn't keep stdout/stderr from individual tool in use. Each tool should have its own logging implemented. Look in the corresponding directory for tool specific log files.</td></tr>
</table>

## Command line options

##### Read alignment

<table class="table table-striped">
<tr><thead> <td>Options</td><td>Usage</td></thead></tr>
<tr><td class="args">-align</td><td>specify your aligner of choice</td></tr>
<tr><td class="args">-fqDir</td><td>specify path to your raw data directory. `RNAsik` will search that path recursively, so don't worry about nested directores</td></tr>
<tr><td class="args">-fastaRef</td><td>specify path to your reference FASTA file, i.e file that holds your refrence genome</td></tr>
</table>

##### Read counting

<table class="table table-striped">
<tr> <thead> <td>Options</td><td> Usage </td></thead></tr>
<tr><td class="args">-count</td> <td> flag if you'd like to get read counts</td></tr>
<tr><td class="args">-gtfFile</td> <td> specify path to your reference annotation file (GTF or GFF)</td></tr>
</table>

##### Reads metrics

<table class="table table-striped">
<tr> <thead> <td>Options</td><td> Usage </td></thead></tr>
<tr><td class="args">-fastqc</td> <td> flag if you'd like to get FastQC reports for your fastq files</td></tr>
<tr><td class="args">-exonicRate</td> <td> flag if you'd like to get Int(ra|er)genic rates for your reads, using QualiMap tool</td></tr>
<tr><td class="args">-multiqc</td> <td> flag if you'd like to get general report that summarises different log files including `STAR`, `featureCounts`, `FastQC` and `QualiMap`</td></tr>
</table>

##### Extra options

<table class="table table-striped">
<tr> <thead> <td>Options</td><td> Usage </td></thead></tr>
<tr><td class="args">-prePro</td> <td> flag to get your BAM files pre-processed i.e get them sorted, duplicates marked and index</td></tr>
<tr><td class="args">-samplesSheet</td> <td> specify tab separated, two columns, file with old and new prefixes</td></tr>
<tr><td class="args">-fqRegex
<span class="argExtraInfo">
      - `-fqRegex A` targets files like `sample-FASTQ-file_L001_R1_001.fastq.gz` 
      - `-fqRegex B` targets files like `sample-FASTQ-file_L001_R1.fastq.gz` 
      - `-fqRegex C` targets files like `sample-FASTQ-file_R1_001.fastq.gz` 
      - `-fqRegex D` targets fiels like `sample-FASTQ-file_R1.fastq.gz`
</span>
</td> <td> specify common regex pattern to get "clean" sample names </td></tr>
<tr><td class="args">-genomeIdx</td> <td> specify path to pre-existing alignment index </td></tr>
<tr><td class="args">-outDir</td><td>give a name to your analysis directory</td></tr>
<tr><td class="args">-extn</td> <td> provide your fastq files extntion. [".fastq.gz"]  </td></tr>
<tr><td class="args">-threads</td> <td> provide number of threads to use. [4]  </td></tr>
<tr><td class="args">-extraOpts</td> <td> provide key=value pairs, one per line, with key being tool name and value is a string of options e.g `star="--outWigType bedGraph"` </td></tr>
<tr><td class="args">-configFile</td><td>specify your own config file with key=value pairs, one per line, for all tools</td></tr>
</table>

##### Unusual user case

<table class="table table-striped">
<tr><td class="args">-paired</td> <td> flag to indicate that your data is paired-end. If `-fqDir` options is given `RNAsik` will automatically detect library type </td></tr>
<tr><td class="args">-bamFiles</td> <td> specify path to BAMs directory. Use if bams were generated outside of the pipeline </td></tr>
</table>

<footer> <p><a href="http://github.com/serine">Created by Kirill Tsyganov</a></p> </footer>
<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

