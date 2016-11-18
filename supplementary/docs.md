# RNAsik-pipe in details

- [RNAsik introduction](#rnasik-pipe-introduction)
- [RNAsik directory hierarchy](#rnasik-pipe-directory-hierarchy)
- [RNAsik options explained](#rnasik-pipe-options-explained)
- [FASTQ files explained](#fastq-files-explained)

## RNAsik introduction

`RNAsik` wraps around several tools making it easy to get from [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) to counts files. Simply provide `RNAsik` with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) directory and your reference files, [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and [GTF](http://mblab.wustl.edu/GTF22.html) and press Go ! 

It is recommended to use [GTF](http://mblab.wustl.edu/GTF22.html) as your annotation file. However [GFF](https://en.wikipedia.org/wiki/General_feature_format) file should also work fine.

`RNAsik` assumes that [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files in `fqDir` directory are homogeneous i.e file naming convention. For example all FASTQs have the same file ending. This also means no library type should be mixed in the `-fqDir` e.g paired end data together with single end data is not allowed in a single run. `RNAsik` further assumes that your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files will have an upper case **R** following by the number 1 or 2 e.g `_R1`, `_R2`. If that exact feature isn't found, then `RNAsik` will run in "single end" mode and treat each FASTQ individually, which is wrong for paired end data!

At this stage `RNAsik` does not deals well with symbolic links. If you don't change the name of the file, than it is okay to use symlinks with `RNAsik`, however if symlink name is different to canonical file name, then `RNAsik` will use canonical file name instead. This may cause some unexpected results, for example if canonical filename doesn't have an **_R1** suffix and you make symlink with such suffix, assuming that `RNAsik` will work, but it will not. 

`RNAsik` has "sanity checks" inbuilt, checking command line options, checking if options are valid files/directories and it will talk to you if you didn't specify the right options so don't sweat :)

## RNAsik directory hierarchy

### Directories explained

  - `refFile/` this directory holds your reference files and several indices, including [STAR aligner](https://github.com/alexdobin/STAR/releases) index. [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and GFT files will be copied across to this directory, this need because some tools make assumption about location of index and reference files location i.e they need to be in the same directory. You can reuse [STAR aligner](https://github.com/alexdobin/STAR/releases) index if you are aligning to the same reference genome. STAR index has a postfix `-starIndex`.

  - `bamFiles/` directory holds your BAM files from [STAR aligner](https://github.com/alexdobin/STAR/releases). If you already have BAM files, you can use them with other parts of the `RNAsik`.

  - `countFiles/` directory holds output from featureCounts, which will be file for non-stranded, reverse-stranded and forward-stranded counts. `RNAsik` will then do additional steps to make those counts files [Degust](http://dna.med.monash.edu:4000/) ready.

  - `markedBams/` directory holds pre-processed BAM files i.e sorted with marked duplicates. This is useful for downstream analysis where you need sorted BAM files, e.g visualisation in [IGV](http://software.broadinstitute.org/software/igv/).

  - `fastqcReport/` directory holds your `FastQC` report per each [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) file

  - `qualiMapResults/` directory holds int(ra|er)genic information per BAM file from [QualiMap tool](http://qualimap.bioinfo.cipf.es/)

## RNAsik options explained

#### Aligning options

   - `-align` use this option to initiate specify your aligner (at this stage only supporting [STAR aligner](https://github.com/alexdobin/STAR/releases) ). At this stage it will always be `-align star`.
   - `-fqDir` use this option to specify path to directory with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files. `fqDir` can and will look two level deep to account for both use cases explained [here](#get-your-fastq-files).
   - `-fqRegex` specify one of the four possible options (A,B,C or D) that are inbuilt in `RNAsik`

   ![fqRegex-sample](fqRegex-sample.png)

      - `-fqRegex A` targets files like `sample-FASTQ-file_L001_R1_001.fastq.gz` 
      - `-fqRegex B` targets files like `sample-FASTQ-file_L001_R1.fastq.gz` 
      - `-fqRegex C` targets files like `sample-FASTQ-file_R1_001.fastq.gz` 
      - `-fqRegex D` targets fiels like `sample-FASTQ-file_R1.fastq.gz`

  - `-genomeIndex` you can use this option to specify [STAR aligner](https://github.com/alexdobin/STAR/releases) index if you already have one made. Yon only need to specify either `-makeIndex` or `-genomeIndex` but not both!
  
#### Read counting options

  - `-count` this will initiate read counts. If specified together with `-align star` option `RNAsik` will wait for read aligning to finish i.e wait for BAM files, before processing with read counting.
  - `gtfFile` you need this file for read counting. This file specifies feature coordinates.


#### Other options

  - `-prePro` you must pre-process you BAM files in a particular way for RNAseQC report to work, for more information refere [here](https://www.broadinstitute.org/cancer/cga/rna-seqc). This will pre-process BAM files in the right way, this is a three step process using picard tools.

  - `-fastqc` will generate per [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) file report 

  - `-extn` if your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files have different extention to `fastq.gz` you can specify alternative extention using this option

  - `-threads` to specify number of threads to use. Note that featureCounts will split number of threads in half, because two separate instances of featureCounts run in parallel. You don't have to worry about specifying an even number of threads, but bear in mind that if you do specify an odd number of threads then featureCounts will be give one less threads.

  - `-extraOptions` You can add extra option to any of the tools used in the pipeline. Use this syntax e.g `-extraOptions "STAR > --outSAMtype BAM Unsorted, --outReadsUnmapped Fastx; starIndex > --sjdbGTFfile /path/to/GTF/file, --sjdbOverhang 99; featureCounts > -t gene"`. Each command is separated by semi-colon (;) after the last options. The command options and command name are separated by grater than sign (>) 

  - `-paired` You can use this option to indicate if you library is paired-end. However if you are using `-fqDir` options then `RNAsik` will look into [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) directory and figure out if the data is paired-end or not. Normally you'd only use this option if you are not doing alignment, but are using other features of the pipeline e.g just running `-RNAseQC`, then you'll need to specify `-checkPair` if you library was paire-end

  - `-bamFiles` If you want to start using pipeline post read alignment and you BAM files located in other directory but the `bamFiles/` directory then you can specify directory with BAM files using this option

## FASTQ files explained

Your raw data will always come in [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) format. The number of [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files will depend on many things including:

  - Number of samples 
  - Number of replicates 
  - Your sample was split into different lanes
  - Your are sequencing paired-end data

#### Directory with FASTQ files

Your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files might reside in one directory e.g directory per experiment

![fqDir](rawDataDir.png)

In this example sample _14-09157_, which might be _WT_ sample was split across two lanes `L001` and `L002` during sequencing, this is some what typical of Illumina data. Therefore one sample is represented by two files, one for each lane. We can also see that this is paired end data, which means for each file there has to be a pair file, that is _R1_ and _R2_. In summary single sample, e.g _WT_ is covered by four [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files:

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

![test](rawDataDirs.png)

In this example each sample is placed into its own directory. Now we can see directory `Sample_14-09157`, 
which will hold four files described above.

**`RNAsik` can work with either of those two options.**
