import logging
import os

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(message)s')

def write_error_report(error_message, report_file):
    with open(report_file, 'a') as f:
        f.write(error_message + '\n')

def run_shell_command(command):
    result = os.system(command)
    if result != 0:
        raise Exception(f"Command failed: {command}")