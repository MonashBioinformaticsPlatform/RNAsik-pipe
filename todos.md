---
author: serine
timestamp: 2021.05.26_23:47:49_UTC
---

## ToDos

- can I pass strand guessing threshold via sik.config? It is causing a few minor issues in strand guessing? Some of the experiments/library preps are well know e.g Trev-seq is forward stranded, but the emperical results are give "weak" strandness i.e 0.85.
- seqkit stats https://bioinf.shenwei.me/seqkit/usage/#stats, very nice tool, can take all fastq files at once and yield single stats file
- fastp https://github.com/OpenGene/fastp

fastp can only use maximum of 16 threads. Not sure why, but thinking I could split fastq files with seqkit into smaller chunks for faster processing
although this might confuse statistics a little, better not

```
for i in  ../raw-data/*_R1*.gz
do
  fastp --thread 16 \
        --in1 $i \
        --in2 ${i/_R1/_R2} \
        --json $(basename ${i%%_R*}).json \
        --html $(basename ${i%%_R*}).html
done
```

```
seqkit stats --all --basename --tabular --out-file seqkit.stats demultiplexed/404LTi*
```

- add gene annotation. I'm thinking to always pull FASTA and Gene annotaitonf rom AnnotationHub() at least for common model organism. Those that exist in the AnnotationHub (ensembl). It is still very tricky to accomodate custom/user inputed annotation. But I think RNAsik shouldn't do "degust" friendly version and instead report an additional command the user can run to make "degust" friendly, and output table of counts from featureCounts

```
Rscript --vanilla ~/gitrepos/RNAsik-pipe/scripts/gene_annotation.R ../refFiles/gene_info.tsv ReverseStrandedCounts.tsv
```

- No need to mask files, pass a list of file to be included into the report to MultiQC instead.  ~~also need to mask featureCounts .summary files the once that are not relevant~~

- remove .repaired files
- add support for multiple fastaRef flags in the config. Instead of manually concatenating files, let RNAsik do that
- add sanity check for mdups flag, to make sure users pass correct values (either default | umi)

## Comments and thoughts

- It is tricky to build good dependencies tree. For example aligned bam files are intermediates that aren't needed later or and therefore deleted. Somehow I don't to set "ultimated" dependencies i.e bamSort
