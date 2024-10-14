# GATK Pipeline
A secondary analysis pipeline that calls single nucleotide variants (SNVs) and insertions/deletions (InDels).

## Introduction

This tool is a newly developed Prefect workflow that has as main task the detection of SNVs and InDels in a given dataset. It initially performs QC on the input dataset (in this case, paired-end reads) and then proceeds with aligning the reads to the human reference genome.

The pipeline uses the following tools:

* [``` FASTQC ```](https://github.com/s-andrews/FastQC): a tool for spotting potential problems in high throughput sequencing datasets.
* [``` bwa ```](https://github.com/lh3/bwa): a software package for mapping DNA sequences against a large reference genome.
* [``` Samtools ```](https://github.com/samtools/): a set of tools for manipulating next-generation sequencing data. 
* [``` GATK ```](https://github.com/broadinstitute/gatk): a tool for identifying SNPs and InDels in germline DNA and RNAseq data.

Apart from the aforementioned tools, the pipeline uses the:

* [``` Prefect ```](https://www.prefect.io/): a powerful and open-source workflow orchestration tool that lets users design, monitor, and respond to data and machine learning pipelines using Python code.

## Data
The user needs to download the [``` Homo_sapiens assembly38```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta;tab=live_object) reference genome, which can be found in the GATK Resource Bundle. This file should be placed in the data directory.

Moreover, the user is required to download the following necessary files:

* [``` .amb ```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.64.amb;tab=live_object)
* [``` .ann ```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.64.ann;tab=live_object)
* [``` .bwt ```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.64.bwt;tab=live_object)
* [``` .pac ```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.64.pac;tab=live_object)
* [``` .sa ```](https://console.cloud.google.com/storage/browser/_details/gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.64.sa;tab=live_object)

These files are needed for aligning the paired reads to the reference genomes and they should also be placed in the data directory.

## Installation
The best way to install the pipeline is to clone this GitHub repository. The pipeline uses the Conda package manager to deploy the defined software packages in the specified version without requiring admin or root privileges.

```
git clone https://github.com/blackadder901/gatk_pipeline.git
```
This command will create the gatk_pipeline directory in the current directory.


In order for someone to use this pipeline they will need to install Micromamba, a tiny version of the mamba package manager.

* [``` Micromamba ```](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html): contains all the necessary guidelines for installing the package manager

## Usage

The user initially will have to create the provided environment that contains the software packages needed to run the pipeline. (All the tools are specified in the .env file placed in the env dir)

In order to do that, the user should execute the following command:

```{bash}
micromamba env create --name gatk_pipeline --file env/environment_gatk.yaml
```

Then activate the environment:

```{bash}
micromamba activate gatk_pipeline
```

Furthermore, when the environment has been created and activated, the user can run the pipeline specifying a number of arguments:

GATK pipeline for genomic data analysis. The pipeline calls single nucleotide variants (SNVs) and insertions/deletions (InDels).

### Options:

- `-h`, `--help`            Show this help message and exit.
- `--fastq1 FASTQ1`       Path to the first FASTQ file.
- `--fastq2 FASTQ2`       Path to the second FASTQ file.
- `--ref_genome REF_GENOME`  Path to the reference genome file.
- `--out_vcf OUT_VCF`     Specify the name of the output VCF file.
- `--threads THREADS`     Number of threads to use.

## How to run the pipeline
Prefect provides a variety of options for workflow execution and orchestration. Nevertheless, in this specific example we will execute the pipeline using a local server. So:

1.  ```{bash}
    prefect server start
    ```
    By doing that the user will be able to access the prefect GUI by opening the prefect dashboard link (http://127.0.0.1:"port"). Then open another terminal window activate the gatk_pipeline env again and execute the pipeline by running:
    
2.  ```{bash}
    python3 run_gatk_pipe.py --fastq1 "name_of_first_file" --fastq2 "name_of_second_file" --ref_genome "name_of_ref_genome" --out_vcf "name_of_output_vcf" --threads "number of threads"
    ```



