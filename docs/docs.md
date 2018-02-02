
![mbp-banner](images/mbp_banner.png)

# Documentation

## Quick start

### Align raw reads

```BASH
RNAsik -align star \
       -fastaRef /path/to/reference.fasta \
       -fqDir /path/to/raw-data/directory
```

### Count gene features

```BASH
RNAsik -counts \
       -gtfFile path/to/annotation.gtf
```
### The lot

```BASH
RNAsik -fqDir /path/to/raw-data/directory \
       -align star \
       -refFiles /path/to/refDir \
       -counts \
       -metrics \
       -threads 10
```

## Data set for testing

> N.B `RNAsik` pipeline is some what resource hungry. This isn't `RNAsik` fault per say, because it "simply" wraps other tools. STAR aligner required fair amount of RAM and cpus. For a large genome like mouse it required around 30 Gb of RAM and the more cpus you have the quicker you'll map. I would advise not run the pipeline with less than 4 cores, which is default. This testing data set is of yeast and requires about 14 Gb of RAM.

I figured that for testing you need smallish data set as well as species with a smalling genome, as indexing of genome takes a while for larger genome e.g mouse
I found this study [GSE103004](https://www.ncbi.nlm.nih.gov//geo/query/acc.cgi?acc=GSE103004) which looks like an open access. If you follow [that link](https://www.ncbi.nlm.nih.gov//geo/query/acc.cgi?acc=GSE103004) you should hit front GEO page for that study. You can find your way to actual data (SRA files) files, but I always find it's a bit convoluted, so hit [here is a link to data files](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP116034). 

I've already prepared raw-data (fastq) files for you. I also reduced number of samples and sub-sampled reads to speed up your test run. Firstly though let me explain to you how to get full data set.

- [download sratoolkit](https://www.ncbi.nlm.nih.gov/sra/docs/toolkitsoft/) which is set of tools from [NCBI](https://www.ncbi.nlm.nih.gov/) that you'll need to download [sra files](https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/) and then extract/convert those to fastq files.

- `fastq-dump --gzip --split-files SRR3407195` this is a command that you'll want to run to get one particular sra file, not `--split-files` options, you need to use that if you data is paired end. If you don't use that flag, then you are going to end up with a single fastq file that has reads interleaved or truncated/merged in a funny way (had some issues like that in the past)

However you don't want run that command several times, so use a loop

```
while read s; do fastq-dump --gzip --split-files $s > $s.log 2>&1 &done < SRR_Acc_List.txt
```

You can download [SRR_Acc_List.txt file at this page](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP116034) (mentioned that page before). That list has 9 sra files corresponding to 9 samples, where each samples was paired end and therefore total number of files is double - 18. 

Also note that default marking when extracting from sra for R1 and R2 is `_1` and `_2` respectively and so if you are running `RNAsik` on that full data set you'll need to pass `-pairIds "_1,_2"` flag, default is `-pairIds "_R1,_R2"` 

If you want nicely labeled bam and then counts you can pass `-samplesSheet samplesSheet.txt`. I haven't implemented url based samples sheets, so you'll need to download one before hand from [here](http://bioinformatics.erc.monash.edu/home/kirill/sikTestData/samplesSheet.txt). I'll include handling of url based samples sheets into roadmap, so watch that space !

### Try it out

```BASH
RNAsik -align star \
       -fastaRef ftp://ftp.ensembl.org/pub/release-91/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna_sm.toplevel.fa.gz \
       -fqDir http://bioinformatics.erc.monash.edu/home/kirill/sikTestData/rawData/IndustrialAntifoamAgentsYeastRNAseqData.tar \
       -counts \
       -gtfFile ftp://ftp.ensembl.org/pub/release-91/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.91.gtf.gz \
       -metrics \
       -threads 10
```

## Introduction

As mentioned previously in [about section](index.md#about) very first step in [RNA-seq analysis](https://rnaseq.uoregon.edu/) is to map your raw reads ([FASTQ](https://en.wikipedia.org/wiki/FASTQ_format)) to the reference genome following by counting of reads that map onto a feature. But there is always more you could do with your data, in fact almost always only by doing more you can get deeper inside into your biological experiment and the system you are studying. And so [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) uses these tools to get as much out of your data as possible in an streamline run:

- [STAR aligner for mapping](https://github.com/alexdobin/STAR/releases)
- [featureCounts from subread package for read counting](http://subread.sourceforge.net/)
- [samtools for coverage calculation and general bam files filtering](http://www.htslib.org/download/)
- [picard tools also for general bam fiels filtering](http://broadinstitute.github.io/picard/)
- [QualiMap for intragenic and interegenic rates](http://qualimap.bioinfo.cipf.es/)
- [FastQC for QC metrics on yor fastq files](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)
- [MultiQC for wraping everying into nice, single page report](http://multiqc.info/) 

As one can imagine every one of those tools has several number of options and by running [RNAsik-pipeline](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) you get predefined - subjective run. Obviously it all comes from years of experience and continues development and improvement. Use can always pass his/her own options through `-extraOptions` flag for more fine turning. 
Alternatively as, hinted above, user can leverage of [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) to run everything separately with fine control over the individual run. [RNAsik](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe) produces [.html report](https://en.wikipedia.org/wiki/HTML) with all commands options specified.

## Prerequisites

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [subread](http://subread.sourceforge.net/)
- [samtools](http://www.htslib.org/download/)
- [bedtools2](http://bedtools.readthedocs.io/en/latest/index.html)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [QualiMap](http://qualimap.bioinfo.cipf.es/)
- [MultiQC](http://multiqc.info/) 
- [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

## Installation

### Preferred method

Follow [ansible installation guid](http://docs.ansible.com/ansible/intro_installation.html) to get ansible then:

```BASH
git clone https://github.com/MonashBioinformaticsPlatform/bio-ansible
cd bio-ansible/
ansible-playbook -i host bio.yml --tags bds,rnasik,star,subread,samtools,htslib,bedtools,picard,qualimap,fastqc,multiqc
```
[Need more help?](https://github.com/MonashBioinformaticsPlatform/bio-ansible)

### Alternative method

If you have all of the tools installed and you just need `RNAsik` you can simply `git clone` it. It doesn't require any
other installations/compilations. BUT you do need to have [BigDataScript](https://github.com/pcingola/BigDataScript) installed
and have it in your `PATH` for `RNAsik` to run

```BASH
git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe
path/to/RNAsik-pipe/bin/RNAsik
```

## User input

### Reference files

<table>
<tr><th class="left_col">Input File</th><th>Description</th></tr>
<tr><td class="left_col">FASTA file</td><td>Most often this is your genomic reference sequence. It is a FASTA file holding raw DNA sequences where different features e.g chromosomes are labeled uniquely with a header line starting with '>'. [FASTA Format Description](https://en.wikipedia.org/wiki/FASTA_format) </td></tr>
<tr><td class="left_col">GTF/GFF/SAF file</td><td> This is your gene annotation file (i.e coordinates of your genes, exons and other genomic features). This should be linked and associated with your genomic reference file. SAF (simple annotation format) is something that featureCounts use and it supported by the pipeline</td></tr>
</table>

### Raw data

<table>
<tr><th>Input File</th><th>Description</th></tr>
<tr><td class="left_col">FASTQ file</td><td>These are your raw files that are provided by the sequencing facility to you, they can be gzipped (.fq, .fastq, .fq.gz, .fastq.gz) </td></tr>
</table>

## User input explained

### Annotation files

Annotation file would central for differential expression (DE) analysis without one you won't be able to do one. You could have very well assembled genome with very good mapping rate, but unless you know where your genes are on that genome i.e start and end coordinates for your features e.g genes you won't be able to deduce any information about those features and therefore compare between conditions. Below is an example of bear minimum information you need for feature counting. 

```
GeneID	Chr	Start	End	Strand
497097	chr1	3204563	3207049	-
497097	chr1	3411783	3411982	-
497097	chr1	3660633	3661579	-
```

There few entities that provide genome annotation, some cover more species than other. There will be of course individuals that simply provide annotation for one particular species, perhaps for more rare model organisms.

There are also different annotation file formats out there, which makes a little hard to provide `RNAsik` support for all of them. Currently `RNAsik` can only work with `GFF`, `GTF` or `SAF` file formats. There are many compatibilities issues between formats, but more importantly certain bits of information are only found in some of the files. The example above show `SAF` file format and as you can see that includes not human redable gene names nor biotype. `GFF` also often doesn't have biotype information, but on the other hand has product tag, which has short description, for protein coding at least, of resulting protein product, `GTF` lacks that information. Because of all these little nuances it can be hard to capture all of the desirable information.

Most tools in the pipeline prefer `GTF`, some can only work with `GTF`. I guess main reason for this is that every line is self contained and the format has been fairly predictable/stable.

If for whatever reason you can't get hold of `GFF/GTF` files and your annotation comes in `GenBank` (very common for bacterial genomes) or `Bed` files, don't panic and try to parse those files into `SAF` format. There are plans to include `gb_parse.py` script that should help most people with `GenBank` files.

Irrespective of which reference file distributor and which annotation file you are going to use, it is highly recommended that both of those files come from the same distributor. Most common distributors are [Ensembl](http://www.ensembl.org/index.html), [UCSC](http://genome.ucsc.edu/) and [NCBI](ftp://ftp.ncbi.nih.gov/genomes/).

### Raw data files

Raw data is something that you should take good care of. You can regenerate all other data files, but you can't really regenerate you raw data, not unless you have lots of money and time. So be sure to back your `fastq` files up and never mess/do (i.e modify) your original fastq files. If you want to try something out, make a copy and do whatever you are doing on a copy. Also there will never be a need to unzip your fastq file. All of you fastq file should be gziped and have file extension `.fastq.gz` or `fq.gz` or something similar. 

`RNAsik` will search recursively your `-fqDir` and find all fastq files. `RNAsik` can handle nested directories as long as your data is homogeneous i.e all data belongs to the same library type single-end or paired-end. If data is paired end, `RNAsik` uses `-pairIds` value to figure out read pairs. You can check that all of your fastq files had been found by looking into `sikRun/logs/samples/fqFiles`. 

After obtaining a list of all fastq files `RNAsik` tries to be smart and attempts to group fastq files into samples, that is R1 and R2 reads are grouped, but also any fastq files that had been split across lanes should also be grouped. You should end up, after the run, with the same number of bam files as you have samples. Again you can check grouping in `sikRun/logs/samples/fqMap`

`RNAsik` fastq grouping works in two modes:

- smart guessing it is a little involved but essentially it uses regular expression to check if fastq files have common suffix and therefore belong to the same sample. It heavily relies on clear labeling of R1 and R2 reads for paired-end data. 
- a more straight forward mode is simply to use samples sheet file, which is any text file with two columns separated by a tab character, `old_prefix\tnew_prefix`. Prefix in this case is your sample name, unique bit of the file. 

Samples sheet in a bit more details; If you have four samples, two wild-type and two controls, you should have four bam files after the analysis. However you number of fastq files is rather variable, depending on your sequencing. For paired-end sequencing you are going to end up with 2 fastq files per sample and 8 fastq files all up. If your sequencing was also split across lanes, say two lanes, then you are going to have 4 fastq file per each samples and 16 fastq files in total. `RNAsik` tries to simplify this for you.

## RNAsik output

### Directories breakdown

<table>
<tr><th>Directories</th><th>Description</th></tr>
<tr><td class="left_col">refFiles/</td><td> Contains the reference files (FASTA and GTF) and indices (aligner index) used in the analysis run </td></tr>
<tr><td class="left_col">bamFiles/</td><td> Contains "raw" BAM files, outputed from an aligner. Also may hold additional files from alignment run e.g aligner specific log files </td></tr>
<tr><td class="left_col">countFiles/</td><td> Contains read count files, "raw" - from `featureCounts`, degust ready counts and filtered for protein_coding features only</td></tr>
<tr><td class="left_col">markedBams/</td><td> Contains pre-processed BAM files, these BAMs are sorted, reordered and duplicates marked as well as indexed, all using picard tools. These BAMs can be used in [IGV](http://software.broadinstitute.org/software/igv/) to view read alignments </td></tr>
<tr><td class="left_col">fastqReport/</td><td> Contains FastQC HTML reports for individual FASTQ files</td></tr>
<tr><td class="left_col">qualiMapResults/</td><td> Contains int(ra|er)genic rates from each BAM file. Each BAM has its own directory with metric files. These results generated using `QualiMap rnaseq` command</td></tr>
<tr><td class="left_col">fastqDir/</td><td> If you are going to pull your FASTQ file over http in tarball, then tarball will be unarchived here</td></tr>
<tr><td class="left_col">multiqc_data/</td><td>Directory created by MultiQC holding a parsed text file, it doesn't serve any purpose for html file</td></tr>
<tr><td class="left_col">logs/</td><td>Directory that holds subdirectories, self explanatory, with logs files</td></tr>
</table>

### Files breakdown

<table>
<tr><th>Files</th><th>Description</th></tr>
<tr><td class="left_col">geneIds.txt</td><td> Hold four additional columns that get added into read counts file, that has postfix "-withNames. Gene.id, Chrom, Gene.Name, Biotype.</td></tr>
<tr><td class="left_col">strandInfo.txt</td><td> Contains guesses, based on `featureCounts` `.summary` files, strand informataion</td></tr>
<tr><td class="left_col">multiqc_report.html</td><td>This is the report file produced by MultiQC tool. A stand alone html file and can be viewed in any browser</td></tr>
</table>

## RNAsik output explained

> I hope that the directories and files naming is some what self explanatory, but here is a bit more detailed explanation of those.

### Bam files

First thing you most certainly going to get out of the pipeline is your bam files, those will be placed into `bamFiles/` directory. I don't really understand why, but `featureCounts` works best (fastest) with name sorted BAM files a.k.a unsorted. There is really two types of sorting, sorted by coordinates, often preferred as you can index those bam files and then have quick access to random parts of the file, second type is sorted by name, which insures that in paired-end experiment R1 and R2 pairs are interleaved, one after another, but you can't index those). `STAR` aligner can output either of those files. I'm however outputting "unsorted" bam file and then in the second step sorting it with `picard SamSort` tool. There are a couple of reasons for that:

- other aligners don't sort e.g bwa and therefore assuming sorted bam file won't work well
- even though `STAR` is pretty amazing (honestly), but I still rather prefer one tool for one job,
hence why I also don't count reads with `STAR`

The bam files from `bamFiles/` are only used with `featureCounts` and then `picard` suite converts them into sorted and marked duplicate bam files, which are now placed into `mdupsFiles/` directory. The rest of the analysis based on these bam files. I'm still deciding what to do with "raw" bam files in `bamFiles/` directory. They should be removed after run have finished, but if you have to re-run the pipeline to get additional things (which you can, it will resolve all dependencies and only run new tasks) those bams are now gone and will get regenerated, which will trigger the rest of pipeline to re-run, which is unwanted result. This is why I'm not auto-removing those bam files, rather doing manually after I'm sure.  

### Count files

Probably the second most important thing in the pipeline is getting read counts. That is given some genome annotation count how many of mapped reads actually ended up mapping into know annotation. For classical differential expression analysis we are interested in protein coding genes only, which pipeline attempts to filter for, but there are other biotypes that we can differentially compare.

The pipeline attempts to guess the strand (directionality) of your library. In theory sequencing provider that had made your libraries should be able to tell you that, but sometimes they get it wrong or simply that information never reaches us (bioinformaticians) hence the guessing.

Pipelines runs `featureCounts` three times forcing reads to forward strand only, forcing to reverse strand only and allowing counting on both strand (non stranded library). `featureCounts` is very nice and it provides summary table that has number of assigned to feature reads. One can simply compare forward and reverse stranded counts and deduce the strand of the library. In essence this formula is used `forward-reverse/forward+reverse` to obtain the ration, if ration is about 0.9 then library is stranded and sign indicates the strand type, if however ration is about 0.1 then library is non stranded, anything else will indication undetermined and `strandInfo.txt` file with default to `NonStranded,1` note the number one after the comment indicating status code, meaning exit with error. If you see that in your `strandInfo.txt` file you'll need to manually inspect your `*.summary` files from `featureCounts` and make decision about which library type to go with. Actual implementation of strand guessing can be found in this script `scripts/strand_guessing.py`.

`featureCounts` by default for any given run outputs two files, counts (e.g `NonStrandedCounts.txt`) and summary (e.g `NonStrandedCounts.txt.summary`). `RNAsik` attempts to "clean up" counts file, which includes removing and addition of certain columns to make counts files more informative. The columns that are added can be found in `geneIds.txt`. If for what ever reason your `geneIds.txt` is empty then all the other files with postfix `-withNames` going to be empty too. You could try to regenerate `geneIds.txt` file using `scripts/get_gene_ids.py` script and then `scripts/mk_counts_file.py` to obtain "clean" table of counts. Doing so isn't strictly needed however additional information such as human understandable gene name and biotypy often come very handy in understanding differential expression. Having a biotype in counts file also allows you to filter for specific biotype e.g `protein_coding` or `snRNA` provided your annotation file has that information.

## Command line options

### Read alignment

<table>
<tr><th>Options</th><th>Usage</th></tr>
<tr><td class="left_col">-align</td><td>specify your aligner of choice [star|starWithAnn|hisat|bwa]</td></tr>
<tr><td class="left_col">-fqDir</td><td>specify path to your raw data directory. `RNAsik` will search that path recursively, so don't worry about nested directores</td></tr>
<tr><td class="left_col">-fastaRef</td><td>specify path to your reference FASTA file, i.e file that holds your refrence genome</td></tr>
<tr><td class="left_col">-paired</td><td>specify if data is paired end (RNASik looks for R1 and R2 in the FASTQ filename representing Read 1 and Read 2 </td></tr>
</table>

### Read counting

<table>
<tr><th>Options</th><th> Usage </th></tr>
<tr><td class="left_col">-counts</td> <td> flag if you'd like to get read counts</td></tr>
<tr><td class="left_col">-gtfFile</td> <td> specify path to your reference annotation file [GTF|GFF|SAF]</td></tr>
</table>

### Reads metrics

<table>
<tr><th>Options</th><th> Usage </th></tr>
<tr><td class="left_col">-metrics</td> <td> This is an aggregate flag that is a short hand of writing out -prePro, -fastqc, -exonicRate and -multiqc</td></tr>
<tr><td class="left_col">-fastqc</td> <td> flag if you'd like to get FastQC reports for your fastq files</td></tr>
<tr><td class="left_col">-exonicRate</td> <td> flag if you'd like to get Int(ra|er)genic rates for your reads, using QualiMap tool</td></tr>
<tr><td class="left_col">-multiqc</td> <td> flag if you'd like to get general report that summarises different log files including `STAR`, `featureCounts`, `FastQC` and `QualiMap`</td></tr>
</table>

### Extra options

<table>
<tr><th>Options</th><th> Usage </th></tr>
<tr><td class="left_col">-prePro</td> <td> flag to get your BAM files pre-processed i.e get them sorted, duplicates marked and index</td></tr>
<tr><td class="left_col">-samplesSheet</td> <td> specify name of a tab separated text file, two columns,the first with old prefixes to be removed by new prefixes in the second column</td></tr>
<tr><td class="left_col">-genomeIdx</td> <td> specify path to pre-existing alignment index </td></tr>
<tr><td class="left_col">-outDir</td><td>give a name to your analysis output directory [sikRun] </td></tr>
<tr><td class="left_col">-extn</td> <td> provide your fastq files extntion. [".fastq.gz"]  </td></tr>
<tr><td class="left_col">-pairIds</td> <td> provide type identification, default is [`_R1,_R2`]</td></tr>
<tr><td class="left_col">-threads</td> <td> provide number of threads to use. [4]  </td></tr>
<tr><td class="left_col">-memory</td> <td> provide amount of memory to use. [40000000000]  </td></tr>
<tr><td class="left_col">-extraOpts</td> <td> provide key=value pairs, one per line, with key being tool name and value is a string of options e.g `star="--outWigType bedGraph"` </td></tr>
<tr><td class="left_col">-configFile</td><td>specify your own config file with key=value pairs, one per line, for all tools</td></tr>
</table>

### Unusual user case

<table>
<tr><td class="left_col">-bamsDir</td> <td> specify path to BAMs directory. Use if bams were generated outside of the pipeline </td></tr>
</table>


<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
