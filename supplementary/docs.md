- [RNAseq workflow explained](#rnaseq-workflow-explained)
- [RNAsik-pipe introduction](#rnasik-pipe-introduction)
  - [FASTQ files explained](#fastq-files-explained)
    - [Directory with FASTQ files](#directory-with-fastq-files)
    - [Directory with subdirectories with FASTQ files](#directory-with-subdirectories-with-fastq-files)
  - [Get RNAseq metrics](#get-rnaseq-metrics)
  - [get your counts](#get-your-counts)
- [Documentation](#documentation)
  - [RNAsik-pipe directory hierarchy](#rnasik-pipe-directory-hierarchy)
  - [Additional and optional files](#additional-and-optional-files)
  - [Best practice tip](#best-practice-tip)
  - [Options](#options)

## RNAseq workflow explained

Your standard [RNA-seq](https://en.wikipedia.org/wiki/RNA-Seq) workflow as follows:

1. get [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) reads
2. align them to your reference genome (your reference genome is given in [FASTA](https://en.wikipedia.org/wiki/FASTA_format) file). [STAR aligner](https://github.com/alexdobin/STAR) is used in `RNAsik-pipe` for that
3. count how many reads have mapped to the gene feature. You need [SAM/BAM files](https://samtools.github.io/hts-specs/SAMv1.pdf) for this. [featureCounts](http://subread.sourceforge.net/) is used in `RNAsik-pipe` for that
4. Then you can choose to use [limma](https://bioconductor.org/packages/release/bioc/html/limma.html) and [edgeR](https://bioconductor.org/packages/release/bioc/html/edgeR.html) in [R](https://en.wikipedia.org/wiki/R_programming_language) to do differential gene expression analysis Or you can simply upload your counts file to [Degust](http://victorian-bioinformatics-consortium.github.io/degust/), which is interactive and user friendly web tool


## RNAsik-pipe introduction

Right now `RNAsik-pipe` is a simple tools that wraps several other tools together to obstruct away the same repetitive work of retyping the same commands over the same number of tools just to get your differentially expressed genes. Simply provide `RNAsik-pipe` with [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) files directory and your reference files such as [FASTA](https://en.wikipedia.org/wiki/FASTA_format) and [GTF](http://mblab.wustl.edu/GTF22.html) and press Go !

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


## Documentation

`RNAsik-pipe` has several "sanity checks" inbuilt so that users essentially can't go wrong in using it.

Three main parts to the pipeline:

    1. Read aligning using [STAR aligner](https://github.com/alexdobin/STAR/releases) - get BAMs
    2. Read counting using [featureCounts](http://subread.sourceforge.net/) - get counts
    3. Getting RNAseq metrics report using [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc). In order to run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) your BAM files need to be preprocessed in particular way. `RNAsik-pipe` takes care of all that. In order to run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) through `RNAsik-pipe` you need to also flag `-prePro` to get your BAMs in the right shape for [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc).

You can do each part separately, for example just get BAMs or just get counts or just pre-process your BAM files or just run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc). However `RNAsik-pipe` does assume particular working directory hierarchy. 

### RNAsik-pipe directory  hierarchy

   - `bamFiles/` this directory will be created if running `RNAsik-pipe` with `-star` flag. This directory holds _unsorted_ BAM files, and output from [STAR aligner](https://github.com/alexdobin/STAR/releases). 

**If would like to mimic `bamFiles/` directory and BAM files please NOTE downstream workflow of `RNAsik-pipe` assumes `STAR` like BAM files, that is each BAM file ends with `\_Aligned.out.bam`**

   - `refFile/` this directory will only be created if running `RNAsik-pipe` with `-makeIndices` flag. This directory holds all required indices files including reference genome file and one subdirectory `*-starIndex`, which is your specific genome index for [STAR aligner](https://github.com/alexdobin/STAR/releases). 

**You can reuse that `\*-starIndex` directory for other runs provided that you are aligning against the same
reference genome**

   - `featureNo/` and `featureReverse/` these two directories will only be created if running `RNAsik-pipe` with `-count` flag. Those directories holds read counts files, one read count file per each BAM file. `RNAsik-pipe` automatically does both:
       - No = read aligned to either forward or reverse strand of the reference
       - Reverse = read alined to reverse strand of the reference only

**Downstream workflow of `RNAsik-pipe` will swap `\_Aligned.out.bam` for `.txt`. It will keep the root name for all files in `featureNo/` and `featureReverse/` directories**

   - `preqcBamFiles/` directory with pre-processed BAM files. Files are pre-processed using [Picard tools](http://broadinstitute.github.io/picard/)

   - `RNAseQC-report/` this direcotry is set as an output directory for `rna-seqc` run. All of your metrics information held in it. You can simply open that directory in the web browser to see your RNAseq metrics report.

### Additional and optional files 

    - `RNAseQC-SampleIds.txt` when you run `RNAsik-pipe` with flag `-RNAseQC` this file is automatically created in your root - project directory. This is an essential file for `rna-seqc` tools. It specify all of your sample names and path those files, which must start with `preqcBamFiles/` prefix. 

    - `*.html` [BDS](http://pcingola.github.io/BigDataScript/) automatically creates HTML report for your run. You can see all setps and more about your `RNAsik-pipe` run by looking at that report.

### Best practice tip

   - Make new directory for your RNAseq analysis e.g koVSwt-MouseLiver
   - `cd koVSwt-MouseLiver` 
   - Run your `RNAsik-pipe` from within this "root" directory

### Options

   - `-makeIndices` use this flag to make all required indices files for complete `RNAsisk-pipe` run. There are two index files that are required to be in the same directory as the reference genome file and one index directory for [STAR aligner](https://github.com/alexdobin/STAR/releases).

   - `-star` use this flag to initiate [STAR](https://github.com/alexdobin/STAR/releases) run. This is a boolflag and therefore it doesn't require any arguments.

   - `-fqDir` and `-fqDirs` have been explained above in [Get your FASTQ files](#get-your-fastq-files) section. **Only use one of two options !**

   - `-fqRegex` specify one of the three possible options (A,B or C) that are inbuilt in `RNAsik-pipe`

   ![fqRegex-sample](fqRegex-sample.png)

      - `-fqRegex A` targets files alike `sample-FASTQ-file_L001_R1_001.fastq.gz` 
      - `-fqRegex B` targets files alike `sample-FASTQ-file_L001_R1.fastq.gz` 
      - `-fqRegex C` targets files alike `sample-FASTQ-file_R1_001.fastq.gz` 

Use can also provide anyother possible unique options using [regex](https://en.wikipedia.org/wiki/Regular_expression), make sure to use `$` at the end of your [regex](https://en.wikipedia.org/wiki/Regular_expression) to indicate the direction i.e from the right to the left of the string. 
