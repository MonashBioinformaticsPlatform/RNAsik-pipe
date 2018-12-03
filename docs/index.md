---
bibliography: supplementary/RNAsik.bib
---

![mbp-banner](images/mbp_banner.png)

# RNAsik for RNAseq

> **N.B** This workflow assumes model organism has a reference genome. If the reference genome isn't applicable, different workflow might be required.

## About

[RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline was build in house for processing [RNA-seq(uencing)](https://rnaseq.uoregon.edu/) data.
It is written in [BigDataScript (bds)](http://pcingola.github.io/BigDataScript/download.html), which is [domain specific language (DSL)](https://en.wikipedia.org/wiki/Domain-specific_language), that makes writing pipelines easy as well as making them robust. To get a bit more technical, bds runs on [java virtual machine (JVM)](https://en.wikipedia.org/wiki/Java_virtual_machine) and therefore requires [Java](https://www.java.com/en/).

In simple terms any pipeline is a wrapper of several tools that makes it easier and arguably faster to get to the end goal. The three core parts to any [RNA-seq analysis](https://rnaseq.uoregon.edu/) are: 

- mapping to the reference genome
- counting reads mapped into features e.g genes
- doing differential expression (DE) statistics

The pipeline does the first two parts and [Degust](http://degust.erc.monash.edu) does the third part. Degust itself, in simple terms, a wrapper around [limma](http://bioconductor.org/packages/release/bioc/html/limma.html) and [edgeR](http://bioconductor.org/packages/release/bioc/html/edgeR.html) R packages. In theory and practice one can take output from [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline, which is a table of counts where every gene is a row and every column is a sample and use those with any other R packages that do DE analysis.

In actual terms both [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) and [Degust](http://degust.erc.monash.edu) provide complete experience, not only you'll get your list of DE genes and QC metrics, but will be able to get full inside into your experimental design and the outcome of that. `RNAsik` does read alignment and read counting and cleaning and improvements of your table of counts, which makes [Degust](http://degust.erc.monash.edu) analysis one upload away. `RNAsik` wraps [these tools](docs.md#prerequisites) making your RNAseq analysis more streamline. It also has "sanity checks" inbuilt, checking command line options, checking if options are valid files/directories and it will talk to you so don't sweat :) but do read the error messages. [Degust](http://degust.erc.monash.edu) is exceptionally good for exploratory data visualisation and analysis. Both tools can also server as a nice proxy for learning bioinformatics as they provide command line and R code for doing the analysis. Last but not least thanks to [MultiQC](http://multiqc.info/) `RNAsik` provides an aggregate of different metrics in one place - multiqc report. This is a good place to start understanding your data.

The central bits of information are:

- Are there differences in library sizes?
- Is there any issues with mapping rates?
- Is there any issues with reads assignment rates?

However there is so many other questions you can ask including:

- What is duplication rate?
- What is multi-mapping rate?
- What is intragenic and interagenic rates?

As mentioned above [multiqc](http://multiqc.info) report is a great first step in the attempt to answer those questions. A lot of the time everything looks fairly good and consistent allowing downstream analysis. Sometimes user can tweak certain individual parameters which can improve results, other times it comes down to experimental design and/or library preparation and sequencing issues. Either way one need to make this "first iteration" in order to see room for improvement. 

## How to cite

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1403976.svg)](https://doi.org/10.5281/zenodo.1403976)

-----

Tsyganov, Kirill, Andrew James Perry, Stuart Kenneth Archer, and David Powell. 2018. “RNAsik: A Pipeline for Complete and Reproducible RNA-Seq Analysis That Runs Anywhere with Speed and Ease.” Journal of Open Source Software 3: 583.

-----

_It is hard to give full acknowlegment to all contributors. The nature of the open source projects such that contributors can come and go, however they leave behind valuable contributions and need to get full credit for that. Please look at [RNAsik GitHub](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) repository to get a full sense of who is contributing. In particular one can look at [number of commits](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/graphs/contributors), [issues triaging and handling](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/issues) and [pull requests (PRs)](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pulls). Please also remember that every contribution matters, nothing is too small!_

## Methods

Raw fastq files have been analysed with RNAsik pipeline [@Tsyganov2018-si] to produce raw genes count matrix and various quality control metrics. For this analysis RNAsik pipeline [@Tsyganov2018-si] ran with STAR aligner option [@Dobin2013-yw] and reads were quantified with featureCounts [@Liao2014-qo]. Raw counts were then analysed with Degust [@Powell2015] web tool to do differential expression analysis to produce list of differentially expressed genes and several quality plots including classical multidimensional scaling (MDS) and MA plots. In this analysis limma voom [@Law2014-ev] was used for differential expression analysis. Degust [@Powell2015] largely follows limma voom workflow with typical conts per million (CPM) library size normalisation and trimmed mean of M values (TMM) normalisation [@Robinson2010-yu] for RNA composition normalisation.

## MBP team photo

![team_photo_2017](images/team_photo_2017.jpg)

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
