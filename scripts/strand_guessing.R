#!/usr/bin/env Rscript

# NOTES:
#
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
# > res5: res2 data.frame with added column strand_sore, as per cal_strand_score function
# This data.frame is full of information about reads distribution and mappibility to features

library(readr)
library(dplyr)
library(tidyr)
library(purrr)

args = commandArgs(trailingOnly=TRUE)

#TODO can instead set it to default to countFiles/
if (length(args) == 0 ) {
  stop("Specify counts directory", call.=FALSE)
}

counts_dir = args[1]

if(!dir.exists(counts_dir)) {
  msg <- paste0("Directory doesn't exist -> ", counts_dir, "\n")
  stop(msg)
}

fns1 <- list.files(counts_dir, pattern = "txt.summary$", full.names = TRUE)

non_stranded_cnts <- fns1[grepl("_nonCnts.txt.summary", fns1)]
fwd_stranded_cnts <- fns1[grepl("_fwdCnts.txt.summary", fns1)]
rev_stranded_cnts <- fns1[grepl("_revCnts.txt.summary", fns1)]

fns2 <- list("NonStandedStats" = non_stranded_cnts,
             "ForwardStrandedStats" = fwd_stranded_cnts,
             "ReverseStrandedStats" = rev_stranded_cnts)

res1 <- fns2 %>% map(function(stats) map(stats, function(n) read_tsv(n)))

res2 <- res1 %>% map(function(dat) Reduce(function(x, y) left_join(x, y, by = "Status"), dat))

res3 <- res2 %>% map(function(dat) dat %>%
                                    gather(sample, stats, -Status) %>%
                                    mutate(sample = gsub("_sorted.(repaired|bam)$", "", basename(sample))))

names(res3) %>% map(function(n) {
                      fn_out <- paste0(counts_dir, "/", gsub("Stats", "Counts", n), ".tsv.summary")
		      dat <- res3[[n]]
		      ss <- unique(dat[["sample"]])
		      #TODO should assert that ss is a length of one
		      dat <- dat %>% select(-sample)
		      colnames(dat) <- c("Status", ss)
                      write_tsv(dat, fn_out)
                    })

res4 <- names(res3) %>% map(function(n) res3[[n]] %>% dplyr::rename(!!n := stats))

res5 <- Reduce(function(x, y) left_join(x, y, by = c("Status", "sample")), res4)

cal_strand_score <- function(fow, rev) {
  (fow - rev) / (fow + rev)
}

res6 <- res5 %>%
	  mutate(strand_score = cal_strand_score(ForwardStrandedStats, ReverseStrandedStats)) %>%
          arrange(Status, sample)
          #filter(abs(strand) > 0, !is.na(strand))

out1_fn <- paste0(counts_dir, "/strandInfoAll.tsv")
out2_fn <- paste0(counts_dir, "/strandInfoPerSample.tsv")
out3_fn <- paste0(counts_dir, "/strandInfoGuess.tsv")

res6 %>% write_tsv(out1_fn)

res6 %>%
  filter(Status == "Assigned") %>%
  write_tsv(out2_fn)

mean_strand_score <- res6 %>%
                       filter(Status == "Assigned") %>%
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

archive_dir <- paste0(counts_dir, "/.archive/")

if(!dir.exists(archive_dir)) {
  msg <- paste0("Archiving individual summary files -> ", archive_dir, "\n")
  cat(msg)
  dir.create(archive_dir, recursive = TRUE)
}

fns1 %>% map(function(n) file.rename(n, paste0(archive_dir, basename(n))))
