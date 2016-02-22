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

```
#------------------------
RNAsik-pipe version 1.3
#------------------------
#----------------------------
Usage: RNAsik-pipe [options]
#----------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Example_1: RNAsik-pipe -makeIndex -fastaRef /path/to/your/referenceFile.fa
Example_2: RNAsik-pipe -makeIndex -fastaRef /path/to/your/referenceFile.fa -align star -fqDir /path/to/your/fastqFiles/directory -fqRegex A
Example_3: RNAsik-pipe -align star -fqDir /path/to/your/fastqFiles/directory -fqRegex A -fastaRef /path/to/your/referenceFile.fa 
Example_4: RNAsik-pipe -count -gtfFile path/to/your/GTF/file
Example_5: RNAsik-pipe -align star -fqDir /path/to/your/fastqFiles/directory -fqRegex A -fastaRef /path/to/your/referenceFile.fa -count -gtfFile path/to/your/GTF/file
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Make Indices options [default STAR]:
	-makeIndex <bool>       : Flag if you need to make STAR index. You must indexed your reference genome in order to do the alignemnt. \
                              If `-genomeIndex` option isn't give and `-align` is specified `RNAsik-pipe` will automatically make an index.
	-fastaRef <string>      : path to the reference FASTA file
FASTQ mapping options [default STAR]:
	-align <string>         : please specify your aligner of choice for the alignment step
	-fqDir <string>         : path to the directory with FASTQ files
	-fqRegex <string>       : select regex option that resembles your common fastq file ending\
                                           A: "_L[0-9]{3}_R[0-9]_[0-9]{3}.fastq.gz$"\
                                           B: "_L[0-9]{3}_R[0-9].fastq.gz$"\
                                           C: "_R[0-9]_[0-9]{3}.fastq.gz$"\
                                           D: "_R[0-9].fastq.gz$" \
                               e.g for this file Samp12_S10_L002_R1_001.fastq.gz you'd do -fqRegex A
	-genomeIndex <string>   : path to the directory with genome index for the coresponding species. If not specified then `-makeIndex` option is assumed
Reads count option [default featureCounts]:
	-count <bool>           : flag if you like to count reads
	-gtfFile <string>       : path to the GTF file
BAM files pre  processing for RNA-SeQC report options [default picard tools]:
	-prePro <bool>          : flag if you like to preprocess your bam files \
                          if you are just processing your BAM files you will also need to specify your reference genome file \
                          use `-fastaRef` option for that
fastQC report [default FastQC]: 
	-fastqc <bool>          : flag if you like to run fastQC report on the files
RNA-SeQC report option [default RNA-SeQC]:
	-RNAseQC <bool>         : flag if you like to run RNA-SeQC report
Other options
	-threads <int>          : specify number of threads to use. This number will be used for STAR genome indexing\
                         and STAR raed alignment as well as for featureCounts, default [1]
	-extn <string>          : optional, specify your files extension default [fastq.gz]
	-sampleNames <string>   : optional, specify a text file with alternative sample names
	-extraOptions <string>  : You can add extra option to any of the tools used in the pipeline. Use this syntax \
                   e.g -extraOptions "STAR > --outSAMtype BAM Unsorted, --outReadsUnmapped Fastx; starIndex > --sjdbGTFfile /path/to/GTF/file, --sjdbOverhang 99; featureCounts > -t gene" \
                          Each command is separated by semi-colon (;) after the last options. \
                          The command options and command name are separated by grater than sign (>) \
```

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

**You can simply specify all of the options at the start and let `RNAsik-pipe` to do everything for your and it will guide you through. `RNAsik-pipe` will let you know if you have forgotten any files needed for your run**

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
- [python](https://www.python.org/downloads/) usually pre-installed on most Linux distributions
- [gffutils](https://pypi.python.org/pypi/gffutils) python package, can use `(sudo) pip install gffutils`
- [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc)

### System requirements 

- At least 100 Gb of disk space. [STAR aligner](https://github.com/alexdobin/STAR/releases) you will need 100 Gb of disk space during making an index step. The index itself isn't 100 Gb, but that much space is required. 
- At least 32 Gb of RAM

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
