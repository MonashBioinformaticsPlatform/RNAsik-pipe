library(readr)
library(dplyr)
library(tidyr)

args = commandArgs(trailingOnly=TRUE)

#TODO can instead set it to default to countFiles/
if (length(args) == 0 ) {
  stop("USAGE: genes_annotation.R <GENES_INFO> <COUNTS>", call.=FALSE)
}

#TODO check that the files exist
gene_info_fn <- args[1]
counts_fn <- args[2]

gene_info <- read_tsv(gene_info_fn, col_types = cols(Chr = col_character()))

counts <- read_tsv(counts_fn) %>%
           select(-Chr, -Strand, -Start, -End, -Length) # want to drop Chr from featureCounts because it contains comma separated values, one for each exon

drop <- c("Geneid")
sample_names <- colnames(counts)
sample_names <- sample_names[!(colnames(counts) %in% drop)] %>% sort()

col_names <- c("GeneId", "Chr", "GeneName", "Start", "End", "Strand", "Biotype", "GeneWidth", sample_names)
#TODO somehow make sure all of those columns exists

left_join(counts, gene_info, by = c("Geneid")) %>%
    rename(GeneId = Geneid,
           Biotype = biotype,
           GeneWidth = width) %>%
    select(all_of(col_names)) %>%
    #filter(Biotype == "protein_coding") %>%
    na.omit() %>%
    write_tsv("counts.tsv")
    #select(GeneId, Chr, GeneName, Start, End, Strand, biotype, Length, width, sample_names))
