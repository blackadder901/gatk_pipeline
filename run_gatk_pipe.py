from run_gatk_flows import *
from prefect import flow
import argparse
import logging

#Logging config
logging.basicConfig(
    filename="gatk_pipe.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    force=True)

# Initial log message
logging.info("###############################################################")
logging.info("###############################################################")
logging.info("#######################FANCY NEW RUN.##########################")

@flow
def gatk():

    #Initialize the argument parser for command line interface
    parser = argparse.ArgumentParser(description="GATK pipeline for genomic data analysis. The pipeline calls single nucleotide variants (SNVs) and insertions/deletions (InDels)")

    #Define command line arguments
    parser.add_argument("--fastq1", required=True, help="Path to the first FASTQ file.")
    parser.add_argument("--fastq2", required=True, help="Path to the second FASTQ file.")
    parser.add_argument("--ref_genome", required=True, help="Path to the reference genome file.")
    parser.add_argument("--out_vcf", required=True, help="Specify the name the output VCF file.")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use.")
    
    args = parser.parse_args()
    
    #Main operations

    #FASTQC analysis
    run_fastqc(args.fastq1, args.fastq2)
    
    #Bwa mem alignment analysis
    run_bwa(args.fastq1, args.fastq2, args.ref_genome, args.threads)
    
    #GATK HaplotypeCaller analysis
    run_HaplotypeCaller(args.ref_genome, args.out_vcf)


if __name__=="__main__":
    gatk()
    