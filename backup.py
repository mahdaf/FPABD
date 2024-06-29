import argparse
import os
import logging
import pyodbc
import time

from config import DB_CONFIG, BACKUP_DIR, LOG_FILE
from utils import setup_logging, write_error_report

ERROR_REPORT_FILE = 'logs/error_report.txt'
LAST_BACKUP_TIME_FILE = 'logs/last_backup_time.txt'
LAST_FULL_BACKUP_TIME_FILE = 'logs/last_full_backup_time.txt'

BACKUP_DIR = os.path.abspath(BACKUP_DIR)

def backup_full(table_name=None):
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        timestamp = time.strftime('%Y%m%d%H%M%S')
        if table_name:
            filename = os.path.join(BACKUP_DIR, f"{db_name}_{table_name}_full_{timestamp}.bak")
            command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP DATABASE [{db_name}] TO DISK='{filename}'\""
        else:
            filename = os.path.join(BACKUP_DIR, f"{db_name}_full_backup_{timestamp}.bak")
            command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP DATABASE [{db_name}] TO DISK='{filename}'\""
        
        os.system(command)
        logging.info(f"Full backup successful: {filename}")
        print(f"Full backup successful: {filename}")
        update_last_full_backup_time(int(time.time()))
    except Exception as e:
        error_message = f"Full backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

def backup_diff(table_name=None):
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        last_full_backup_time = get_last_full_backup_time()
        if not last_full_backup_time:
            print("No previous full backup found. Performing full backup instead.")
            backup_full()
            return
        
        # Backup differential
        timestamp = time.strftime('%Y%m%d%H%M%S')
        filename = os.path.join(BACKUP_DIR, f"{db_name}_diff_backup_{timestamp}.bak")
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP DATABASE [{db_name}] TO DISK='{filename}' WITH DIFFERENTIAL\""
        
        os.system(command)
        
        logging.info(f"Differential backup successful: {filename}")
        print(f"Differential backup successful: {filename}")
    except Exception as e:
        error_message = f"Differential backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)
