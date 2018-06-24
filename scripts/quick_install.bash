#!/bin/bash

#if [[ -z "$@" ]]
#then
#  echo "USAGE: ./quick_install run"
#  exit 
#fi

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

echo export PATH=$(readlink -f miniconda)/bin:$PATH
export PATH=$(readlink -f miniconda)/bin:$PATH

conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda

conda install --yes --channel serine/label/dev bigdatascript=v2.0+9ad04607
conda install --yes --channel serine/label/dev rnasik=1.5.1+c53adf6
conda install --yes --channel bioconda qualimap
