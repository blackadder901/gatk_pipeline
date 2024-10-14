from run_gatk_tasks import *
from run_gatk_extras import *
from prefect import flow
from prefect.task_runners import ThreadPoolTaskRunner
import os

#------------------------------------------------------------------------
#Function for looking into the quality of the reads.
#The FASTQC tool is being used.
#Input: Paired raw reads  (*_1.fastq.gz)-(*_2.fastq.gz)-- Output: *.html and *.zip files
#This prefect flow initially checks if the output directory in present and if not it creates it. Moreover, it checks if the output files already exist by calling the function remove_extension, then by defining the correct expected output files and finaly by checking if the .html and .zip files exist. If the files do not exist, it proceeds with running the FASTQC tool.
@flow
def run_fastqc(fastq_1, fastq_2):

    #Check if output dir exists and if not, create it
    fastqc_output_dir="fastqc_results"
    if not os.path.exists(fastqc_output_dir):
        os.makedirs(fastqc_output_dir)
        logging.info(f"Directory for FASTQC results, created.")

    #Remove file extensions
    fastq_1_base=remove_extension(fastq_1)
    fastq_2_base=remove_extension(fastq_2)

    #Define expected output files for FASTQC
    fastq_1_zip=os.path.join(fastqc_output_dir, f"{fastq_1_base}_fastqc.zip")
    fastq_1_html=os.path.join(fastqc_output_dir, f"{fastq_1_base}_fastqc.html")
    
    fastq_2_zip=os.path.join(fastqc_output_dir, f"{fastq_2_base}_fastqc.zip")
    fastq_2_html=os.path.join(fastqc_output_dir, f"{fastq_2_base}_fastqc.html")

    #Check if FASTQC output files already exist
    if all(os.path.exists(f) for f in [fastq_1_zip, fastq_1_html, fastq_2_zip, fastq_2_html]):
        logging.info (f"------------------FASTQC quality check-----------------")
        logging.info(f"FASTQC output files for {fastq_1} and {fastq_2} already exist. Skipping FASTQC analysis.")
    else:
        fastqc_command=["fastqc", fastq_1, fastq_2, "-o", str(fastqc_output_dir)]
        run_subprocess(fastqc_command, tool="FASTQC")

#------------------------------------------------------------------------
#Function for aligning the paired reads with a reference genome.
#The Bwa mem tool is being used.
#Input: Paired raw reads, reference genome (*.fasta) -- Output: *.SAM, *.BAM, *_sorted.BAM
#This prefect flow initially checks if the the .SAM output file is present. If not, it proceeds with running the bwa mem alignment. Moreover, it calls 2 external tasks (convert_sam_to_bam and sort_bam to perfom some basic operations to the alignment output files. Both of these 2 functions only run if the correct output files are not present) 
@flow
def run_bwa(fastq_1, fastq_2, ref_genome, threads, out_sam="gatk_pipeline.sam", bam="gatk_pipeline.bam", bam_sorted="gatk_pipeline_sorted.bam"):

    #Run Bwa mem
    if os.path.exists(out_sam):
        logging.info (f"------------------BWA mem alignment-----------------")
        logging.info(f"Output SAM file '{out_sam}' already exists. Skipping the BWA alignment process.")
    else:
        read_group_info = '@RG\\tID:gatk_exercise\\tSM:NA12878\\tLB:lib1\\tPL:ILLUMINA\\tPU:unit1'
        bwa_command = ["bwa", "mem", "-t", str(threads), "-R", read_group_info, ref_genome, fastq_1, fastq_2]
        
        run_subprocess_out_file(bwa_command, out_sam, tool="BWA mem", out_name="bwa_output")

    #Convert SAM to BAM
    if os.path.exists(bam):
        logging.info (f"------------------SAM to BAM analysis-----------------")
        logging.info(f"Output BAM file '{bam}' already exists. Skipping the BAM conversion process.")
    else:
        convert_sam_to_bam(out_sam, bam)

    #Sort BAM
    if os.path.exists(bam_sorted):
        logging.info (f"------------------Samtools sort analysis-----------------")
        logging.info(f"Output sorted BAM file '{bam_sorted}' already exists. Skipping the BAM sorting process.")
    else:
        sort_bam(bam, bam_sorted)

#------------------------------------------------------------------------
#Function for calling variants.
#The GATK HaplotypeCaller tool is being used.
#Input: reference genome (*.fasta), sorted BAM (*.sorted.BAM) -- Output: *.fai, *.dict, *.bam.bai, *.vcf
#This prefect flow initially perfomr some basic operations in order for GATK HaplotypeCaller to run. It runs the following functions only if the correct associated output files are not there: index_reference, dict_reference, index_bam. Then it proceeds with running the GATK HaplotypeCaller
@flow(task_runner=ThreadPoolTaskRunner())
def run_HaplotypeCaller(ref_genome, out_vcf, bam_sorted="gatk_pipeline_sorted.bam", reference_genome_index="data/Homo_sapiens_assembly38.fasta.fai", reference_genome_dict="data/Homo_sapiens_assembly38.dict", bam_index="gatk_pipeline_sorted.bam.bai"):

    #Run Samtools faidx for indexing the reference genome
    if os.path.exists(reference_genome_index):
        logging.info (f"------------------Samtools faidx Analysis-----------------")
        logging.info(f"Output reference index file '{reference_genome_index}' already exists. Skipping the reference indexing process.")
        index_ref_res=None
    else:
        index_ref_res=index_reference.submit(ref_genome, reference_genome_index)
    
    #Run Samtools dict for creating a .dict file for the reference genome
    if os.path.exists(reference_genome_dict):
        logging.info (f"------------------Samtools Dict-----------------")
        logging.info(f"Output reference dict file '{reference_genome_dict}' already exists. Skipping the reference dict process.")
        dict_ref_res=None
    else:
        dict_ref_res=dict_reference.submit(ref_genome, reference_genome_dict)
    
    #Run Sammtols index for indexing the .BAM file
    if os.path.exists(bam_index):
        logging.info (f"------------------SAMTOOLS index Analysis-----------------")
        logging.info(f"Output bam index file '{bam_index}' already exists. Skipping the BAM indexing process.")
        index_bam_res=None
    else:
        index_bam_res=index_bam.submit(bam_sorted, bam_index)

    if index_ref_res:
        index_ref_res.result()

    if dict_ref_res:
        dict_ref_res.result()

    if index_bam_res:
        index_bam_res.result()

    #Run GATK HaplotypeCaller for variant call analysis
    if os.path.exists(out_vcf) and os.path.getsize(out_vcf) > 0:
        logging.info (f"------------------GATK HaplotypeCaller Analysis-----------------")
        logging.info(f"Output vcf file '{out_vcf}' already exists. Skipping the variant calling process.")
    else:
        haplotypecaller_command=["gatk", "HaplotypeCaller", "-R", ref_genome, "-I", bam_sorted, "-O", out_vcf]

        run_subprocess_out_file(haplotypecaller_command, out_vcf, tool="GATK HaplotypeCaller", out_name="haplo_output")