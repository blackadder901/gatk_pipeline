import unittest
from unittest.mock import patch
import os
from run_gatk_pipe import *

#------------------------------------------------------------------------
#Tests for run_gatk_flows.py
#------------------------------------------------------------------------
class test_flows(unittest.TestCase):
    #Test for run_fastqc
    #Using patch to mock if the dir exists as well as the creation of the dir in run_gatk_flow.py
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_fastqc_dir_exists(self, mock_exists, mock_makedirs):

        mock_exists.return_value = False

        fastqc_out_dir="fastqc_results"
        if not os.path.exists(fastqc_out_dir):
            os.makedirs(fastqc_out_dir)
        
        mock_exists.assert_called_once_with(fastqc_out_dir)
        mock_makedirs.assert_called_once_with(fastqc_out_dir)
    
    #Test for run_fastqc
    #Using patch to mock if the remove_extension returns correct results in run_gatk_flow.py
    @patch("run_gatk_flows.remove_extension")
    def test_remove_extension(self, mock_remove_extension):

        mock_remove_extension.side_effect = ["sample1"]

        fastq="sample1.fastq.gz"

        removal=mock_remove_extension(fastq)

        mock_remove_extension.assert_any_call(fastq)

        self.assertEqual(removal,("sample1"))
    
    #Test for run_bwa
    #Using patch to mock if run_bwa (run_subprocess_out_file) will run if sam output is already present in run_gatk_flow.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_run_sam_exists(self, mock_run_subprocess_out_file, mock_exists):

        mock_exists.side_effect=lambda x: x == "gatk_pipeline.sam"
        
        run_bwa("sample1.fastq", "sample1.fastq", "ref_genome.fasta", 4)

        mock_run_subprocess_out_file.assert_not_called()

    #Test for run_bwa
    #Using patch to mock if run_bwa (convert_sam_to_bam) will run if bam output is already present in run_gatk_flow.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.convert_sam_to_bam")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_run_bam_exists(self, mock_run_subprocess_out_file, mock_convert_sam_to_bam, mock_exists):
        
        mock_exists.side_effect=lambda x: x == "gatk_pipeline.bam" 
        
        run_bwa("sample1.fastq", "sample1.fastq", "ref_genome.fasta", 4)

        mock_convert_sam_to_bam.assert_not_called()
        mock_run_subprocess_out_file.assert_called_once()

    #Test for run_bwa
    #Using patch to mock if run_bwa (sort_bam) will run if sorted bam output is already present in run_gatk_flow.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.sort_bam")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_run_sorted_bam_exists(self, mock_run_subprocess_out_file, mock_convert_sort_bam, mock_exists):
        
        mock_exists.side_effect=lambda x: x == "gatk_pipeline_sorted.bam"  # BAM and SAM files exist
        
        run_bwa("file1.fastq", "file2.fastq", "ref_genome.fasta", 4)

        mock_convert_sort_bam.assert_not_called()
        mock_run_subprocess_out_file.assert_called_once()

    #Test for run_HaplotypeCaller
    # Using patch to mock if the run_HaplotypeCaller (run_subprocess_out_file) will run if output vcf file is already present in run_gatk_flows.py
    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_run_haplotype_caller_not_called_if_vcf_exists_and_non_empty(self, mock_run_subprocess_out_file, mock_getsize, mock_exists):
    
        mock_exists.side_effect = lambda x: "output_vcf" in x
        mock_getsize.side_effect = lambda x: 100 

        run_HaplotypeCaller("ref_genome.fasta", "output_vcf")

        mock_run_subprocess_out_file.assert_not_called()

    #Test for run_HaplotypeCaller
    #Using patch to mock if the run_HaplotypeCaller (index_reference) will run if the ref index file is already present in run_gatk_flows.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.index_reference")  # Change "your_module" to the actual module name
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_index_reference_exists(self, mock_run_subprocess_out_file, mock_index_reference, mock_exists):
    
        mock_exists.side_effect=lambda x: x == "data/Homo_sapiens_assembly38.fasta.fai"
        
        run_HaplotypeCaller("ref_genome.fasta", "output_vcf")

        mock_index_reference.assert_not_called()
        mock_run_subprocess_out_file.assert_called_once()
    
    #Test for run_HaplotypeCaller
    #Using patch to mock if the run_HaplotypeCaller (dict_reference) will run if the dict file is already present in run_gatk_flows.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.dict_reference")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_dict_reference_exists(self, mock_run_subprocess_out_file, mock_dict_reference, mock_exists):

        mock_exists.side_effect=lambda x: x == "data/Homo_sapiens_assembly38.dict"
        
        run_HaplotypeCaller("ref_genome.fasta", "output_vcf")

        mock_dict_reference.assert_not_called()
        mock_run_subprocess_out_file.assert_called_once()
    
    #Test for run_HaplotypeCaller
    # Using patch to mock if the run_HaplotypeCaller (index_bam) will run if the index BAM file is already present in run_gatk_flows.py
    @patch("os.path.exists")
    @patch("run_gatk_flows.index_bam")
    @patch("run_gatk_flows.run_subprocess_out_file")
    def test_index_bam_exists(self, mock_run_subprocess_out_file, mock_index_bam_reference, mock_exists):
    
        mock_exists.side_effect=lambda x: x == "data/Homo_sapiens_assembly38.dict"
        
        run_HaplotypeCaller("ref_genome.fasta", "output_vcf")

        mock_index_bam_reference.assert_not_called()
        mock_run_subprocess_out_file.assert_called_once()

    
    
if __name__ == "__main__":
    unittest.main()

