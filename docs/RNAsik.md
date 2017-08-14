# RNAsik for RNAseq

> **N.B** This workflow assumes model organism has a reference genome. If the reference genome isn't applicable, different workflow is required.

## Introduction

[RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline was build in house for processing [RNA-seq(uencing)](https://rnaseq.uoregon.edu/) data.
It is written in [BigDataScript (bds)](http://pcingola.github.io/BigDataScript/download.html), which is [domain specific language (DSL)](https://en.wikipedia.org/wiki/Domain-specific_language), that makes writing pipelines easy as well as making them robust. To get a bit more technical bds runs on [java virtual machine (JVM)](https://en.wikipedia.org/wiki/Java_virtual_machine) and therefore requires [Java](https://www.java.com/en/). In simple terms any pipeline is a wrapper of several tools that makes it easier and arguably faster to get to the end goal. The three core parts to any [RNA-seq analysis](https://rnaseq.uoregon.edu/) are: 

- mapping to the reference genome
- counting reads mapped into features e.g genes
- doing differential expression (DE) statistics

The pipeline does the first two parts and [Degust](degust.erc.monash.edu) does the third part. Degust itself, in simple terms, a wrapper around [limma](http://bioconductor.org/packages/release/bioc/html/limma.html) and [edgeR](http://bioconductor.org/packages/release/bioc/html/edgeR.html) R packages. In theory and practice one can take output from [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline, which is a table of counts where every gene is a row and every column is a sample and use those or other R packages to do your own DE analysis.

In actual terms both [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) and [Degust](degust.erc.monash.edu) provide much more than just those few simple steps and both tools are very powerful for RNA-seq analysis. [Degust](degust.erc.monash.edu) is exceptionally good for exploratory data visualisation and analysis. Both tools can also server as a nice proxy for learning bioinformatics as they provide command line and R code for doing the analysis.

## RNAsik pipeline

As mentioned above very first step in [RNA-seq analysis](https://rnaseq.uoregon.edu/) is to map your raw reads ([FASTQ](https://en.wikipedia.org/wiki/FASTQ_format)) to the reference genome following by counting of reads that map onto a feature. But there is always more you could do with your data, in fact almost always only by doing more you can get deeper inside into your biological experiment and the system you are studying. And so [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) uses these tools to get as much out of your data as possible in an streamline run:

- [STAR aligner for mapping](https://github.com/alexdobin/STAR/releases)
- [featureCounts from subread package for read counting](http://subread.sourceforge.net/)
- [samtools for coverage calculation and general bam files filtering](http://www.htslib.org/download/)
- [picard tools also for general bam fiels filtering](http://broadinstitute.github.io/picard/)
- [QualiMap for intragenic and interegenic rates](http://qualimap.bioinfo.cipf.es/)
- [FastQC for QC metrics on yor fastq files](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [MultiQC for wraping everying into nice, single page report](http://multiqc.info/) 

As one can imagine every one of those tools has several number of options and by running [RNAsik-pipeline](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) you get predefined - subjective run. Obviously it all comes from years of experience and continues development and improvement. Use can always pass his/her own options through `-extraOptions` flag for more fine turning. 
Alternatively as, hinted above, user can leverage of [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) to run everything separately with fine control over the individual run. [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) produces [.html report](https://en.wikipedia.org/wiki/HTML) with all commands options specified.

## Quality metrics 

[MultiQC](http://multiqc.info/) is an aggregate tool that pulls different metrics into one place - multiqc report. This is a good place to start understanding your data. The central bits of information are:

- Are there differences in library sizes?
- Is there any issues with mapping rates?
- Is there any issues with reads assignment rates?

However there is so many other questions you can ask including:

- What is duplication rate?
- What is multi-mapping rate?
- What is intragenic and interagenic rates?

As mentioned above [multiqc](http://multiqc.info) report is a great first step in the attempt to answer those questions. A lot of the time everything looks fairly good and consistent allowing downstream analysis. Sometimes user can tweak certain individual parameters which can improve results, other times it comes down to experimental design and/or library preparation and sequencing issues. Either way one need to make this "first iteration" in order to see room for improvement. 
