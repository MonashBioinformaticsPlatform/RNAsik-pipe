# Checklist

I feel that the researchers some what commonly ask bioinformaticians - What do you need to know about the experiment?

The short answer is everything ! but here is a break down of everything..

> The best practice is to gather all of the information in the checklist before the analysis.

## Must 

If the below information isn't give I can't really do the analysis

- Have you got raw (FASTQ) files?
- What is your model organism?
- Which reference database to use? (e.g. ucsc, ensembl, refseq)
- Additional reference files e.g transgenes? will need relevant files (FASTA , GTF/GFF)
- Do you have a samples sheet for me?

## Should

I'm saying should, but really the more information you provide the more
accurate - more reflective analysis is going to be of your biological experiment

- Have I got enough explanation about experimental design including:
    - Any batch effects. Paired-data (eg. individual before/after treatment)
    - Comparisons of interest.  Pairwise? Interaction?
    - Additional factors for contrast matrix:
        - sample pairing
        - sex
        - time points
        - phenotype
        - stimulus
        - other..

## Up to you

This is your experiment and your money and time spend on it. I'm just saying 
that there are instrument to instrument variations and biases. As well as 
certain artifacts due to particular library preparation method. On top of that
you'll need this information if you are going to publish your results in a paper.

- Which sequencing facility was doing the sequencing?
- Library preparation info:
    - library type: single or paired end
    - preparation method ribo-depletion or poly(A), other
    - is library stranded 
    - name of preparation kit was used
- Sequencer used (e.g HiSeq1500, NovaSeq, NextSeq etc)
- Are you keeping a copy of your raw data somewhere safe
