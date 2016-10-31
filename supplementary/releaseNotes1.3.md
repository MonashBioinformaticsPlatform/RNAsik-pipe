# Release Notes, version 1.3

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
