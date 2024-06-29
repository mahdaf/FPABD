import argparse
import os
import logging
import pyodbc
from config import DB_CONFIG, BACKUP_DIR, LOG_FILE
from utils import setup_logging, write_error_report
import time
import sys

ERROR_REPORT_FILE = 'logs/error_report.txt'
LAST_BACKUP_TIME_FILE = 'logs/last_backup_time.txt'

BACKUP_DIR = os.path.abspath(BACKUP_DIR)

def backup_full():
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        timestamp = int(time.time())
        filename = os.path.join(BACKUP_DIR, f"{db_name}_full_backup_{timestamp}.bak")
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP DATABASE [{db_name}] TO DISK='{filename}'\""
        
        os.system(command)
        logging.info(f"Full backup successful: {filename}")
        print(f"Full backup successful: {filename}")
        update_last_backup_time(timestamp)
    except Exception as e:
        error_message = f"Full backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

def backup_translog():
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        timestamp = int(time.time())
        translog_filename = os.path.join(BACKUP_DIR, f"translog_{timestamp}.trn")
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP LOG [{db_name}] TO DISK='{translog_filename}'\""
        
        os.system(command)
        logging.info(f"Transaction log backup successful: {translog_filename}")
        print(f"Transaction log backup successful: {translog_filename}")
    except Exception as e:
        error_message = f"Transaction log backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

def backup_diff():
    try:
        setup_logging(LOG_FILE)
        db_name = DB_CONFIG['database']
        timestamp = int(time.time())
        diff_filename = os.path.join(BACKUP_DIR, f"{db_name}_diff_backup_{timestamp}.bak")
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"BACKUP DATABASE [{db_name}] TO DISK='{diff_filename}' WITH DIFFERENTIAL\""
        
        os.system(command)
        logging.info(f"Differential backup successful: {diff_filename}")
        print(f"Differential backup successful: {diff_filename}")
        update_last_backup_time(timestamp)
    except Exception as e:
        error_message = f"Differential backup failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

def get_last_backup_time():
    try:
        with open(LAST_BACKUP_TIME_FILE, 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def update_last_backup_time(timestamp):
    with open(LAST_BACKUP_TIME_FILE, 'w') as file:
        file.write(str(timestamp))

def auto_diff_backup(interval):
    try:
        setup_logging(LOG_FILE)
        while True:
            backup_diff()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nDifferential backup process interrupted. Exiting...")
    except Exception as e:
        error_message = f"Unexpected error occurred: {str(e)}"
        logging.error(error_message)
        print(error_message)

def main(full_backup_interval, diff_backup_interval, translog_backup_interval):
    try:
        last_full_backup_time = get_last_backup_time()
        last_diff_backup_time = last_full_backup_time
        
        while True:
            current_time = int(time.time())
            
            # Full Backup
            if current_time - last_full_backup_time >= full_backup_interval:
                backup_full()
                last_full_backup_time = current_time
                last_diff_backup_time = current_time
            
            # Differential Backup
            elif current_time - last_diff_backup_time >= diff_backup_interval:
                backup_diff()
                last_diff_backup_time = current_time
            
            # Transaction Log Backup
            else:
                backup_translog()
            
            time.sleep(translog_backup_interval)
    except KeyboardInterrupt:
        print("\nBackup process interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        error_message = f"Unexpected error occurred: {str(e)}"
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automated Database Backup')
    parser.add_argument('full_backup_interval', type=int, nargs='?', help='Interval in seconds for full backups')
    parser.add_argument('diff_backup_interval', type=int, nargs='?', help='Interval in seconds for differential backups')
    parser.add_argument('translog_backup_interval', type=int, nargs='?', help='Interval in seconds for transaction log backups')
    parser.add_argument('--diff', type=int, help='Run differential backup only with specified interval')
    args = parser.parse_args()

    if args.diff:
        auto_diff_backup(args.diff)
    else:
        if args.full_backup_interval is None or args.diff_backup_interval is None or args.translog_backup_interval is None:
            parser.error("the following arguments are required: full_backup_interval, diff_backup_interval, translog_backup_interval")
        main(args.full_backup_interval, args.diff_backup_interval, args.translog_backup_interval)
