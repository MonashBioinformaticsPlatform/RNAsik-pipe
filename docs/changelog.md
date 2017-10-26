# New in version 1.4.6

- generalised aligner's call, this will make it easier to add new aligners into RNAsik
- included support for `hista2 `aligner
- added samplesSheep logging
- fixed few minor bugs and improved code quality
- added `canFail` option to several non crucial tasks, allowing pipeline to continue if some task failed of fastqc and qualimap to allow them to fail as those are non essential tasks.

# New in version 1.4.7 

- fixed STAR memory allocation issue, now user can run with fewer cpus without a worry for STAR spawning multiple tasks causing out of memory issue.
- made BASH wrapper (not ideal) for `RNAsik` this is capture `bds` logs including report.html which is rather valuable piece of information about the run
- introduced another new aligner - `bwa mem` to do bacterial RNAseq.
- introduced multiqc config file in `configs` directory now
- completely removed `-fqRegex` and added sanity check for paired end data. If R2 is found and -paired isn't set or vice verse then error message sent
- several general bug fixes
- simplified help menu

# New in version 1.4.8

- added new feature: coverage plots generation
- added new feature: ability to pass previously generated references directory, saves spaces and time
- fixed strand guessing script, should be better at guessing now
- moved to [mkdocs](http://www.mkdocs.org/) for documents compilation and deployment to gh_pages
- added new python script to make degust file, this simplifies and strengthens the code
- improved readability of the code
- improved and fixed bugs in handling fastq files and assignment of fastq to sample names
