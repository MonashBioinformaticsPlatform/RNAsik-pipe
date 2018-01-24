
![mbp-banner](images/mbp_banner.png)

# RNAsik for RNAseq

> **N.B** This workflow assumes a reference genome and gene model exists for the experimental organism. If a reference genome isn't applicable, a different 
workflow is required.

## Introduction

[RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline was built for processing [RNA-seq(uencing)](https://rnaseq.uoregon.edu/) data.
It is written in [BigDataScript (bds)](http://pcingola.github.io/BigDataScript/download.html), which is 
[domain specific language (DSL)](https://en.wikipedia.org/wiki/Domain-specific_language), that makes writing pipelines easy as well as making them robust. 
To get a bit more technical bds runs on [java virtual machine (JVM)](https://en.wikipedia.org/wiki/Java_virtual_machine) and therefore requires 
[Java](https://www.java.com/en/). In simple terms, any pipeline is a wrapper of several tools that makes it easier and arguably faster to get to the end goal.
Moreover, parameters and logs from the tools are captured and documented by RNAsik for reproducibility.  
The three core parts to any [RNA-seq analysis](https://rnaseq.uoregon.edu/) are: 

- mapping to the reference genome
- counting reads mapped to features e.g genes
- differential expression (DE) analysis and statistics

RNAsik performss the first two parts generating a count table for entry into [Degust](degust.erc.monash.edu), the third part of RNA-seq analysis. Degust itself, 
in simple terms, a wrapper for [LIMMA](http://bioconductor.org/packages/release/bioc/html/limma.html) and 
[edgeR](http://bioconductor.org/packages/release/bioc/html/edgeR.html) R packages. In theory and practice one can take output from 
[RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) pipeline, which is a table of counts where every gene is a row and every column is a sample 
and use those for other R packages to do your own DE analysis.

In actual terms both [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) and [Degust](degust.erc.monash.edu) provide much more than just those 
few simple steps and both tools are very powerful for RNA-seq analysis. [Degust](degust.erc.monash.edu) is exceptionally good for exploratory data visualisation 
and analysis. Both tools can also serve as a nice proxy for learning bioinformatics as they provide the command line and R code for each step of the core of RNA-seq
analysis.

## RNAsik pipeline

As mentioned above very first step in [RNA-seq analysis](https://rnaseq.uoregon.edu/) is to map your raw reads ([FASTQ](https://en.wikipedia.org/wiki/FASTQ_format)) 
to the reference genome followed by counting of reads that map onto a feature. But there is always more you could do with your data, in fact almost always only by 
doing more you can get deeper insight into your biological experiment and the system you are studying. And so 
[RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) uses these tools to get as much out of your data as possible in a timely manner that is 
streamlined into one simple command line script RNAsik uses as defaults:

- [STAR aligner for mapping](https://github.com/alexdobin/STAR/releases)
- [featureCounts from subread package for read counting](http://subread.sourceforge.net/)
- [samtools for coverage calculation and general bam files filtering](http://www.htslib.org/download/)
- [picard tools also for general bam fiels filtering](http://broadinstitute.github.io/picard/)
- [QualiMap for intragenic and interegenic rates](http://qualimap.bioinfo.cipf.es/)
- [FastQC for QC metrics on yor fastq files](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [MultiQC for wraping everying into nice, single page report](http://multiqc.info/) 

As one can imagine every one of those tools has several number of options and by running [RNAsik-pipeline](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) 
with default parameters (best practice), you get one  result. Obviously it all comes from years of experience and continues development and improvement. Use can always 
parse your own options using the `-extraOptions` flag for more fine turning. 
Alternatively as, hinted above, you can leverage off [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) to run everything separately with fine control
over the individual run. [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) produces an [.html report](https://en.wikipedia.org/wiki/HTML) with 
all commands options specified.

## Quality metrics 

[MultiQC](http://multiqc.info/) is an aggregate tool that pulls different quality metrics from each tool into one place -the  multiqc report. This is a good place to 
start understanding your data and guage a sense of how well your sequencing experiment went. From the multiqc report, it is possible to determine:

- Sample Library preparation performance, Are there differences in library insert sizes?
- Sample Library pooling performance and sequencing performance, Are there differences in total read yields from your libraries?
- Sequence alignemnt and mapping performance. Are there any issues with mapping rates?
- Read assignement to feature and sample library preparation performance. Are there any issues with reads assignment rates?

However there is so many other questions you can ask including:

- What is read duplication rate?
- What is read multi-mapping rate?
- What is intragenic and interagenic rates?

As mentioned above [multiqc](http://multiqc.info) report is a great first step in the attempt to answer those questions. A lot of the time everything looks fairly good 
and consistent allowing downstream analysis. It is a very important sanity check to make before going onto tertiary analysis such as differential expression.  Sometimes 
users can tweak certain individual parameters which can improve these QC results, other times it comes down to experimental design and/or library preparation and 
sequencing issues. It is from these plots the user can infer if something went wrong with the experiment, what could have gone wrong.  Either way, this "first iteration" 
of data analysis in important before moving on. 

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
