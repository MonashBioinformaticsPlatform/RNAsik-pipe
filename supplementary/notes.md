Strandedness: By default, the counting script assumes your library to be strand-specific, i.e., reads are
aligned to the same strand as the gene they originate from. If you have used a library preparation
protocol that does not preserve strand information (i.e., reads from a given gene can appear equally
likely on either strand), you need to inform the script by specifying the option “-s no”. If your library
preparation protocol reverses the strand (i.e., reads appear on the strand opposite to their gene of
2The possibility to process paired-end data from a file sorted by position is based on recent contributions of PaulTheodor
Pyl to HTSeq.
Inferring differential exon usage in RNA-Seq data with the DEXSeq package 6
origin), use “-s reverse”. In case of paired-end data, the default (-s yes) means that the read from
the first sequence pass is on the same strand as the gene and the read from the second pass on the
opposite strand (“forward-reverse” or “fr” order in the parlance of the Bowtie/TopHat manual) and the
options -s reverse specifies the opposite case.
SAM and BAM files: By default, the script expects its input to be in plain-text SAM format. However,
it can also read BAM files, i.e., files in the the compressed binary variant of the SAM format. If you
wish to do so, use the option “-f bam”. This works only if you have installed the Python package
pysam, which can be found at https://code.google.com/p/pysam/.
Alignment quality: The scripts takes a further option, -a to specify the minimum alignment quality (as
given in the fifth column of the SAM file). All reads with a lower quality than specified (with default
-a 10) are skipped.
Help pages: Calling either script without arguments displays a help page with an overview of all options
and arguments.


Because of file names like these ones you can't really check for _1 and/or _2
It really has to be _R1 and/or _R2
RNA_10_C6HCPANXX_GGCTACAT_L003_R2.fastq.gz
RNA_10_C6HCPANXX_GGCTACAT_L004_R1.fastq.gz
RNA_10_C6HCPANXX_GGCTACAT_L004_R2.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L003_R1.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L003_R2.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L004_R1.fastq.gz
RNA_11_C6HCPANXX_CTTGTAAT_L004_R2.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L003_R1.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L003_R2.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L004_R1.fastq.gz
RNA_12_C6HCPANXX_AGTCAACA_L004_R2.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L003_R1.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L003_R2.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L004_R1.fastq.gz
RNA_1_C6HCPANXX_TGACCAAT_L004_R2.fastq.gz


## Useful links to other pipelines

- http://gkno.me/

---
author: serine
timestamp: 2020.03.03_10:32:35_AEDT
---

https://docs.oracle.com/en/java/javase/11/

## 09.03.2020

It takes a while to kick into gear, especially after a few days of sick leave .. :/
Im thining out loud trying to figure out what was I thinking.

- I want ability to pass on custom command line options to any cmd tool
- I also want to have default cmd tools options stored in a separate config, without a need to hard code anything.
- ideally (and this should work) I want my parameters to be stored in a config file as well, such that I can pretty much re-write entire command via the config file

- level of configuration files:

    - command line options configuration

        - global config or system config, RNAsik comes with it
        - user specified config

    - resources configuration

        - global config or system config, RNAsik comes with it
        - user specified config

    - main config that: Purpose is for user to


##

I think I just want to allow user to pass a single config file a.k.a sik.config where it can pass any keys he/she wants.
And Ill simply build internal a massive map of all allowed keys and error out if the key isnt know, add more keys over time.



make allowed

cat configs/sikResources.config | grep -v "#" | grep -v "^$" | cut -f1 -d" " > configs/supplementary/sikResourcesConfigAllowed.txt

bwa mem |& sed 's/^\s*//' | grep --colo=none "^-" | cut -f1 -d" " > t

## comment 18.03.2020

Cmnt1:
I'm not sure what to do if I find --sjdbSTFfile key in the user (sik.config) config file, do I pass it at indexing step
or do I pass to mapping step? I guess doing at index step would mean that it happened once, whereas if I'm passing it at
the alignment step I would have to pass it every time, N samples.

I guess for now I'll will only pass those to indexing, ah.. actually if the index directory and already exists and/or user passing it in directly
then I should pass those to the alignment step

This config class needs to know whether user has passed in refFiles with pre-existing indecies

Cmnt2:
Because I'm specifically moved to starAligner and starIdx options, previous comment is not of a huge conern, however I should include all of those GTF one into allowed keys for both aligner and indexing


