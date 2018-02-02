
![mbp-banner](images/mbp_banner.png)

# Roadmap 

## Going forward

### 1.4.9 Q1 (January) 2018

- general bug fixes and maintenance

### 1.4.x

- need to have better way to check for index directory, want to know if starIdx includes or doesn't indexing with annotation. 
- recheck [Stuart's PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10/commits/9e64da57de6da066e94bf6fcc66e23c36adb3671), polish off refFiles detection
- recheck [this whole PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10)

### 1.4.10 Q1 (February) 2018

- improve `RNAsik` logging, particular want to make individual tools version logging independent of each other, so that if one wants to run
just counts, `RNAsik` shouldn't complain about `bwa` not found in the PATH. Also double check the behaviour of the logger when pipelines re-runs.
From memory it might not perform as it should. You really want a log of every event that had happened.
- include logging of split lanes and R1 and R2. Want to be able to see from the log whether two reads were classified as split lanes or paired end. This is
to do with recent bug that got fixed in [b924027](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/commit/b9240274fa7c964e953a767c254f31ba0d044547) 

### 1.4.11 Q1 (February/March) 2018

- add `samtools flagstat` qc run. Definitely need this for bacterial RNAseq i.e when running [bwa aligner](https://github.com/lh3/bwa), but this metric
wouldn't hurt in general. It does overlap overall with [STAR aligner](https://github.com/alexdobin/STAR) qc output, but going forward other aligners will be
added/used but `samtools flagstat` will remain
- improve python scripts, make strand_guessing more pythonic, also consider making it python3 friendly as per [Andrews PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/8),
also output ration value as a third value csv value. This is useful number, particular if exit code is 1.
- Document python scripts existence, what they do, how to run them manually in the case of failure, and the output they give

### 1.5.0 Q1 (March) 2018

New feature(s) described below:

- implement new flag `-fqFiles` that can take either a file or a directory.
    - if a directory is given, do what `-fqDir` does now and traverse down retuning list of fastq files. 
    - if a file is given, use those locations getting fastq files. Location can be local file path or URLs, assume one location per line

Will keep `-fqDir` flag, as a backward compatibility with a warning that flag had been deprecated. Will also schedule to remove `-fqDir` completely in future releases
Because of changes in arg's options will do a minor version bump.

- include handling of url based samples sheets, i.e `-samplesSheet` flag should handle local based or remote files, just like `-fastaRef` option

### 1.5.1 Q2 (April) 2018

- general maintenance and bug fixes
- start including unit testing in your master branch, once I'm happy with with `unit_test` branch

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
