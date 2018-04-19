## Using bio-ansible

### Quick start

- [watch it on youtube](https://www.youtube.com/watch?v=oHRa9iniy3o)

```
sudo apt-get install unzip make gcc git python-virtualenv
sudo apt-get install zlib1g-dev libbz2-dev liblzma-dev libncurses5-dev
sudo apt-get install openjdk-8-jdk ant golang-go
sudo apt-get install git htop tmux vim

virtualenv ~/ansible_env
source ~/ansible_env/bin/activate

pip install --upgrade pip
pip install ansible

git clone https://github.com/MonashBioinformaticsPlatform/bio-ansible
cd bio-ansible/
ansible-playbook -i hosts bio.yml --tags dirs,bds,rnasik,star,bwa,hisat2,subread,samtools,htslib,bedtools,picard,qualimap,fastqc,multiqc

export PATH=$HOME/bioansible/software/apps/BigDataScript-0.99999g:$PATH
export PATH=$HOME/bioansible/software/apps/RNAsik-pipe-1.4.9/bin:$PATH

RNAsik
```

## Tools prerequisites

I tried to account for every sub-dependency in [bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible), definitely checked against vanilla ubuntu 16.04 linux distro, however other systems/linux distros might have slight deviation from this. If you run into trouble please double check dependencies for the tool that is failing.
There is quite a spectrum of languages there in the pipeline, C/C++, java and python so far. One can image the difficulty to accommodate every distro and/or system. I'm doing my best !

- [BigDataScript](http://pcingola.github.io/BigDataScript/download.html)
- [STAR aligner](https://github.com/alexdobin/STAR/releases)
- [subread](http://subread.sourceforge.net/)
- [samtools](http://www.htslib.org/download/)
- [bedtools2](http://bedtools.readthedocs.io/en/latest/index.html)
- [Picard tools](http://broadinstitute.github.io/picard/)
- [QualiMap](http://qualimap.bioinfo.cipf.es/)
- [MultiQC](http://multiqc.info/) 
- [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/)

## System prerequisites

In order to install system dependencies you'll need admin privilege i.e `sudo`

**General**, these are you "stock" utils, that most running system will/should have

- `unzip`
- `make`
- `gcc`
- `git`
- `python-virtualenv`

```
sudo apt-get install unzip make gcc git python-virtualenv
```

**samtools, htslib and bwa deps**, these are some what specific libraries

- `zlib1g-dev` 
- `libbz2-dev` 
- `liblzma-dev`
- `libncurses5-dev`

```
sudo apt-get install zlib1g-dev libbz2-dev liblzma-dev libncurses5-dev
```

**Java and BigDataScript**, these again rather generic packages, except golang. 
Note that golang is pretty easy to install, comes as a pre-compiled binary [here](https://golang.org/dl/) if you don't want to get it through system package mamanger

- `openjdk-8-jdk` 
- `ant`
- `golang-go`

```
sudo apt-get install openjdk-8-jdk ant golang-go
```

**Extras**, these are optional dependencies, but `tmux` especially recommended as pipeline run could take some time to complete
_provided you are doing this on remote machine (server), which is also recommended_

- `htop`
- `tmux`
- `vim`

```
sudo apt-get install git htop tmux vim
```

## Running bio-ansible

Follow [ansible installation guid](http://docs.ansible.com/ansible/intro_installation.html) to get ansible then:

```BASH
git clone https://github.com/MonashBioinformaticsPlatform/bio-ansible
cd bio-ansible/
ansible-playbook -i hosts bio.yml --tags dirs,bds,rnasik,star,bwa,hisat2,subread,samtools,htslib,bedtools,picard,qualimap,fastqc,multiqc
```

## Alternative installation method for RNAsik

If you have all of the tools installed and you just need `RNAsik` you can simply `git clone` it. It doesn't require any
other installations/compilations. BUT you do need to have [BigDataScript](https://github.com/pcingola/BigDataScript) installed
and have it in your `PATH` for `RNAsik` to run

```BASH
git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe
path/to/RNAsik-pipe/bin/RNAsik
```

## Make RNAsik analysis ready

[bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) is complete bioinformatics stack (with heavily genomics focus at this stage) deployment written in ansible script, which depending on a type of deployment might require admin privilege i.e `sudo`.
Given that [system prerequisites](#system-prerequisites) are satisfied one **don't** need `sudo` to install bioinformatics stack, primarily [bio_tools](https://github.com/MonashBioinformaticsPlatform/bio-ansible/blob/master/roles/bio_tools/tasks/main.yml).

In this docs there is an assumption that user either has `sudo` rights and/or able to install [system prerequisites](#system-prerequisites) OR already has those dependencies installed and therefore can simply use [bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) as per installing `RNAsik` section above to get all required tools dependencies.

Also right now [bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) is focused on a particular tools/enviroment management type, which is [lmod](https://lmod.readthedocs.io/en/latest/), where one can `module load samtools` into their environment for use, by default `samtools` isn't available in the current (shell) environment. This is rather common approach on HPC clusters. Because of that type of installation, if user doesn't have pre-installed `lmod` they will needs to either `export PATH` for every tool (sounds a bit annoying), OR `export` `RNAsik` into your `PATH` and them simply let `RNAsik` know where tools are through `-configFile` option.

```
export PATH=$HOME/bioansible/software/apps/BigDataScript-0.99999g:$PATH
export PATH=$HOME/bioansible/software/apps/RNAsik-pipe-1.4.9/bin:$PATH
```

copy these lines into file e.g sik.config and add `-configFile path/to/sik.config` to `RNAsik`

```
starExe = $HOME/bioansible/software/apps/STAR-2.5.2b/STAR
hisat2Exe = $HOME/bioansible/software/apps/hisat2-2.1.0/bin/hisat2
bwaExe = $HOME/bioansible/software/apps/bwa-v0.7.15/bwa
samtoolsExe = $HOME/bioansible/software/apps/samtools-1.4.1/bin/samtools
bedtoolsExe = $HOME/bioansible/software/apps/bedtools2-2.25.0/bin/bedtools
countsExe = $HOME/bioansible/software/apps/subread-1.5.2/bin/featureCounts
fastqcExe = $HOME/bioansible/software/apps/fastqc-0.11.5/fastqc
pythonExe = python
picardExe = java -Xmx6g -jar $HOME/bioansible/software/apps/picard-2.17.10/picard.jar
qualimapExe = $HOME/bioansible/software/apps/qualimap_v2.2.1/qualimap
multiqcExe = $HOME/bioansible/software/apps/multiqc-1.4/bin/multiqc
```

If the user happens to have `lmod` installed, simply `module use $HOME/bioansible/software/modules/bio` to let `lmod` know about new modules and then simply `module load RNAsik-pipe`, which will automatically "pull" other dependencies into your environment. You can check that by `module list` to see what is in your environment
### Make RNAsik analysis ready

[bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) is complete bioinformatics stack (with heavily genomics focus at this stage) deployment written in ansible script, which depending on a type of deployment might require admin privilege i.e `sudo`.
Given that [system prerequisites](#system-prerequisites) are satisfied one **don't** need `sudo` to install bioinformatics stack, primarily [bio_tools](https://github.com/MonashBioinformaticsPlatform/bio-ansible/blob/master/roles/bio_tools/tasks/main.yml).

In this docs there is an assumption that user either has `sudo` rights and/or able to install [system prerequisites](#system-prerequisites) OR already has those dependencies installed and therefore can simply use [bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) as per installing `RNAsik` section above to get all required tools dependencies.

Also right now [bio-ansible](https://github.com/MonashBioinformaticsPlatform/bio-ansible) is focused on a particular tools/enviroment management type, which is [lmod](https://lmod.readthedocs.io/en/latest/), where one can `module load samtools` into their environment for use, by default `samtools` isn't available in the current (shell) environment. This is rather common approach on HPC clusters. Because of that type of installation, if user doesn't have pre-installed `lmod` they will needs to either `export PATH` for every tool (sounds a bit annoying), OR `export` `RNAsik` into your `PATH` and them simply let `RNAsik` know where tools are through `-configFile` option.

```
export PATH=$HOME/bioansible/software/apps/BigDataScript-0.99999g:$PATH
export PATH=$HOME/bioansible/software/apps/RNAsik-pipe-1.4.9/bin:$PATH
```

copy these lines into file e.g sik.config and add `-configFile path/to/sik.config` to `RNAsik`

```
starExe = $HOME/bioansible/software/apps/STAR-2.5.2b/STAR
hisat2Exe = $HOME/bioansible/software/apps/hisat2-2.1.0/bin/hisat2
bwaExe = $HOME/bioansible/software/apps/bwa-v0.7.15/bwa
samtoolsExe = $HOME/bioansible/software/apps/samtools-1.4.1/bin/samtools
bedtoolsExe = $HOME/bioansible/software/apps/bedtools2-2.25.0/bin/bedtools
countsExe = $HOME/bioansible/software/apps/subread-1.5.2/bin/featureCounts
fastqcExe = $HOME/bioansible/software/apps/fastqc-0.11.5/fastqc
pythonExe = python
picardExe = java -Xmx6g -jar $HOME/bioansible/software/apps/picard-2.17.10/picard.jar
qualimapExe = $HOME/bioansible/software/apps/qualimap_v2.2.1/qualimap
multiqcExe = $HOME/bioansible/software/apps/multiqc-1.4/bin/multiqc
```

If the user happens to have `lmod` installed, simply `module use $HOME/bioansible/software/modules/bio` to let `lmod` know about new modules and then simply `module load RNAsik-pipe`, which will automatically "pull" other dependencies into your environment. You can check that by `module list` to see what is in your environment
