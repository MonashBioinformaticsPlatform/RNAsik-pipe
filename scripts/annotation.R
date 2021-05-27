library(AnnotationHub)

ah <- AnnotationHub()

release <- "AH89956"
mus <- query(ah, c("Ensembl", "GRCm39", "Mus musculus"))
gene_models_gr <- mus[[release]]

gene_models[gene_models$type == "gene"][,c("gene_id", "gene_name", "gene_biotype")] %>%
    as.data.frame() %>%
    dplyr::rename(Chr = seqnames,
                  Geneid = gene_id,
                  GeneName = gene_name,
                  biotype = gene_biotype,
                  Start = start,
                  End = end,
                  Strand = strand) %>%
  write_tsv("gene_info.tsv")

