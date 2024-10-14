import unittest
from unittest.mock import patch
from run_gatk_pipe import *

#------------------------------------------------------------------------
#Tests for run_gatk_extras.py
#------------------------------------------------------------------------
class test_tasks(unittest.TestCase):
    #Test for convert_sam_to_bam
    #Using patch to mock if the convert_sam_to_bam function constructs the correct command and parameters when called
    @patch("run_gatk_tasks.run_subprocess_out_file")
    def test_convert_sam_to_bam(self, mock_run_subprocess_out_file):
        
        sam_file="input.sam"
        out_bam="output.bam"
        
        convert_sam_to_bam(sam_file, out_bam)

        mock_run_subprocess_out_file.assert_called_once_with(
            ["samtools", "view", "-bS", sam_file],
            out_bam,
            tool="Samtools view",
            out_name="bam_output")

    #Test for sort_bam
    #Using patch to mock if sort_BAM function constructs the correct command and parameters when called
    @patch("run_gatk_tasks.run_subprocess_out_file")
    def test_sort_bam(self, mock_run_subprocess_out_file):
        
        bam_file="input.bam"
        out_sorted_bam_file="sorted_output.bam"
        
        sort_bam(bam_file, out_sorted_bam_file)

        mock_run_subprocess_out_file.assert_called_once_with(
            ["samtools", "sort", bam_file],
            out_sorted_bam_file,
            tool="Samtools sort",
            out_name="sorted_bam_output")

    #Test for index_reference
    #Using patch to mock if index_reference function constructs the correct command and parameters when called
    @patch("run_gatk_tasks.run_subprocess_out_file")
    def test_index_reference(self, mock_run_subprocess_out_file):
        
        reference_genome="reference.fasta"
        out_reference_genome_index="reference.fasta.fai"
        
        index_reference(reference_genome, out_reference_genome_index)

        mock_run_subprocess_out_file.assert_called_once_with(
            ["samtools", "faidx", reference_genome],
            out_reference_genome_index,
            tool="Samtools faidx",
            out_name="ref_index")

    #Test for dict_reference
    #Using patch to mock if the dictionary file is already present
    @patch("run_gatk_tasks.os.path.exists")
    @patch("run_gatk_tasks.os.path.getsize")
    @patch("run_gatk_tasks.run_subprocess_out_file")
    def test_dict_reference_file_exists(self, mock_run_subprocess_out_file, mock_getsize, mock_exists):

        reference_genome="reference.fasta"
        reference_genome_dict="reference.dict"

        mock_exists.return_value=True
        mock_getsize.return_value=100
        
        dict_reference(reference_genome, reference_genome_dict)

        mock_run_subprocess_out_file.assert_not_called()

    #Test for dict_reference
    #Using patch to mock if dict_reference function constructs the correct command and parameters when called
    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("run_gatk_extras.run_subprocess_out_file")
    def test_dict_reference_create_dict(self, mock_run_subprocess_out_file, mock_getsize, mock_exists):

        reference_genome="reference.fasta"
        reference_genome_dict="reference.dict"

        mock_exists.return_value=False
        mock_getsize.return_value=0

        dict_reference(reference_genome, reference_genome_dict)

        mock_run_subprocess_out_file.assert_not_called()

    #Test for index_bam
    #Using patch to mock if index_bam function constructs the correct command and parameters when called
    @patch("run_gatk_extras.run_subprocess_out_file")
    def test_index_bam(self, mock_run_subprocess_out_file):

        bam_sorted="sorted.bam"
        out_index_bam_file="sorted.bam.bai"
        
        index_bam(bam_sorted, out_index_bam_file)

        mock_run_subprocess_out_file.assert_not_called()

if __name__ == "__main__":
    unittest.main()