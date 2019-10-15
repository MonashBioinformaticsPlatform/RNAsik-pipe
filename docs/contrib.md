
![mbp-banner](images/mbp_banner.png)

# Contributing

There are many places for contribution the most obvious ones are help with documentations, help in the [user's group](https://groups.google.com/forum/#!forum/rnasik)
and of course with the source itself.

## Documentations

I'm using [mkdocs](https://github.com/mkdocs/mkdocs) to generate this site, which has been very easy to use.
All documentations are written in plain markdown and located in main repo [`docs/` directory](https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe/tree/master/docs). You can simply fork `RNAsik` repository, do changes to the docs and send me a pull request (PR). Any changes are super welcomed, even one letter spell correction (there'll be more than one), but all changes need to come through PR, which will not only acknowledge you as contributor, but also enable me to review changes quickly and incorporate them in (pull them in) easily.

Quick notes on [mkdocs](https://github.com/mkdocs/mkdocs), it is pretty easy to install with `pip` in `virtualenv` if you prefer (you should).

- to install mkdocs (don't have to use `virtualenv`)

```
virtualenv mkdocs_env
source mkdocs_env/bin/activate
pip install mkdocs
```

- mkdocs in the nutshell

```
mkdocs build
mkdocs gh-deploy
```

This will deploy your copy of `RNAsik` docs to your [github-pages (gh-pages)](https://pages.github.com/)
You actually don't need to do that, you don't need deploy your own copy of the docs to your branch. Just use `mkdocs
server` (read below) to prerview changes and send them through to me.

```
git clone https://github.com/MonashBioinformaticsPlatform/RNAsik-pipe
cd RNAsik-pipe
# do docs changes
```

- get localhost server (to preview your changes)

```
mkdocs server
```

This will give you live updates to you copy of the docs, default URL should be [localhost:8000](localhost:8000), but it will tell you that once you've started the server. Then simply use your favourite text editor to edit markdown documents. Commit your changes, don't be afraid to be verbose, say what you've added/changed/removed in your commit message. And send me PR.

## Developing pipeline further

I need to write a more comprehensive developer guide at sometime soon. Any contributions are again extremely welcomed and again as I've mentioned in the [documentations](#documentations) section above, any contributions need to come through pull request (PR).

To summarise briefly layouts of the `src/`:

- `RNAsik.bds` is the main "executable" file that sources all required modules and runs the pipeline.
- `sikHeader.bds` defines help menu and all user inputs options. I do have a couple of command line
arguments hidden from main help menu, but if you take a pick at this file you'll see them all
- All other `*.bds` files contain functions to specific tasks those functions get called in `RNAsik.bds`

#### Building conda package

First of all you need to install (mini)conda.

- download [miniconda](https://conda.io/miniconda.html) `.sh` installer
- run it and follow the prompts

I run it like this

```BASH
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/.miniconda
```

These are fairly routine steps, but if this is your first time you'll need to do them

- add a few `conda` "channels", this is so `conda` knows where to get things from

```
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
```

- install a couple `conda` packages, required

```
conda install conda-build anaconda-client
```

Note that you can use `-y` flag to say assume `yes` instead of manually entering
yes/no

- you will need a copy of bioconda recipes. I haven't PR my fork to official bioconda channel
so for now it is

```
git clone  https://github.com/serine/bioconda-recipes
cd bioconda-recipes
conda build recipes/rnasik
```

- To install `RNAsik` locally from just build package. You need these two commands.
First command simply list the location of where the `.tar.bz2` file is on the system.
You also need that location if you want to publish to anaconda repository.
The second command simply installs the package

```
conda build recipes/rnasik --output
conda install -y --use-local rnasik
```

- To upload newly build package to anacoda repository
    - set up an account at [Anacoda](https://anaconda.org)
    - `anaconda login`
    - `anaconda upload <path_to_file.tar.bz2>`
    - `anaconda upload <path_to_file.tar.bz2>` --label dev

Once you've logged in once, anaconda will store login token somewhere in your home directory

- here ?

```
~/.continuum/anaconda-client
```

#### RNAsik conda environment

Since version 1.5.4 RNAsik conda package only contains `RNAsik` pipeline without any additional bioinformatics tools. This is because I was having issues building a new version of the conda package. I'm guessing this is to do with the fact that those other bioinformatics tools like samtools etc aren't true dependencies, although I was specifing them under "requirements: run: " the build was spending too much time in "solving environment".
Instead I exported full environmnet and how that on github such that use can simply grab that yaml and re-create RNAsik env

This is how to create new environment yaml config file

```
cat > tools.txt

rnasik
bigdatascript
fastqc
multiqc
bedtools
star==2.7.2b
subread
samtools
picard
bwa
skewer
je-suite
qualimap

ctrl^D
```

```
while read t; do conda install -y $t ;done < tools.txt
```

I know that you can give all of those tools on command line all at once, but this for some reason gets stuck in "solving environment" as well

```
conda env export > rnasik-1.5.4.yaml
```

Optionally you can initiate empty - clean environment before installing all of the packages with

```
conda create --name rnasik-1.5.4
conda activate rnasik-1.5.4
```

And then install and export. This additional step is probably better approach, since you are creating clean RNAsik environment

## Travis CI and testing

Continues integration is very useful to ensure your code is checked continiouslly. RNAsik code is checked (tested)
with every commit. However that testing only as good as I, or hopefully we, will make it. BigDataScript provides
very nice unit testing mechanism, the trick of course it gotta to be written. Currently only very small proportion
of the code is actually covered by tests. A lot of work is needed in this space. Of course one might say that I should
have been writing tests as I was writing my code. Perhaps, but I'm new to this and better later then never!

[Have a look at bds docs](http://pcingola.github.io/BigDataScript/bigDataScript_manual.html#test) on how to write tests.

<p><a href="https://twitter.com/intent/tweet?screen_name=kizza_a" class="twitter-mention-button" data-size="large" data-show-count="false">Tweet to @kizza_a</a><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script> </p>

<p class="twitter-btn">
<a class="twitter-share-button"
  href="https://twitter.com/intent/tweet?text=Hey%20I%27m%20using%20this%20fully%20sick%20RNAseq%20pipeline%20It%27s%20sik%20easy%20http%3A%2F%2Fgithub%2Ecom%2Fmonashbioinformaticsplatform%2FRNAsik%2Dpipe%20by%20%40kizza%5Fa%20from%20%40MonashBioinfo" data-size="large">
Share</a>
</p>
