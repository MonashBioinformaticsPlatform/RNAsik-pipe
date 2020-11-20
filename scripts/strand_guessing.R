#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(tidyr)

args = commandArgs(trailingOnly=TRUE)

#TODO can instead set it to default to countFiles/
if (length(args) == 0 ) {
  stop("Specify counts directory", call.=FALSE)
}

counts_dir = args[1]

if(!file.exists(counts_dir)) {
  msg <- paste0("Directory doesn't exist -> ", counts_dir, "\n")
  stop(msg)
}

fns <- list.files(counts_dir, pattern = ".summary")

# NOTES:
#
# > res1: is a list of data.frames, one for each counts file, normally should only be three
# NonStrandedCounts, ReverseStrandedCounts and ForwardStrandedCounts.
# Column table 'Status Sample Value' where Status value is one of:
#
# - Assigned
# - Unassigned_Ambiguity
# - Unassigned_Chimera
# - Unassigned_Duplicate
# - Unassigned_FragmentLength
# - Unassigned_MappingQuality
# - Unassigned_MultiMapping
# - Unassigned_NoFeatures
# - Unassigned_NonSplit
# - Unassigned_Overlapping_Length
# - Unassigned_Secondary
# - Unassigned_Unmapped
#
# > res2: res1 list aggregated into single tibble, easy to work with
#
# > res3: res2 data.frame with added column strand_sore, as per cal_strand_score function
# This data.frame is full of information about reads distribution and mappibility to features

res1 <- lapply(fns, function(fn) read_tsv(fn) %>% gather(sample, value, -Status))
res2 <- Reduce(function(x, y) left_join(x, y, by = c("Status", "sample")), res1)

nn <- basename(fns)
nn <- gsub("StrandedCounts.txt.summary$", "", nn)

colnames(res2) <- c("status", "sample", nn)

cal_strand_score <- function(fow, rev) {
  (fow - rev) / (fow + rev)
}

res3 <- res2 %>%
	  mutate(strand_score = cal_strand_score(Forward, Reverse)) %>%
          arrange(status, sample)
          #filter(abs(strand) > 0, !is.na(strand))

out1_fn <- paste0(counts_dir, "/strandInfoAll.tsv")
out2_fn <- paste0(counts_dir, "/strandInfoPerSample.tsv")
out3_fn <- paste0(counts_dir, "/strandInfoGuess.tsv")

res3 %>% write_tsv(out1_fn)

res3 %>%
  filter(status == "Assigned") %>%
  write_tsv(out2_fn)

mean_strand_score <- res3 %>%
                       filter(status == "Assigned") %>%
                       summarize(mean_strand_score = mean(strand_score)) %>%
                       select(mean_strand_score) %>%
	               unlist() %>%
	               unname()

strnd_test = (19 - 1) / (20 + 1)  # 0.857
non_strnd_test = (55 - 45) / (55 + 45)  # 0.1

out3 <- ""

if(abs(mean_strand_score) > strnd_test) {
  if(mean_strand_score >= 0) {
    out3 <- paste0("ForwardStrandedCounts,", mean_strand_score, ",0")
  } else {
    out3 <- paste0("ReverseStrandedCounts,", mean_strand_score, ",0")
  }
} else if(abs(mean_strand_score) < non_strnd_test) {
    out3 <- paste0("NonStrandedCounts,", mean_strand_score, ",0")
} else if(non_strnd_test < abs(mean_strand_score) | strnd_test > abs(mean_strand_score)) {
    out3 <- paste0("NonStrandedCounts,", mean_strand_score, ",1")
} else {
    stop("This shouldn't happen")
}

out3_header <- "strand_type,mean_score,exit_code"
gsub(",", "\t", out3_header) %>% write(out3_fn)
gsub(",", "\t", out3) %>% write(out3_fn, append = TRUE)
