
![mbp-banner](images/mbp_banner.png)

# Roadmap 

## Going forward

### 1.5.0 

New feature(s) described below:

- implement new flag `-fqFiles` that can take either a file or a directory.
    - if a directory is given, do what `-fqDir` does now and traverse down retuning list of fastq files. 
    - if a file is given, use those locations getting fastq files. Location can be local file path or URLs, assume one location per line

Because this will "break"/change `RNAsik` as `-fqDir` flag will be removed, needs a minor version bump. I can make it backwards compatible, 
probably should do that.

### 1.4.9

- general bug fixes and maintenance

## ToDo's 

- include IGVlink into RNAsik-pipe output, can only do that if data outputted into something that is hostable i.e object store?
- Need better support for exonic/intronic rates estimation. Is `read_distribution.py` from RSeQC good idea? Right now qualiMap is ok
- add variants calling, already have a prototype, but still not sure if this is a good idea given different
experimental designs. For example if samples were pooled then variant calling isn't valid anymore. Can make it a 
flag to opt in.
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
