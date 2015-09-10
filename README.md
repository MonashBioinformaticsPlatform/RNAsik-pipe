# `RNAsik-pipe` is easy to use RNA-seq(uencing) pipeline

### RNA-seq(uencing) a.k.a Whole-transcriptome sequencing

1. Get your FASTQ files

Your raw data will always come in FASTQ format. The number of FASTQ files will really depend many things
including:

  - Number of samples 
  - Number of replicates 
  - Your sample was split into different lanes
  - Your are sequencing paired-end data

Also your FASTQ files might reside in one directory - directory per experiment 
OR 
Each sample might be put into its own subdirectory 

Well `RNAsik-pipe` can either take your project direcoty 
### Caveats 

 - at the moment only can run `STAR` mapper with fixed options
 - right now `-fastqDir` parameter will only work with `.` i.e your execute `rnas-pipe` in the directory where
   your fastq files are
 - `prePro` is a must if you want to gete RNA-SeQC report  
 - at the moment there isn't an option to choose the strand direction for read counts
   right now `rnas-pipe` simply counts all bams against stranded NO and stranded REVERSE options

The `rnas-pipe` features:

1. Reads alignment. Currently it is set to `STAR` with predefined `STAR` input parameters
   It is rather stringent at this stage and only through manual intervention one can change the input
   parameters inside the source code. Feel free to `git clone` and edit source to your needs. 
   There are the parameters `STAR` set up to run with in BDS by default.

   ```
   STAR --runThreadN 26 \
        --genomeDir $genomeIndex \
        --outSAMtype BAM Unsorted \
        --outSAMattrRGline ID:$laneNumber CN:AGRF DS:RNA-seq PL:ILLUMINA PM:MiSeq SM:$uniqueName \
        --outSAMunmapped Within \
        --readFilesCommand zcat \
        --readFilesIn $read1 $read2 \
        --outFileNamePrefix $preFix
   ```
2. Several `picard` pre-processing steps for `RNA-SeQC` run later. `picard` produces, sorted, reordered bam files
   with marked duplicates. This is prerequisite for `RNA-SeQC` run

3. `featureCouunts` that count how many reads mapped one genes 

### Work in progress 

I'm working on including `fastqc` report at the first item to run in the pipeline
