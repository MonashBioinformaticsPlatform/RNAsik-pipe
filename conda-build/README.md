# Building the conda package

```bash
conda install conda-build
conda build conda-build

# These additional options can be useful on misbehaving (NFS?) filesystems
# --prefix-length 80 --no-long-test-prefix --no-locking
```

... or build with [boa](https://github.com/mamba-org/boa) instead and it will probably be faster.

```bash
conda install -c conda-forge mamba boa conda-verify

conda mambabuild -c defaults -c conda-forge -c bioconda -c serine conda-build 

# The path of the generated package will be output.
# Login to Anaconda Cloud and upload it
anaconda login
anaconda upload -l main "${CONDA_PREFIX}"/conda-bld/linux-64/rnasik-${version}-${build}.tar.bz2
```
