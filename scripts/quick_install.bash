#!/bin/bash

version="1.5.5"
build=1

miniconda_fn="miniconda.sh"
miniconda_dir="miniconda"

if ! [[ -d ${miniconda_dir} ]]
then
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ${miniconda_fn}
  bash ${miniconda_fn} -b -p ${miniconda_dir}
elif ! [[ -d "${miniconda_dir}/bin" ]]
then
  echo "ERROR: This can't happend, bin/ directory must exist inside miniconda directory"
fi

conda_sh=$(realpath miniconda/etc/profile.d/conda.sh)
source ${conda_sh}

conda update --name base \
             --channel defaults \
             conda \

conda create --name rnasik-1.5.5 \
             --channel serine \
             --yes \
             "rnasik=${version}=${build}"
