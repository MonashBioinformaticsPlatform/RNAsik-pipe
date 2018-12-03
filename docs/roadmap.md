
![mbp-banner](images/mbp_banner.png)

# Roadmap

## Going forward

### 1.x.x

- need to have better way to check for index directory, want to know if starIdx includes or doesn't indexing with annotation.
- recheck [Stuart's PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10/commits/9e64da57de6da066e94bf6fcc66e23c36adb3671), polish off refFiles detection
- recheck [this whole PR](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/pull/10)
- noticed that qualimap could have high RAM consumption, need to fix cpu and mem parameters passing through sik.config file. Reckon to set mem at 4 or 6 Gb
- add support for another aligner - [minimap2](https://github.com/lh3/minimap2)

### 1.5.4 (end of the year) 2018

- include handling of url based samples sheets, i.e `-samplesSheet` flag should handle local based or remote files, just like `-fastaRef` option
- better tools version logging, don't like when `RNAsik` checks `bwa` version when `STAR` aligner is used
- include logging of split lanes and R1 and R2. Want to be able to see from the log whether two reads were classified as split lanes or paired end. This is
to do with recent bug that got fixed in [b924027](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/commit/b9240274fa7c964e953a767c254f31ba0d044547)
- add alignment free support for RNAseq analysis salmon/kalisto

### 1.6.0 (February/March) 2019

- Plans to add variants calling to `RNAsik`. It'll be opt in flag,  `-varsCall`. Suggestions are welcomed about different name for a flag.
I already have a prototype in bds, just need to plug it in.

    - Not sure which caller to use `GATK` or `freebayes` will need to do more reading on that.
    - Also need to document common pitfalls for using RNAseq for variant calling e.g can only can variances in coding regions that are expressed.
    - Not a good idea to use pulled samples as you won't be able to get allele frequency
    - will also need to find out where to get known SNP's (snpDB? for known germ line mutations) and a list of blacklisted regions

- [an example of someone else variant calling pipeline](https://github.com/CRG-CNAG/CalliNGS-NF)

## Ideas for future releases

- Need better support for exonic/intronic rates estimation. Is `read_distribution.py` from RSeQC good idea? Right now qualiMap is ok flag to opt in.
- is there need for circular RNA support?
- add demultiplexign tools into pipeline; `-demult`, [more info here](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/issues/32)

## Changelog

### 1.5.2

features:

  - `-fqDir` can now take file with links to fastq files, links can have local or remote paths
  - coverage plots are now stranded, i.e for every bam file you'll get forward, reverse and all (non) stranded coverages
  - trimming has now support for both single and paired-end data
  - started to include logging of individual tools, started with sikQC.bds file. Basically redirecting individual tools stderr/stdout into logs files.

maintenance:

  - include continue integration testing - TraviCI and started writing more test that cover bds source as well as additional scripts source
  - bug fixes and improvements of python scripts.
  - added testing for `get_geneids.py` script, this isn't python unit test rather simple "does the tool run" type test.
  - introduced short args notation for python scripts as an option to long args naming
  - pulled [@pansapiens](https://github.com/pansapiens) PR, now we have `RNASIK_BDS_CONFIG` variable for passing bds.config
  - fixed samtools sort bug that led to out-of-memory kill
  - all (most?) picard tools now have mem and cpu parameters
  - fixed bwa mem dependencies issue, for [more info here](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/blob/b5acbd03c0b79323420caead79927c6c4e00f92e/src/sikSTARaligner.bds#L62)
  - fixed qualimap issue with DISPLAY variable, explicitly unsetting it now
  - fixed pairIds overide, only set pairIds to default value _R1,_R2 if no -pairIds given on cmd
  - removed paired-end checking from inside bwa, all checks happens outside of alinger scope now
  - improved multiqc report visual, by tweaking config file, the report shouldn't look as cluttered

conda:

  - started packaging bds and RNAsik with conda, packages are available at [my anaconda channel](https://anaconda.org/serine)
  - updated docs with how to conda build, install and upload
  - wrote quick_install.bash script that does install and used in traviCI

### 1.5.1

- several bug fixes including [#18](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/issues/18), hisat2 related bugs, and samtools sort memory bug
- in relation to bug [#18](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/issues/18) added extra [sanity check](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/blob/b3f91ca72e2c34a97f3d6b757a2fc3b9027df001/src/sikUtils.bds#L153)
- general code improvement and maintenance
- updated docs and included new installation method
- improved python scripts, made them user executable and updated docs with how to use them
- updated UCSC binaries due to libpng12 issue

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

### 1.3

## Content

- [General](#general)
- [STAR](#star)
- [featureCounts](#featureCounts)

#### General

- Improved documentations and help menu
- Introduced new `-extraOptions` command. Now user can pass in any additional commands that particular tools can have. This will make pipeline rather flexible.
- Included more checks along the way, such as:

    - checking if directories and files given on the cli are valid and accessible
    - check if FASTQ files where found in the given location
    - if no `-align` option was specified check that `bamFiles` directory exists and has BAM files
    - if no `-prePro` options specified checks for `preqcBamFiles` directory and not present through an error. Can now use `-proBams` for processed bams to specify RNAseQC ready bams

- Made `RNAsik-pipe` more sequential, i.e step one run STAR, then run featureCounts then run processing steps. Previously featureCounts and picard tools were running in paralell and I/O was suffering. It is faster to have featureCounts end its run before doing picard processing.

- Removed `-makeIndicies` and `-fqDirs` options and simplified input
    - Combined `-fqDir` and `fqDirs` into single flag `-fqDir` under which you can specify either directory with FASTQ's or a project directory with directories with FASTQ's. In another way, now pipeline looks two level deep for FASTQ files in a given directory under `-fqDir`
    - `-makeIndex` now only makes STAR index. In future it might accept aligner name for which to make an index
    - other indicies for picard and RNAseQC are now made on the fly when those tools are called
- Don't have to specify `-makeIndex` if running an alignment. If `-align` given and no `-genomeIndex` is specified, then pipeline will ask for `-fastaRef` and make index before aligning
- Improved scoping. RNAsik-pipe is a mine file that runs everything, all other files define functions and don't look outside of the file. Everything is passed in from within main file - RANsik-pipe.
- Included an option to specify gzipped files, but not in the `-extraOptions` if additoinal file is need to be given through `extraOptions` and file is gzipped it won't be handled. The gzipped option is specific for `fastaRef` and `gtfFile` only. Those can be gzipped and pipieline will handle it.
- also now copy `fastaRef` and `gtfFile` into `refFiles` directory. This is to avoid permission issues. Because original destination might not have all the required files, such as `.dict` and `.fai` files and if not permitted pipeline won't be able to execute certain steps.
- Introduced `-sampleNames` options now user can "fix" BAM file names and all the downstream file and data naming to something more minegful.

#### STAR

- Changed bool `-star` option for `-align` that now accepts a string. At the moment the only string it can accept is `star` (lower case). This is again step towards making pipeline more flexible for users demands. In future I'm planing to introduce other aligners to my pipeline so that user perhaps can choose an aligner.
- Auto detect is FASTQ are paired-end or not. Wrote a function that loops through `-fqDir` directory and counting all the R1 and R2 reads. Based on the counts it ditermines whether data is paired end or not.

#### featureCounts

- included a couple of python script that uses `gffutils` package to make a datatbase of GTF entries and then parse that database file to get public gene names, Ensmebl Ids and gene's biotypes. It is easy to include more information about the gene with this python module.
- Included more post processing on count files, now they are ready for degust upload

### 1.2

- Changed the way `RNAsik-pipe` gets read counts files. Now it creates only two files one for reverse
stranded data and another for non stranded data. featureNo and featureReverse directories with
corresponding read counts files have been removed and replaced with featureNo.txt and
featureRevere.txt that already will have all of your reads in columns as expected by
[Degust](http://www.vicbioinformatics.com/degust/). Minor cosmetic changes are made to both
featureNo.txt and featureReverse.txt to convert then into featureNoCounts.txt and
featureReverseCounts.txt respectively. Use counts file for your
[Degust](http://www.vicbioinformatics.com/degust/) session.

- Added `threads` option, default at [1], so that user can specify number of threads they wish to
  use.

- Added `makeIndex` option, which allows user to either make all indices with `makeIndices`, that is
  `STAR genomeGenerate`, `picard CreateSequnceDictionary` and `samtools faidx`, but given that STAR index
takes a long time, can be some hours if running on minimal number of threads and user already has
BAM files and just wishes to use other modules of the `RNAsik-pipe`, user can now just make other
required indices.

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
