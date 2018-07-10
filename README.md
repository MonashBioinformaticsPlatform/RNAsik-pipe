# RNAsik-pipe

[![Build Status](https://travis-ci.org/MonashBioinformaticsPlatform/RNAsik-pipe.svg?branch=master)](https://travis-ci.org/MonashBioinformaticsPlatform/RNAsik-pipe)

[![install-with-conda](https://anaconda.org/serine/rnasik/badges/installer/conda.svg)](https://anaconda.org/serine/rnasik)

[![anaconda-version](https://anaconda.org/serine/rnasik/badges/version.svg)](https://anaconda.org/serine/rnasik/files)

#### This is fully SIcK way towards differential gene expression !

> `RNAsik-pipe` implemented in [BigDataScript (bds)](http://pcingola.github.io/BigDataScript/) language.

## IF( SuperQuickStart ) {

```BASH
RNAsik -fqDir https://bioinformatics.erc.monash.edu/home/kirill/sikTestData/rawData/fqFiles.txt \
       -align star \
       -fastaRef ftp://ftp.ensembl.org/pub/release-91/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna_sm.toplevel.fa.gz \
       -gtfFile ftp://ftp.ensembl.org/pub/release-91/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.91.gtf.gz \
       -counts \
       -paired \
       -all
```

## }

## ELSE [RNAsik-website](https://monashbioinformaticsplatform.github.io/RNAsik-pipe/)
