
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

<p>Raw fastq files have been analysed with RNAsik pipeline <span class="citation">(Tsyganov et al. 2018)</span> to produce raw genes count matrix and various quality control metrics. For this analysis RNAsik pipeline <span class="citation">(Tsyganov et al. 2018)</span> ran with STAR aligner option <span class="citation">(Dobin et al. 2013)</span> and reads were quantified with featureCounts <span class="citation">(Liao, Smyth, and Shi 2014)</span>. The reference GTF and FASTA files were downloaded from <a href="https://ensembl.org">Ensembl database</a>. Raw counts were then analysed with Degust <span class="citation">(Powell 2015)</span> web tool to do differential expression analysis to produce list of differentially expressed genes and several quality plots including classical multidimensional scaling (MDS) and MA plots. In this analysis limma voom <span class="citation">(Law et al. 2014)</span> was used for differential expression analysis. Degust <span class="citation">(Powell 2015)</span> largely follows limma voom workflow with typical conts per million (CPM) library size normalisation and trimmed mean of M values (TMM) normalisation <span class="citation">(Robinson and Oshlack 2010)</span> for RNA composition normalisation.</p>
<h2 id="references" class="unnumbered">References</h2>
<div id="refs" class="references">
<div id="ref-Dobin2013-yw">
<p>Dobin, Alexander, Carrie A Davis, Felix Schlesinger, Jorg Drenkow, Chris Zaleski, Sonali Jha, Philippe Batut, Mark Chaisson, and Thomas R Gingeras. 2013. “STAR: Ultrafast Universal RNA-seq Aligner.” <em>Bioinformatics</em> 29 (1): 15–21. <a href="http://dx.doi.org/10.1093/bioinformatics/bts635" class="uri">http://dx.doi.org/10.1093/bioinformatics/bts635</a>.</p>
</div>
<div id="ref-Law2014-ev">
<p>Law, Charity W, Yunshun Chen, Wei Shi, and Gordon K Smyth. 2014. “Voom: Precision Weights Unlock Linear Model Analysis Tools for RNA-seq Read Counts.” <em>Genome Biol.</em> 15 (2): R29. <a href="http://dx.doi.org/10.1186/gb-2014-15-2-r29" class="uri">http://dx.doi.org/10.1186/gb-2014-15-2-r29</a>.</p>
</div>
<div id="ref-Liao2014-qo">
<p>Liao, Yang, Gordon K Smyth, and Wei Shi. 2014. “FeatureCounts: An Efficient General Purpose Program for Assigning Sequence Reads to Genomic Features.” <em>Bioinformatics</em> 30 (7): 923–30. <a href="http://dx.doi.org/10.1093/bioinformatics/btt656" class="uri">http://dx.doi.org/10.1093/bioinformatics/btt656</a>.</p>
</div>
<div id="ref-Powell2015">
<p>Powell, David. 2015. “Degust: Powerfull and User Friendly Front-End Data Analsysis, Visualisation and Exploratory Tool for Rna-Sequencing.” github. <a href="http://degust.erc.monash.edu" class="uri">http://degust.erc.monash.edu</a>.</p>
</div>
<div id="ref-Robinson2010-yu">
<p>Robinson, Mark D, and Alicia Oshlack. 2010. “A Scaling Normalization Method for Differential Expression Analysis of RNA-seq Data.” <em>Genome Biol.</em> 11 (3): R25. <a href="http://dx.doi.org/10.1186/gb-2010-11-3-r25" class="uri">http://dx.doi.org/10.1186/gb-2010-11-3-r25</a>.</p>
</div>
<div id="ref-Tsyganov2018-si">
<p>Tsyganov, Kirill, Andrew James Perry, Stuart Kenneth Archer, and David Powell. 2018. “RNAsik: A Pipeline for Complete and Reproducible RNA-seq Analysis That Runs Anywhere with Speed and Ease.” <em>Journal of Open Source Software</em> 3: 583. <a href="https://www.theoj.org/joss-papers/joss.00583/10.21105.joss.00583.pdf" class="uri">https://www.theoj.org/joss-papers/joss.00583/10.21105.joss.00583.pdf</a>.</p>
</div>
</div>

## MBP team photo

![team_photo_2017](images/team_photo_2017.jpg)

## Getting help

Please submit all of you questions, comments and any other issues to [GitHub issues](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/issues)

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
