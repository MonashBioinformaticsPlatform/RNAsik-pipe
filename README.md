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
- [Installation](#installation)
- [User manual](supplementary/docs.md)
- [Release notes](#release-notes)

## Quick start

If you have a `module` system on you server/cluster make sure to `module load` all required tools e.g `module load STAR`
**Need to have [all of these tools](#prerequisites) in your enviroment**. Alternatively use [ansible RNAsik-playbook](https://github.com/serine/sik_ansible) to install everything for you and `module load RNAsik-pipe` which will automatically load all the dependencies.

Use `RNAsik-pipe` executable file to run it e.g `./RNAsik`. Everything else will depend on what you want to do, some examples below

### RNAsik-pipe commands examples

- To align FASTQ files in `raw-data/data-a` directory use 

```BASH
RNAsik -align star \
       -fastaRef /path/to/reference.fasta \
       -fqDir /path/to/raw-data/directory
```

** RNAsik will search `-fqDir` recursively ! **

- To just get counts on pre-existing BAM files your can either put BAM files into `bamFiles` directory pass then in using `-bamFiles /path/to/BAMfiles/directory`

```BASH
RNAsik -count \
       -gtfFile path/to/your/annotation/file \
```

- Here is full run

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

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [subread](http://subread.sourceforge.net/)
- [samtools](http://www.htslib.org/download/)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [QualiMap](http://qualimap.bioinfo.cipf.es/)
- [MultiQC](http://multiqc.info/) 
- [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

### System requirements 

- At least 100 Gb of disk space. For [STAR aligner](https://github.com/alexdobin/STAR/releases) you will need 100 Gb of disk space during making an index step. The index itself isn't 100 Gb, but that much space is required. 
- At least 32 Gb of RAM for read alignments

## Installation

#### The easy way:

```BASH
git clone https://github.com/serine/bio-ansible --branch from-scratch
cd bio-ansible/
ansible-playbook -i host bio.yml --tags bds,rnasik,star,subread,samtools,htslib,picard,qualimap,fastqc
```
#### The other way:

- Install [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- Install [latest stable RNAsik-pipe release](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/releases)

    1. Locate your `*tar.gz` file
    2. `tar zxvf *tar.gz file` 
    3. You `RNAsik` executable file is located in `src` directory

- Install all [dependencies](#prerequisites)
 
#### Latest unstable version:
## Release notes

- [Version 1.2](supplementary/releaseNotes1.2.md)
- [Version 1.3](supplementary/releaseNotes1.3.md)
