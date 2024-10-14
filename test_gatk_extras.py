import unittest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
from run_gatk_pipe import *

#------------------------------------------------------------------------
#Tests for run_gatk_extras.py
#------------------------------------------------------------------------
class test_extras(unittest.TestCase):

    #Test for run_subprocess
    #Using patch to mock if the run_subprocess function handles correctly cmd commands
    @patch("run_gatk_extras.subprocess.run")
    def test_run_subprocess_success(self, mock_run):
        mock_run.return_value=MagicMock() 
        result=run_subprocess(["pwd"], "TestTool")
        
        self.assertTrue(result)

    #Test for run_subprocess
    #Using patch to mock if the run_subprocess fails when a subprocess call fails.
    @patch("run_gatk_extras.subprocess.run")
    def test_run_subprocess_error(self, mock_run):
        mock_run.side_effect=subprocess.CalledProcessError(returncode=1, cmd="ls")
        result=run_subprocess(["ls"], "TestTool")
        
        self.assertFalse(result)

    #Test for run_subprocess
    #Using patch to mock if the run_subprocess fails because the user used a run command that does not exist
    @patch("run_gatk_extras.subprocess.run")
    def test_run_subprocess_no_tool_error(self, mock_run):
        mock_run.side_effect=FileNotFoundError
        result=run_subprocess(["ToolDoesNotExist"], "TestTool")
        
        self.assertFalse(result)

    #Test for run_subprocess
    #Using patch to mock if the run_subprocess handles correctly subprocess when dealing with output files
    @patch("run_gatk_extras.subprocess.run")
    @patch("builtins.open", new_callable=mock_open)
    def test_run_subprocess_out_file_error(self, mock_open, mock_run):

        mock_run.side_effect=subprocess.CalledProcessError(returncode=1, cmd="ls")

        result=run_subprocess_out_file(["ls", "-l"], "output.txt", "TestTool", "out_name")

        self.assertFalse(result)

        mock_open.assert_called_once_with("output.txt", "w")
        mock_run.assert_called_once_with(["ls", "-l"], stdout=mock_open(), check=True)

    #Test for run_subprocess
    #Using patch to mock if the run_subprocess works correctly when it encounters a FileNotFoundError error
    @patch("run_gatk_extras.subprocess.run")
    @patch("builtins.open", new_callable=mock_open)
    def test_run_subprocess_file_not_found_error(self, mock_open, mock_run):

        mock_run.side_effect=FileNotFoundError
    
        result=run_subprocess_out_file(["ToolDoesNotExist"], "output.txt", "TestTool", "out_name")
        
        self.assertFalse(result)

        mock_open.assert_called_once_with("output.txt", "w")
        mock_run.assert_called_once_with(["ToolDoesNotExist"], stdout=mock_open(), check=True)

if __name__ == "__main__":
    unittest.main()
