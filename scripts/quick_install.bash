#!/bin/bash

version="1.5.4"
config="${version}.yaml"

name="rnasik-${version}"
conda_env="${name}.yaml"

if [[ ${TRAVIS_PYTHON_VERSION:0:1} == "2" ]]
then
  wget http://repo.continuum.io/miniconda/Miniconda-2.0.0-Linux-x86_64.sh -O miniconda.sh
else
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
fi

if ! [[ -d miniconda ]]
then
  bash miniconda.sh -b -p miniconda
elif ! [[ -d miniconda/bin ]]
then
  echo "ERROR: This can't happend, bin/ directory must exist inside miniconda directory"
fi

conda_sh=$(realpath miniconda/etc/profile.d/conda.sh)
source ${conda_sh}

wget -O ${conda_env} "https://raw.githubusercontent.com/MonashBioinformaticsPlatform/RNAsik-pipe/master/supplementary/conda_envs/${config}"
conda env create --name ${name} --file ${conda_env}

echo ""
echo "MSG: Run this command to source conda"
echo "     source ${conda_sh}"
echo ""
echo "MSG: And run this command to activate RNAsik environment"
echo "     conda activate ${name}"
echo ""
