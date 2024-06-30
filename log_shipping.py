import logging
import subprocess
import os
import sys
from datetime import datetime
from config import BACKUP_DIR, DB_CONFIG, LOG_FILE
from utils import setup_logging, write_error_report

ERROR_REPORT_FILE = 'logs/error_report.txt'

BACKUP_DIR = os.path.abspath(BACKUP_DIR)
SECONDARY_BACKUP_DIR = os.path.join(BACKUP_DIR, 'secondary')

if not os.path.exists(SECONDARY_BACKUP_DIR):
    os.makedirs(SECONDARY_BACKUP_DIR)

def run_sqlcmd(command):
    try:
        setup_logging(LOG_FILE)
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(e.stdout)
        print(e.stderr)
        logging.error(str(e))
        write_error_report(str(e), ERROR_REPORT_FILE)
        return False

def backup_transaction_log(db_config_primary, secondary_backup_dir):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(secondary_backup_dir, f'translog_{timestamp}.bak')
    dump_command = (
        f"sqlcmd -S {db_config_primary['host']} -U {db_config_primary['user']} "
        f"-P {db_config_primary['password']} -d {db_config_primary['database']} "
        f"-Q \"BACKUP LOG [{db_config_primary['database']}] TO DISK = '{backup_file}' WITH INIT\""
    )
    if run_sqlcmd(dump_command):
        print(f"Transaction log backup successful: {backup_file}")
        return backup_file
    else:
        print(f"Transaction log backup failed.")
        return None

def restore_log_on_secondary(db_config_secondary, log_file):
    restore_command = (
        f"sqlcmd -S {db_config_secondary['host']} -U {db_config_secondary['user']} "
        f"-P {db_config_secondary['password']} "
        f"-Q \"RESTORE LOG [{db_config_secondary['database']}] FROM DISK = '{log_file}' WITH NORECOVERY\""
    )
    print(f"Running restore command: {restore_command}")
    if run_sqlcmd(restore_command):
        print(f"Log file restored successfully on secondary server: {log_file}")
    else:
        print(f"Failed to restore log file.")

def recovery_secondary(db_config_secondary):
    recovery_command = (
        f"sqlcmd -S {db_config_secondary['host']} -U {db_config_secondary['user']} "
        f"-P {db_config_secondary['password']} "
        f"-Q \"RESTORE DATABASE [{db_config_secondary['database']}] WITH RECOVERY\""
    )
    print(f"Running recovery command: {recovery_command}")
    if run_sqlcmd(recovery_command):
        print(f"Database recovered successfully on secondary server.")
    else:
        print(f"Failed to recover database.")

def full_backup_primary(db_config_primary, secondary_backup_dir):
    backup_file = os.path.join(secondary_backup_dir, 'full_backup.bak')
    dump_command = (
        f"sqlcmd -S {db_config_primary['host']} -U {db_config_primary['user']} "
        f"-P {db_config_primary['password']} "
        f"-Q \"BACKUP DATABASE [{db_config_primary['database']}] TO DISK = '{backup_file}' WITH INIT\""
    )
    if run_sqlcmd(dump_command):
        print(f"Full backup successful: {backup_file}")
        return backup_file
    else:
        print(f"Full backup failed.")
        return None

def restore_full_on_secondary(db_config_secondary, backup_file, secondary_backup_dir):
    mdf_path = os.path.join(secondary_backup_dir, f"{db_config_secondary['database']}.mdf")
    ldf_path = os.path.join(secondary_backup_dir, f"{db_config_secondary['database']}_log.ldf")
    
    restore_command = (
        f"sqlcmd -S {db_config_secondary['host']} -U {db_config_secondary['user']} "
        f"-P {db_config_secondary['password']} "
        f"-Q \"RESTORE DATABASE [{db_config_secondary['database']}] FROM DISK = '{backup_file}' "
        f"WITH MOVE 'test1' TO '{mdf_path}', MOVE 'test1_log' TO '{ldf_path}', NORECOVERY\""
    )
    print(f"Running restore command: {restore_command}")
    if run_sqlcmd(restore_command):
        print(f"Full backup restored successfully on secondary server: {backup_file}")
    else:
        print(f"Failed to restore full backup.")

def drop_database_secondary(db_config_secondary):
    drop_db_command = (
        f"sqlcmd -S {db_config_secondary['host']} -U {db_config_secondary['user']} "
        f"-P {db_config_secondary['password']} "
        f"-Q \"IF EXISTS (SELECT name FROM sys.databases WHERE name = '{db_config_secondary['database']}') "
        f"DROP DATABASE [{db_config_secondary['database']}]\""
    )
    print(f"Running drop database command: {drop_db_command}")
    if run_sqlcmd(drop_db_command):
        print(f"Database dropped successfully on secondary server.")
    else:
        print(f"Failed to drop database on secondary server.")

def main(db_name_primary, db_name_secondary):
    db_config_primary = {
        'driver': DB_CONFIG['driver'],
        'host': DB_CONFIG['server'],
        'user': DB_CONFIG['user'],
        'password': DB_CONFIG['password'],
        'database': db_name_primary
    }

    db_config_secondary = {
        'driver': DB_CONFIG['driver'],
        'host': 'localhost',  # Sesuaikan dengan host secondary server
        'user': DB_CONFIG['user'],
        'password': DB_CONFIG['password'],
        'database': db_name_secondary  # Sesuaikan dengan nama database secondary
    }
    

    drop_database_secondary(db_config_secondary)
    
    full_backup_file = full_backup_primary(db_config_primary, SECONDARY_BACKUP_DIR)
    if full_backup_file:
        restore_full_on_secondary(db_config_secondary, full_backup_file, SECONDARY_BACKUP_DIR)
    
    log_file = backup_transaction_log(db_config_primary, SECONDARY_BACKUP_DIR)
    if log_file:
        restore_log_on_secondary(db_config_secondary, log_file)
    
    recovery_secondary(db_config_secondary)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python log_shipping.py <primary_db_name> <secondary_db_name>")
        sys.exit(1)
    
    db_name_primary = sys.argv[1]
    db_name_secondary = sys.argv[2]
    main(db_name_primary, db_name_secondary)