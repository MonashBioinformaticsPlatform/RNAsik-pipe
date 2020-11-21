#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(tidyr)
library(purrr)

args = commandArgs(trailingOnly=TRUE)

#TODO can instead set it to default to countFiles/
if (length(args) == 0 ) {
  stop("Specify counts directory", call.=FALSE)
}

counts_dir = gsub("/$", "", args[1])

if(!file.exists(counts_dir)) {
  msg <- paste0("Directory doesn't exist -> ", counts_dir, "\n")
  stop(msg)
}

fns1 <- list.files(counts_dir, pattern = "Cnts.txt$", full.names = TRUE)

non_stranded_cnts <- fns1[grepl("_nonCnts.txt", fns1)]
fwd_stranded_cnts <- fns1[grepl("_fwdCnts.txt", fns1)]
rev_stranded_cnts <- fns1[grepl("_revCnts.txt", fns1)]

fns2 <- list("NonStandedCounts" = non_stranded_cnts,
             "ForwardStrandedCounts" = fwd_stranded_cnts,
             "ReverseStrandedCounts" = rev_stranded_cnts)

res1 <- fns2 %>% map(function(cnts) map(cnts, function(n) read_tsv(n, skip = 1)))

res2 <- res1 %>% map(function(dat) Reduce(function(x, y) left_join(x, y, by = c("Geneid", "Chr", "Start", "End", "Strand", "Length")), dat))

res3 <- res2 %>% map(function(dat) dat %>%
                                    gather(sample, counts, -Geneid, -Chr, -Start, -End, -Strand, -Length) %>%
                                    mutate(sample = gsub("_sorted.(repaired|bam)$", "", basename(sample))) %>%
                                    spread(sample, counts))

names(res3) %>% map(function(n) {
                      fn_out <- paste0(counts_dir, "/", n, ".tsv")
                      write_tsv(res3[[n]], fn_out)
                    })
