import unittest
from unittest.mock import patch
import argparse
import os
from run_gatk_pipe import *

#------------------------------------------------------------------------
#Tests for run_gatk_pipe.py
#------------------------------------------------------------------------
#Using patch to mock the external main functions from run_gatk_pipe.py as well as argument parser
class test_pipe(unittest.TestCase):
    @patch("run_gatk_pipe.run_HaplotypeCaller")
    @patch("run_gatk_pipe.run_bwa")
    @patch("run_gatk_pipe.run_fastqc")
    @patch("argparse.ArgumentParser.parse_args")
    def test_gatk_pipe(self, mock_parse_args, mock_run_fastqc, mock_run_bwa, mock_run_haplotypecaller):
        
        mock_parse_args.return_value = argparse.Namespace(
            fastq1="sample1.fastq",
            fastq2="sample2.fastq",
            ref_genome="reference.fasta",
            out_vcf="output.vcf",
            threads=4
        )

        gatk()

        mock_run_fastqc.assert_called_once_with("sample1.fastq", "sample2.fastq")
        mock_run_bwa.assert_called_once_with("sample1.fastq", "sample2.fastq", "reference.fasta", 4)
        mock_run_haplotypecaller.assert_called_once_with("reference.fasta", "output.vcf")

if __name__ == '__main__':
    unittest.main()
