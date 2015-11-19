- [Documentation](#documentation)
  - [RNAsik-pipe directory hierarchy](#rnasik-pipe-directory-hierarchy)
  - [Additional and optional files](#additional-and-optional-files)
  - [Best practice tip](#best-practice-tip)
  - [Options](#options)

## Documentation

RNAsik-pipe has several "sanity checks" inbuilt so that users almost always can't go wrong in using it.
There are three main parts to the pipeline:

    1. Reads aligning using [STAR aligner](https://github.com/alexdobin/STAR/releases) - get BAMs
    2. Reads counting using [featureCounts](http://subread.sourceforge.net/) - get conts
    3. Getting RNAseq metrics report using [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc). In order to run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) your BAM files need to be preprocessed in particular way. `RNAsik-pipe` takes care of all that. In order to run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc) through `RNAsik-pipe` you need to also flag `-prePro` to get your BAMs in the right shape for [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc).

You can do each part separatelly and jsut get BAMs and/or just get counts and/or just pre-process your BAM files and/or just run [RNA-SeQC](https://www.broadinstitute.org/cancer/cga/rna-seqc). However `RNAsik-pipe` does assume particular working directory hierarchy. 

### RNAsik-pipe directory  hierarchy

   - `bamFiles/` this directory will be created if running `RNAsik-pipe` with `-star` flag. This directory holds _unsorted_ BAM files, an output from [STAR aligner](https://github.com/alexdobin/STAR/releases). 

**If would like to mimic `bamFiles/` directory and BAM files please NOTE downstream workflow of `RNAsik-pipe1assumes `STAR` like BAM files, that is each BAM file ends with `\_Aligned.out.bam`**

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

   ![fqRegex-sample](supplementary/fqRegex-sample.png)

      - `-fqRegex A` targets files alike `sample-FASTQ-file_L001_R1_001.fastq.gz` 
      - `-fqRegex B` targets files alike `sample-FASTQ-file_L001_R1.fastq.gz` 
      - `-fqRegex C` targets files alike `sample-FASTQ-file_R1_001.fastq.gz` 

Use can also provide anyother possible unique options using [regex](https://en.wikipedia.org/wiki/Regular_expression), make sure to use `$` at the end of your [regex](https://en.wikipedia.org/wiki/Regular_expression) to indicate the direction i.e from the right to the left of the string. 


