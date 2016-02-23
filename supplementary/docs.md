# RNAsik-pipe in details

- [RNAsik-pipe introduction](#rnasik-pipe-introduction)
- [RNAsik-pipe directory hierarchy](#rnasik-pipe-directory-hierarchy)
- [RNAsik-pipe options explained](#rnasik-pipe-options-explained)
- [FASTQ files explained](#fastq-files-explained)

## RNAsik-pipe introduction

`RNAsik-pipe` wraps around several tools making it easy to get from [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) to counts files. Simply provide `RNAsik-pipe` with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files and your reference files such as [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and [GTF](http://mblab.wustl.edu/GTF22.html) and press Go ! 

It is recommended to use [GTF](http://mblab.wustl.edu/GTF22.html) as your annotation file. If you'd like to use [GFF](https://en.wikipedia.org/wiki/General_feature_format) instead you will need to use `-extraOptions` option to specify additional options to [STAR aligner](https://github.com/alexdobin/STAR/releases) and featureCounts for it to handle [GFF](https://en.wikipedia.org/wiki/General_feature_format). 

`RNAsik-pipe` assumes that all of [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files given in one directory using `fqDir` options are homogeneous data in terms of both library type and file naming. This means if your data is paired end, then no single end [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files should be located within `fqDir` directory and vice versa. `RNAsik-pipe` also assumes that your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files will have an upper case **R** following by the number 1 or 2 e.g `_R1`, `_R2`. If your data is single-end your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files still must have an `_R1` in the file name.

The best practice in running `RNAsik-pipe` is to make new directory for your RNAseq analysis e.g koVSwt-MouseLiver, `cd koVSwt-MouseLiver` and run your `RNAsik-pipe` from within this, "root", directory

`RNAsik-pipe` has "sanity checks" inbuilt, checking command line options, checking if options are valid files/directories and it will talk to you if you didn't specify the right options so don't sweat.

Three main parts to the pipeline:

  1. Read aligning using [STAR aligner](https://github.com/alexdobin/STAR/releases) - get BAMs
  2. Read counting using [featureCounts](http://subread.sourceforge.net/) - get counts
  3. Getting RNAseq metrics report using [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc).

You can do each part separately, for example just get BAMs or just get counts or just pre-process your BAM files or just run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) OR you can run all at once and `RNAsik-pipe` will figure out files dependencies.

## RNAsik-pipe directory hierarchy

### Directories explained

  - `refFile/` this directory will hold your reference files including [STAR aligner](https://github.com/alexdobin/STAR/releases) index and other indices that might be required for downstream analysis. You [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and GFT files will be copied across to this directory. You can reuse [STAR aligner](https://github.com/alexdobin/STAR/releases) index if you are aligning to the same reference genome. [STAR aligner](https://github.com/alexdobin/STAR/releases) index will be located in the directory with postfix `-starIndex`
  - `bamFiles/` this directory will be created if running `RNAsik-pipe` with `-aling` option. This directory will hold your BAM files from [STAR aligner](https://github.com/alexdobin/STAR/releases). If you already have BAM files, you can use them with other parts of the `RNAsik-pipe` except BAM files should have either `_Aligned.out.bam` or `_Aligned.sortedByCoord.out.bam` postfix as per [STAR aligner](https://github.com/alexdobin/STAR/releases) aligner output. This will make downstream file naming consistent and clean.
  - `countFiles/` directory will hold eight text files, half for non stranded feature counting and the other four for reverse strand feature counting. `featureNo.txt` and `featureReverse.txt` and its associated `.summary` files are output straight from `featureCounts`. `featureNoCounts.txt` and `featureReverseCounts.txt` is a filtered version of respective file. Filtering header and columns 2 to 5 out of those files. Finally `-withNames.txt` postfix indicates that two additional columns were added to those files with public gene names and biotype.
  - `preqcBamFiles/` directory with pre-processed BAM files. Files are pre-processed using [Picard tools](http://broadinstitute.github.io/picard/)
  - `RNAseQC-report/` this direcotry is set as an output directory for `rna-seqc` run. All of your metrics information held in it. You can simply open that directory in the web browser to see your RNAseq metrics report.
  - `fastqcReport/` will hold your `FastQC` report per each `[FASTQ](https://en.wikipedia.org/wiki/FASTQ_format)` file

### Files explained

  - `RNAseQC-SampleIds.txt` file will be created when you run `RNAsik-pipe` with option `-RNAseQC`. This is an essential file for `rna-seqc` tools. It specify all of your sample names and path those files.
  - `*.html` [BDS](http://pcingola.github.io/BigDataScript/) automatically creates HTML report for your run. You can see all setps and more about your `RNAsik-pipe` run by looking at that report.

## RNAsik-pipe options explained

#### Aligning options

   - `-makeIndex` use this option to make [STAR aligner](https://github.com/alexdobin/STAR/releases) index. This is must do step before aligning you reads to the reference genome. The indexing step, indexes your reference genome to make access to it quicker during alignment process.
   - `-align` use this option to initiate specify your aligner (at this stage only supporting [STAR aligner](https://github.com/alexdobin/STAR/releases) ). At this stage it will always be `-align star`.
   - `-fqDir` use this option to specify path to directory with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files. `fqDir` can and will look two level deep to account for both use cases explained [here](#get-your-fastq-files).
   - `-fqRegex` specify one of the four possible options (A,B,C or D) that are inbuilt in `RNAsik-pipe`

   ![fqRegex-sample](fqRegex-sample.png)

      - `-fqRegex A` targets files like `sample-FASTQ-file_L001_R1_001.fastq.gz` 
      - `-fqRegex B` targets files like `sample-FASTQ-file_L001_R1.fastq.gz` 
      - `-fqRegex C` targets files like `sample-FASTQ-file_R1_001.fastq.gz` 
      - `-fqRegex D` targets fiels like `sample-FASTQ-file_R1.fastq.gz`

  - `-genomeIndex` you can use this option to specify [STAR aligner](https://github.com/alexdobin/STAR/releases) index if you already have one made. Yon only need to specify either `-makeIndex` or `-genomeIndex` but not both!
  
#### Read counting options

  - `-count` this will initiate read counts. If specified together with `-align star` option `RNAsik-pipe` will wait for read aligning to finish i.e wait for BAM files, before processing with read counting.
  -`gtfFile` you need this file for read counting. This file specifies feature coordinates. If you just using `RNAsik-pipe` to count and not proceeding with `-RNAseQC` you can specify `.saf` file and indicate that you did so using `-exptraOptions "featureCounts > -F SAF"

#### RNAseQC report

  - `-prePro` you must pre-process you BAM files in a particular way for RNAseQC report to work, for more information refere [here](https://www.broadinstitute.org/cancer/cga/rna-seqc). This will pre-process BAM files in the right way, this is a three step process using picard tools.
  - `RNAseQC` will run `rna-seqc`

#### Other options

  - `-fastqc` will generate per [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) file report 
  - `-extn` if your [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files have different extention to `fastq.gz` you can specify alternative extention using this option
  - `-threads` to specify number of threads to use. Note that featureCounts will split number of threads in half, because two separate instances of featureCounts run in parallel. You don't have to worry about specifying an even number of threads, but bear in mind that if you do specify an odd number of threads then featureCounts will be give one less threads.
  - `-extraOptions` You can add extra option to any of the tools used in the pipeline. Use this syntax e.g `-extraOptions "STAR > --outSAMtype BAM Unsorted, --outReadsUnmapped Fastx; starIndex > --sjdbGTFfile /path/to/GTF/file, --sjdbOverhang 99; featureCounts > -t gene"`. Each command is separated by semi-colon (;) after the last options. The command options and command name are separated by grater than sign (>) 
  - `-checkPair` You can use this option to indicate if you library is paired-end. However if you are using `-fqDir` options then `RNAsik-pipe` will look into [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) directory and figure out if the data is paired-end or not. Normally you'd only use this option if you are not doing alignment, but are using other features of the pipeline e.g just running `-RNAseQC`, then you'll need to specify `-checkPair` if you library was paire-end
  - `-proBams` If you just want to run RNAseQC and you processed BAM files located in some other directory but the `preqcBamFiles/` directory then you can provide directory with processed BAM files using this option
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

**`RNAsik-pipe` can work with either of those two options.**
