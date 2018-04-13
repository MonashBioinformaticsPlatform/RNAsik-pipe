
![mbp-banner](images/mbp_banner.png)

# Roadmap 

## Going forward

### 1.x.x

- need to have better way to check for index directory, want to know if starIdx includes or doesn't indexing with annotation. 
- recheck [Stuart's PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10/commits/9e64da57de6da066e94bf6fcc66e23c36adb3671), polish off refFiles detection
- recheck [this whole PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10)
- Document python scripts existence, what they do, how to run them manually in the case of failure, and the output they give

### 1.5.1 Q2 (April/May) 2018

- general maintenance and bug fixes
- start including unit testing in your master branch, once I'm happy with with `unit_test` branch

### 1.5.2 Q3 (July/August) 2018

- improve `RNAsik` logging, particular want to make individual tools version logging independent of each other, so that if one wants to run
just counts, `RNAsik` shouldn't complain about `bwa` not found in the PATH. Also double check the behaviour of the logger when pipelines re-runs.
From memory it might not perform as it should. You really want a log of every event that had happened.
- include logging of split lanes and R1 and R2. Want to be able to see from the log whether two reads were classified as split lanes or paired end. This is
to do with recent bug that got fixed in [b924027](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/commit/b9240274fa7c964e953a767c254f31ba0d044547) 

### 1.5.3 Q4 (October/November) 2018

New feature(s) described below:

- implement new flag `-fqFiles` that can take either a file or a directory.
    - if a directory is given, do what `-fqDir` does now and traverse down retuning list of fastq files. 
    - if a file is given, use those locations getting fastq files. Location can be local file path or URLs, assume one location per line

Will keep `-fqDir` flag, as a backward compatibility with a warning that flag had been deprecated. Will also schedule to remove `-fqDir` completely in future releases
Because of changes in arg's options will do a minor version bump.

- include handling of url based samples sheets, i.e `-samplesSheet` flag should handle local based or remote files, just like `-fastaRef` option

### 1.6.0 Q3 (October/November) 2018

- Plans to add variants calling to `RNAsik`. It'll be opt in flag,  `-varsCall`. Suggestions are welcomed about different name for a flag.
I already have a prototype in bds, just need to plug it in.

    - Not sure which caller to use `GATK` or `freebayes` will need to do more reading on that. 
    - Also need to document common pitfalls for using RNAseq for variant calling e.g can only can variances in coding regions that are expressed. 
    - Not a good idea to use pulled samples as you won't be able to get allele frequency
    - will also need to find out where to get known SNP's (snpDB? for known germ line mutations) and a list of blacklisted regions

- [an example of someone else variant calling pipeline](https://github.com/CRG-CNAG/CalliNGS-NF)

## Ideas for future releases 

- include IGVlink into RNAsik-pipe output, can only do that if data outputted into something that is hostable i.e object store?
- Need better support for exonic/intronic rates estimation. Is `read_distribution.py` from RSeQC good idea? Right now qualiMap is ok flag to opt in.
- add alignment free support for RNAseq analysis e.g salmon/kalisto
- is there need for circular RNA support?

## Changelog

### 1.5.0

- fixed bugs and improved python scripts, also migrated them to python3
- fixed issues: #16, #15, #20, #21
- fixed bug in handling remote reference files
- added `mk_igv_links.py` script as general utility script
- added FASTQ trimmer - `skewer`
- internal code improvements, made code more readable and clean
- Re-wrote bam files processing, i.e sorting and marking duplicates. Changed sorting from `picard SortSam` to `samtools sort`. Kept `picard MarkDuplicates` for conventional marking duplicates, but add [Je-suite](https://gbcs.embl.de/portal/tiki-index.php?page=Je) for UMI based de-duplication.
- Made improvements in handling of featureCounts output for multiqc purposes.
- completely removed threads and memory parameters, now each task's gets it's own cpu and mem setting all through sik.config. This makes it more cluster friendly as well
- Added more metrics gathering; samtools qc metrics:

    - `flagstat`
    - `idxstats`
    - `stats`

- Improved many different task's dependencies flow.
- changed few command lines options; new options:

    - `-all`
    - `-counts`
    - `-mdups`
    - `-qc`
    - `-umi`
    - `-trim`

- removed command line options:

    - `-metrics`
    - `-fastqc`
    - `-prePro`
    - `-threads`
    - `-memory`

- all flags changes have some backward compatibility, i.e will set the closet new option. 

### 1.4.9

- Fixed BWA indexing problem. Problem around STAR and Hisat2 aligners pass index as directory whereas bwa as a file, had to fight to make all different options i.e `-refFiles` and `-genomeIdx` to work
- Included proper support for SAF file format handled through -gtfFile flag i.e user can pass GTF, GFF or SAF through that flag and will still get counts
- Imporved handling of urls for refrence files `-fastaRef`, `-gtfFile` now works with all bds supported url types. Also fixed tarball url handling through `-fqDir`
- Improved code readability in several places and included `canFail` flag for making degust reads counts files.
- Fixed a bug in `exonicRates` function was passing "wrong" gtf file path
- Updated docs, added more explanation on how RNAsik ticks. Included a roadmap to allow better time and features management
- fixed `-pairIds` bug, courtesy @stu2 (PR #6) and samples sheet file making
- Improved python script, including several small bug fixing

### 1.4.8

- added new feature: coverage plots generation
- added new feature: ability to pass previously generated references directory, saves spaces and time
- fixed strand guessing script, should be better at guessing now
- moved to [mkdocs](http://www.mkdocs.org/) for documents compilation and deployment to gh_pages
- added new python script to make degust file, this simplifies and strengthens the code
- improved readability of the code
- improved and fixed bugs in handling fastq files and assignment of fastq to sample names

### 1.4.7 

- fixed STAR memory allocation issue, now user can run with fewer cpus without a worry for STAR spawning multiple tasks causing out of memory issue.
- made BASH wrapper (not ideal) for `RNAsik` this is capture `bds` logs including report.html which is rather valuable piece of information about the run
- introduced another new aligner - `bwa mem` to do bacterial RNAseq.
- introduced multiqc config file in `configs` directory now
- completely removed `-fqRegex` and added sanity check for paired end data. If R2 is found and -paired isn't set or vice verse then error message sent
- several general bug fixes
- simplified help menu

### 1.4.6

- generalised aligner's call, this will make it easier to add new aligners into RNAsik
- included support for `hista2 `aligner
- added samplesSheep logging
- fixed few minor bugs and improved code quality
- added `canFail` option to several non crucial tasks, allowing pipeline to continue if some task failed of fastqc and qualimap to allow them to fail as those are non essential tasks.

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
