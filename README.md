# Identify the promoter Among ATAC-seq data

Our goal is to find the promoter automatically by only giving raw data of ATAC-seq data. For now, we just have the open datasets and tried to do some further analysis about the raw data. 



This work **is still in progress**. By now, we have finished data pre-processing of some open datasets in NCBI. I want to write down some specific steps here to remind me in the future. But if possible, I really happy this can provide some help for you. 



## Prerequisites

- Data:  **[SRX7806722](https://www.ncbi.nlm.nih.gov/sra/SRX7806722[accn])** Drosophila melanogaster, ATAC-seq (SRR11186388-SRR11186393) 
  - 2 time slots (48hr,72hr)
- Systems: Linux/OS
- Language: Python(3.71) 



## Pre-processing & Analysis

1. Following the [ATAC-seq Guidelines](https://informatics.fas.harvard.edu/atac-seq-guidelines.html). There are some discussion about the major steps in ATAC-seq data analysis, inlcuding quality-check,alignment and peak-calling. 

   - **Download the dataset**. Here we had better use **paired-end sequencing**. 

     - Using **NBIC** dataset to visit the dataset, you could download **SRA** **Toolkit** first, which is helpful to you to download datasets. You can download SRA files or other required reference sequences by using command `prefetch`. 

       For example, 

       ```
       prefetch SRR11186388
       ```

     - Also, if you want to convert SRA files into other data formats, `fast-dump` could help you do so. This work like prefetch, as the tools will also automatically acquire all needed reference sequences. But if you want to operate on a local file, it can do as well. 

       ```
       fastq-dump --outdir ./ --skip-technical --readids --read-filter pass --dumpbase --split-3 --clip SRR11186388  
       ```

       There are so many used options, and you could find what they mean in [Tool:fastq-dump](https://ncbi.github.io/sra-tools/fastq-dump.html).

   - **Quality Control**

     - [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) is commonly used for giving quality report for raw sequence data.  It can help ensure that high-quality data are provided to the initial spliced alignment step.

   - **Adapter removal**

     - Here are some tools for running an adapter removal. I uesd [Cutadapt](https://cutadapt.readthedocs.io/en/stable/guide.html) which is one of the most widely used adapter removal program.
     - You can download it using either `pip` or `conda`.
     - For different dataset, it has different **adapter sequence**. For my current dataset, the adpater will be "CTGTCTCTTATA". 
     - Because it is a paired-end sequencing, we must do this thing **twice**.
     - `-a` means the sequence of the adpater. `-o` is the file name of the output if you want to hava a gzip-compressed output file.

     ```
     cutadapt -a CTGTCTCTTATA -o output1.fastq SRR11186388_pass_1.fastq
     cutadapt -a CTGTCTCTTATA -o output2.fastq SRR11186388_pass_2.fastq
     ```

   - **Alignment**

     - This is to align the reads to a reference genome. There are many programs available to perform the alignment as well. And here I chose [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml) (I think it is easy for me to get involved in). 

     - Before you start, you should ensure the reference sequence be indexed. In Bowtie2, index coule be made from a FASTA format genome file by using `bowtie2-build`.  For many orgnisms, the genome and pre-built reference indexes are available in [iGenomes](https://support.illumina.com/sequencing/sequencing_software/igenome.html). So for Drosophila melanogaster, **dm6.fa** is used as the index files here.

       ```
       bowtie2-build  <genome.fa>  <genomeIndexName>
       e.g. bowtie2-build  dm6.fa dm6
       ```

     - Once the indexed are built, the reads could be aligned. 

       `--very-sensitive` : To get the alignment results better.

       `-k` : Maximum number of alignments to report per read.

       `-x` : The basement of the index for the reference genome.

       ```
       bowtie2  --very-sensitive  -k 10  -x <genomeIndexName>  -1 <name>_1.fastq.gz  -2 <name>_2.fastq.gz
       e.g. bowtie2  --very-sensitive  -k 10  -x dm6 -1 ./48hr_rep1/output1.fastq -2 ./48hr_rep1/output2.fastq
       ```

     - It is noteworthy to know the output file will be **SAM** file, containing alignment information for each input read. The size of this kind of file is very large. Thus we should convert it into a binary format(**BAM**) and sorted by queryname. [SAMtools](http://www.htslib.org/doc/samtools.html) is a tool to deal with this kind issues. 

       ```
       bowtie2  --very-sensitive  -k 10  -x dm6 -1 ./48hr_rep1/output1.fastq -2 ./48hr_rep1/output2.fastq  
       | samtools sort  -n  -o ./48hr_rep1/output.bam
       ```

   - **Peak-calling**

     The document recommends us to call peaks with [Genrich](https://github.com/jsh58/Genrich). It was designed to be able to run all of the post-alignment steps through peak-calling with one-command. So it is very convenient. 

     `-j` : ATAC-seq mode (**must** be specified)

     `-y` : Analyze unpaireded alignments

     `-r` : remove PCR duplicates

     `-e` : Chromosomes to exclude

     `-v` : verbose mode

     ```
     Genrich  -t output.bam  -o sample.narrowPeak  -j  -y  -r  -e chrM  -v
     ```

     - For learnning more details about **narrowPeak** files, please get into this link: [Data File Formats](https://genome.ucsc.edu/FAQ/FAQformat.html#format12)

2. **Extract information** we need from each narrowPeak files.  [Extract_Data.py]

   - To have a better visualization, I converted each **narrowPeak** file into an another new file with **csv** format.  I used 4 keys: 

     - `chrom`(Name of the chromosome)
     - `chromstart`(The starting position of the feature)
     - `chromend`(The ending position of the feature)
     - `singleValue`(Measurement of overall enrichment for the region)

     In particular, I **removed** some chromosome information which *the length of their name larger thatn 7*. For drosophila, I just want to focus on the chromosome like "ChrX" and "ChrY". Others like "ChrY_DS485888v1_random", the name of this kind of chromosome are very complex. They are likely not be relevant to our topic, I filtered these out. 

   - Also, I calculatded the **median position** of each region. It is to simplify the step to make a plot. I could use the medium point instead of th whole region, and make a figure to show the relationship between **positions** and their **peak** values. 

   - There are **three** replicate files and **two** time slots, so I plot some figures to show above relationship and comparision between different time slots in different replicates and different chromosomes.

3. Find the **ranges**(start,end) in ATAC-seq data that is **common** to all replicates. [Find_common.py]

   What we know is that ATAC-seq data requires that biological replicates run. This could *ensure that any signals observed are due to biological effects and not idiosyncracies of one particular sample or its processing*.  So here we could find **the common regions** and consider it as the final info that we get.

4. Once we get the common regions, we just focus on these positions. So we want to go back and **find their signalvalue**. [Get_peakvalue.py]

5. 

6. How to check if we find the promoter or not? We need the **promoter information**: [the *Drosophila melanogaster* (fruit fly) curated promoter database](https://epd.epfl.ch/drosophila/drosophila_database.php?db=drosophila). I extracted the region of each possible promoter and convert this data into dictionary in Python, which could be easily access to get. [getpromoter.py]

7. 

   



## Possible steps:

Deal with the RNA-seq Data. 

TBD





## Reference:

1. [ATAC-seq Guidelines](https://informatics.fas.harvard.edu/atac-seq-guidelines.html)
2. [SRA handbook](https://www.ncbi.nlm.nih.gov/books/NBK242621/)
3. 

