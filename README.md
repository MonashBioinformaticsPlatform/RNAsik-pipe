# RNAsik-pipe quick and easy way to get differentially expressed genes

> Why `RNAsik-pipe` cause its sik easy. Get list of differentially expressed genes in a single command line.
> Simply give your FASTQ files to `RNAsik-pipe` with your reference files and press go ! [Enter] Go now !
>
> `RNAsik-pipe` is written in [BigDataScrip](http://pcingola.github.io/BigDataScript/) (BDS) language.
> There are many advantages in using BDS, but main ones are:
>
>  1. One script works on your local machine, on your remote server and on your cluster
>  2. Checkpoints - never need to run your job from the start in case it stopped. Start from where you left off
>  3. Remote access to your data. Don't need to worry about `scp`ing you data to the server, just point RNAsik-pipe to your cloud store if you like

## Content

- [Quick start](#quick-start)
- [Prerequisites](#prerequisites)
  - [System requirement](#system-requirement)
- [Installation](#installation)
  - [The easy way](#the-easy-way)
  - [The other way](#the-other-way)
- [User manual](#user-manual)
- [Release notes](#release-notes)
  - [Version 1.2](#version-1.2)

## Quick start

If you have a `module` system on you server/cluster make sure to `module load` all required tools e.g `module load STAR`
**Need to have [all of these tools](#prerequisites) in your enviroment**. Alternatively use [ansible RNAsik-playbook](https://github.com/serine/sik_ansible) to install everything for you and `module load RNAsik-pipe` which will automatically load all the dependencies.

Use `RNAsik-pipe` executable file to run it e.g `./RNAsik-pipe`. Everything else will depend on what you want to do, some examples below

### RNAsik-pipe commands examples

- To align FASTQ files in `raw-data/data-a` directory use 

```BASH
RNAsik-pipe -align star \
            -fqRegex A \
            -fqDir raw-data/data-a \
            -genomeIndex path/to/yourIndexDirectory
```

- To just get counts on already existing bam files you must have directory `bamFiles` with all BAM files with either `_Aligned.out.bam` or `_Aligned.sortedByCoord.out.bam` postfix as per STAR aligner output.

```BASH
RNAsik-pipe -count \
            -gtfFile path/to/your/annotation/file \
```

- To get RNA-SeQC report

```BASH
RNAsik-pipe -prePro \
            -fastaRef path/to/yourFASTAreference-file \
            -RNAseQC
```

**You can simply specify all of the options at the start and let `RNAsik-pipe` to do everything for you. `RNAsik-pipe` will guide you through, don't worry it can communicate.**

```BASH
RNAsik-pipe -align star \
            -fqRegex A \
            -fqDir raw-data/data-a \
            -genomeIndex path/to/yourIndexDirectory
            -count \
            -gtfFile path/to/your/annotation/file \
            -prePro \
            -fastaRef path/to/yourFASTAreference-file \
            -RNAseQC \
            -threads 15
```

`RNAsik-pipe` can't handle gzipped files inside `-extraOptions` flag. You have to specify any additional files exactly how the tools will want it.

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [featureCounts](http://subread.sourceforge.net/)
- [samtools](http://www.htslib.org/download/)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [gffutils](https://pypi.python.org/pypi/gffutils) python package, can use `(sudo) pip install gffutils`
- [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc)

### System requirements 

- At least 100 Gb of disk space. [STAR aligner](https://github.com/alexdobin/STAR/releases) you will need 100 Gb of disk space during making an index step. The index itself isn't 100 Gb, but that much space is required. 
- At least 32 Gb of RAM for read alignments

## Installation

### The easy way

**It is recommended that you use ansible to install RNAsik-pipe with all dependencies**

The easiest way to get `RNAsik-pipe` installed together with all dependencies is to use [ansible RNAsik-playbook](https://github.com/serine/sik_ansible)

### The other way

Make sure to install [BigDataScript](http://pcingola.github.io/BigDataScript/) first. Follow [BDS installation instructions](http://pcingola.github.io/BigDataScript/download.html)

Get [latest stable release](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/releases) by 
downloading `*tar.gz` file.

1. Locate your `*tar.gz` file
2. `tar zxvf *tar.gz file` 
3. You `RNAsik-pipe` executable file is located in `src` directory
4. Be sure to install all [dependencies](#prerequisites)
 
**If you like to get developing version**

`git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe.git`

## User manual

- [User manual](supplementary/docs.md)

## Release notes

- [Version 1.2](supplementary/releaseNotes1.2.md)
- [Version 1.3](supplementary/releaseNotes1.3.md)
