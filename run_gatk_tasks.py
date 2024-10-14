from run_gatk_extras import *
from prefect import task
import os

#------------------------------------------------------------------------
#Function for converting SAM file to BAM file.
#Input=SAM -- Output=BAM
#This task is used by run_bwa flow
@task
def convert_sam_to_bam(sam_file, out_bam):
    samtools_command=["samtools", "view", "-bS", sam_file]
    
    run_subprocess_out_file(samtools_command, out_bam, tool="Samtools view", out_name="bam_output")

#------------------------------------------------------------------------
#Function for sorting BAM file
#Input: BAM -- Output: Sorted BAM
#This task is used by run_bwa flow
@task
def sort_bam(bam_file, out_sorted_bam_file):
    samtools_sort_bam=["samtools", "sort", bam_file]

    run_subprocess_out_file(samtools_sort_bam, out_sorted_bam_file, tool="Samtools sort", out_name="sorted_bam_output")

#------------------------------------------------------------------------
#Function for indexing the reference genome fasta file
#Input: Reference genome fasta file -- Output: Indexed reference genome fasta file
#This task is used by run_HaplotypeCaller flow
@task
def index_reference(reference_genome, out_reference_genome_index):
    samtools_faidx=["samtools", "faidx", reference_genome]

    run_subprocess_out_file(samtools_faidx, out_reference_genome_index, tool="Samtools faidx", out_name="ref_index")

#------------------------------------------------------------------------
#Function for creating a dictionary file for the reference genome file
#Input: Reference genome fasta file -- Output: Reference genome fasta dictionary file
#This task is used by run_HaplotypeCaller flow
@task
def dict_reference(reference_genome, reference_genome_dict):
    ref_dict="data/Homo_sapiens_assembly38.dict"

    if os.path.exists(ref_dict) and os.path.getsize(ref_dict) > 0:
        logging.info(f"The Dict file already exists and is not empty.")
        logging.info (f"------------------Creating FASTA dict analysis ends-----------------")
        return
    samtools_dict=["samtools", "dict", reference_genome]

    run_subprocess_out_file(samtools_dict, reference_genome_dict, tool="Samtools dict", out_name="ref_dict")

#------------------------------------------------------------------------
#Function for indexing the sorted BAM file
#Input: Sorted BAM file -- Output: Indexed sorted BAM file
#This task is used by run_HaplotypeCaller flow
@task
def index_bam(bam_sorted, out_index_bam_file):     
    samtools_index=["samtools", "index", bam_sorted]

    run_subprocess_out_file(samtools_index, out_index_bam_file, tool="Samtools index", out_name="bam_index")