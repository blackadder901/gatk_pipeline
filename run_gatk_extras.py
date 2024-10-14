import subprocess
import logging
import os

#------------------------------------------------------------------------
#Function for handling the subprocess operations.
#This function executes a subprocess command and logs the analysis progress
def run_subprocess(command, tool):
    try:
        logging.info(f"------------------{tool} analysis starts-----------------")
        subprocess.run(command, check=True)
        logging.info(f"{tool} completed successfully")
        logging.info(f"------------------{tool} analysis ends-----------------")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}. Error code: {e.returncode}")
        return False
    except FileNotFoundError:
        logging.error(f"Tool not found for command: {command}")
        return False

#------------------------------------------------------------------------
#Function for handling the subprocess operations.
#This function executes a subprocess command that has to return an output file and logs the analysis progress
def run_subprocess_out_file(command, out_file, tool, out_name):
    with open(out_file, "w") as out_name:
        try:
            logging.info(f"------------------{tool} analysis starts-----------------")
            subprocess.run(command, stdout=out_name, check=True)
            logging.info(f"{tool} completed successfully")
            logging.info(f"------------------{tool} analysis ends-----------------")
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {command}. Error code: {e.returncode}")
            return False
        except FileNotFoundError:
            logging.error(f"Tool not found for command: {command}")
            return False

#------------------------------------------------------------------------
#Function for removing the extension in either .fastq.gz or .fq.gz files
def remove_extension(filename):
    base=os.path.basename(filename)
    if base.endswith(".fastq.gz"):
        return base[:-9]
