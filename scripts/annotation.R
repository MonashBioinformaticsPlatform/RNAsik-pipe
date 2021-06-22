library(AnnotationHub)
library(tidyverse)

ah <- AnnotationHub()

dat1 <- ah %>%
#dat2 <- ah2 %>%
#dat3 <- ah3 %>%
#dat4 <- mus %>%
          mcols %>%
          as.data.frame() %>%
          rownames_to_column(var = "id") %>%
          as_tibble()

# to find orgDb package for mouse genome
q <- query(ah, c("Mus musculus"))
# to get the key name to retrive the information
# in this case there was only one record with the key AH84123
names(q)

org_db <- ah[["AH84123"]]

k <- AnnotationDbi::keys(org_db)
# to get a list of possible column in the db
AnnotationDbi::columns(org_db)

info <- AnnotationDbi::select(org_db,
                              keys = k,
                              keytype = "ENTREZID",
                              columns = c("ENSEMBL",
                                          "GENENAME",
                                          "MGI",
                                          "ENZYME",
                                          #"GO",
                                          #"GOALL",
                                          #"ONTOLOGY",
                                          "PROSITE"))


db_entries <- dat1 %>%
                filter(dataprovider == "Ensembl",
                       species == "Mus musculus",
                       genome == "GRCm39")

# this will load ensembldb package
ens_db <- ah[["AH89457"]]

genes <- ensembldb::genes(ens_db,
                          columns = c(listColumns(ens_db, "gene")),
                          return.type = "data.frame")

genes <- genes %>%
            as_tibble() %>%
            dplyr::rename(start = gene_seq_start,
                          end = gene_seq_end)

exons <- ensembldb::exons(ens_db,
                          columns = c(listColumns(ens_db, "exon"), "gene_id"),
                          return.type = "data.frame")

exons <- exons %>%
            as_tibble() %>%
            dplyr::rename(start = exon_seq_start,
                          end = exon_seq_end)

dat1 <- full_join(genes, exons, by = c("gene_id", "start", "end"))

ee <- ensembldb::exons(ens_db)
dd <- ensembldb::disjointExons(ens_db, aggregateGenes = T)
m <- findOverlaps(ee, dd, type = "equal")

res <- dd[subjectHits(m), ]
mcols(res)[["exon_id"]] <- mcols(ee[queryHits(m),])[["exon_id"]]


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

