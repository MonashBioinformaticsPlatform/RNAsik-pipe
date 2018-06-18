#!/bin/bash

origin=${BASH_SOURCE[0]}
test_dir=$(dirname $origin)
scripts_dir=$test_dir/../scripts
get_geneids=$scripts_dir/get_geneids.py
output=$test_dir/output

if [[ ! -d $output ]]
then
  mkdir $output
fi

$get_geneids -h

$get_geneids --help

mm10_ensembl=ftp://ftp.ensembl.org/pub/release-90/gtf/mus_musculus/Mus_musculus.GRCm38.90.gtf.gz
mm10_ensembl_unz=$output/$(basename $mm10_ensembl .gz)

wget -O $output/$(basename $mm10_ensembl) $mm10_ensembl
gunzip -c $output/$(basename $mm10_ensembl) > $mm10_ensembl_unz

if [[ ! -f $mm10_ensembl_unz ]]
then
  echo "ERROR: File not found $mm10_ensembl_unz"
  exit 1
fi

$get_geneids --in_file $mm10_ensembl_unz --file_type gtf > $output/tmp1.geneIds
$get_geneids -i $mm10_ensembl_unz -t gtf > $output/tmp2.geneIds

for f in `ls $output/*.geneIds`
do
  echo "Checking $f file ..."
  if [[ `wc -l $f | cut -f1 -d" "` == 52637 ]]
  then
    echo "all good :)"
  else
    echo "ERROR: no good :("
    exit 1
  fi
done

echo "All done"

echo "Removing output files"
rm $output/*
