---
title: 'RNAsik: Pipeline for complete RNA-seq analysis with speed and ease'
tags:
- RNA-seq
- gene expression
- pipeline
- bioinformatics
authors:
- name: Kirill Tsyganov
  orcid: 
  affiliation: 1
- name: Andrew Perry
  orcid: 
  affiliation: 1
- name: Stuart Archer
  orcid: 
  affiliation: 1
- name: David Powell
  orcid: 
  affiliation: 1
affiliations:
- name: 'Monash Bioinformatics Platform, Monash University'
  index: 1
date: 6 February 2018
bibliography: paper.bib
---

# Summary

RNA-sequencing (RNA-seq) is one of the applications of next-generation sequencing (NGS) method. Illumina based NGS can produce millions of short reads, around 100 bases long, and currently no longer than 300 bases. RNA-seq can help answer number of different biological questions, but most commonly it is used for measuring differential gene expression (DGE). RNAsik pipeline in single run gives your everything you need to know about your RNA-seq experiment and sets you up for DGE calling.
In alignment based approach, three main steps are; alignment of fastq files to the reference genome, counting number of reads mapped to the features (genes) and calling DEG. Degust [@Powell2015] is the best suited for calling DEG and nicely coupled with RNAsik output - table of counts. Degust is powerful front-end and user friendly tool for DGE data analysis, visualisation and exploration. However RNAsik table of counts can be used with any other DEG tools/packages that take table of counts as input, which is most common approach.
Additionally RNAsik includes number of different quality control (QC) metrics; fastqc reports using FastQC [@Bioinformatics2011-ve], int(ra|er)genic rates estimation using QualiMap [@Okonechnikov2016-jk] library size and GC bias estimation using picard tools [@picard-tools2018] and all of that summarised in a single html report, thanks to MulitQC [@Ewels2016-ik]. Other nice features to note; RNAsik improves table of counts with addition of extra meta information about each gene e.g biotype and human readable gene names, it provides ready to use coverage plots for every sample using bedtools2 [@Quinlan2010-am] and UCSC binaries [@Raney2014-ti],and RNAsik uses internal logger to log every step in the pipeline including number of samples and associated fastq files, tooling versions and sequencing strand information. 
RNAsik is written in BigDataScript (BDS) [@Cingolani2015-nm], which is domain specific language (DSL). Thanks to BDS, you will get additional html report about your RNAsik run, unlike RNAsik internal logger,this report holds system information such as time break down and exit status for every tool ran.
RNAsik already includes STAR aligner [@Dobin2013-yw], featureCounts [@Liao2014-qo], samtools [@Li2009-aa] to name some of the tools. However one can extend RNAsik with other new tools and features. Recently RNAsik had been extend to include two other aligners, Hisat2 [@Kim2015-ju] and BWA-MEM [@Li2013-bz]. This is to broaden RNAsik scope to bacterial RNA-seq analysis as well as allow diversity.
RNAsik is an open-source project under Apache License 2.0, any contributions are welcomed. In the near future there are plans to extend RNAsik to alignment free reads quantification, that is using kmer counting approach as well as include RNA-seq variant calling option [@Sun2016-ud]. To say the least RNAsik simplifies and speeds up your RNA-seq analysis enabling end user to dive much deeper into your data and have more time to study it #valueformoney.
