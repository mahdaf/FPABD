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

def backup_full():
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        timestamp = time.strftime('%d%m%Y%H%M%S')
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

def backup_diff():
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        last_full_backup_time = get_last_full_backup_time()
        if not last_full_backup_time:
            print("No previous full backup found. Performing full backup instead.")
            backup_full()
            return
        
        # Backup differential
        timestamp = time.strftime('%d%m%Y%H%M%S')
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

def backup_translog():
    try:
        setup_logging(LOG_FILE)
        
        conn = pyodbc.connect(
            f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['user']};PWD={DB_CONFIG['password']};TrustServerCertificate=yes"
        )
        cursor = conn.cursor()
        
        timestamp = time.strftime('%d%m%Y%H%M%S')
        translog_filename = os.path.join(BACKUP_DIR, f"translog_{timestamp}.trn")
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP LOG [{DB_CONFIG['database']}] TO DISK='{translog_filename}'\""
        os.system(command)
        
        logging.info(f"Transaction log backup successful: {translog_filename}")
        print(f"Transaction log backup successful: {translog_filename}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        error_message = f"Transaction log backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

def get_last_full_backup_time():
    try:
        with open(LAST_FULL_BACKUP_TIME_FILE, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        logging.warning(f"Last full backup time file not found: {LAST_FULL_BACKUP_TIME_FILE}")
        return None
    except Exception as e:
        logging.error(f"Error reading last full backup time file {LAST_FULL_BACKUP_TIME_FILE}: {str(e)}")
        return None

def update_last_full_backup_time(timestamp):
    try:
        with open(LAST_FULL_BACKUP_TIME_FILE, 'w') as file:
            file.write(str(timestamp))
    except Exception as e:
        logging.error(f"Error writing last full backup time file {LAST_FULL_BACKUP_TIME_FILE}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Database Backup CLI')
    parser.add_argument('type', choices=['full', 'diff', 'translog'], help='Type of backup to perform')
    args = parser.parse_args()

    if args.type == 'full':
        backup_full()
    elif args.type == 'diff':
        backup_diff()
    elif args.type == 'translog':
        backup_translog()

if __name__ == "__main__":
    main()