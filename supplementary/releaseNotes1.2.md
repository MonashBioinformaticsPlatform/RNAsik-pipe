## Release Notes, version 1.2

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
