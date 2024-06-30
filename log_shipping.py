import subprocess
import os
from datetime import datetime
from config import BACKUP_DIR, DB_CONFIG

# Konfigurasi database sumber (primary)
DB_CONFIG_PRIMARY = {
    'driver': DB_CONFIG['driver'],
    'host': DB_CONFIG['server'],
    'user': DB_CONFIG['user'],
    'password': DB_CONFIG['password'],
    'database': DB_CONFIG['database']
}

# Konfigurasi database tujuan (secondary)
DB_CONFIG_SECONDARY = {
    'driver': DB_CONFIG['driver'],
    'host': 'localhost',  # Sesuaikan dengan host secondary server Anda
    'user': DB_CONFIG['user'],
    'password': DB_CONFIG['password'],
<<<<<<< HEAD
    'database': 'test50'  # Sesuaikan dengan nama database secondary
=======
    'database': 'test2'  # Sesuaikan dengan nama database secondary
>>>>>>> 75df43ebf77df6d6a89f6ad58b07932703a02018
}

# Direktori untuk menyimpan file backup
BACKUP_DIR = os.path.abspath(BACKUP_DIR)
SECONDARY_BACKUP_DIR = os.path.join(BACKUP_DIR, 'secondary')

# Membuat direktori secondary jika belum ada
if not os.path.exists(SECONDARY_BACKUP_DIR):
    os.makedirs(SECONDARY_BACKUP_DIR)

def run_sqlcmd(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def backup_transaction_log():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(SECONDARY_BACKUP_DIR, f'translog_{timestamp}.bak')
    dump_command = (
        f"sqlcmd -S {DB_CONFIG_PRIMARY['host']} -U {DB_CONFIG_PRIMARY['user']} "
        f"-P {DB_CONFIG_PRIMARY['password']} -d {DB_CONFIG_PRIMARY['database']} "
        f"-Q \"BACKUP LOG [{DB_CONFIG_PRIMARY['database']}] TO DISK = '{backup_file}' WITH INIT\""
    )
    if run_sqlcmd(dump_command):
        print(f"Transaction log backup successful: {backup_file}")
        return backup_file
    else:
        print(f"Transaction log backup failed.")
        return None

def restore_log_on_secondary(log_file):
    restore_command = (
        f"sqlcmd -S {DB_CONFIG_SECONDARY['host']} -U {DB_CONFIG_SECONDARY['user']} "
        f"-P {DB_CONFIG_SECONDARY['password']} "
        f"-Q \"RESTORE LOG [{DB_CONFIG_SECONDARY['database']}] FROM DISK = '{log_file}' WITH NORECOVERY\""
    )
    print(f"Running restore command: {restore_command}")
    if run_sqlcmd(restore_command):
        print(f"Log file restored successfully on secondary server: {log_file}")
    else:
        print(f"Failed to restore log file.")

def recovery_secondary():
    recovery_command = (
        f"sqlcmd -S {DB_CONFIG_SECONDARY['host']} -U {DB_CONFIG_SECONDARY['user']} "
        f"-P {DB_CONFIG_SECONDARY['password']} "
        f"-Q \"RESTORE DATABASE [{DB_CONFIG_SECONDARY['database']}] WITH RECOVERY\""
    )
    print(f"Running recovery command: {recovery_command}")
    if run_sqlcmd(recovery_command):
        print(f"Database recovered successfully on secondary server.")
    else:
        print(f"Failed to recover database.")

def full_backup_primary():
    backup_file = os.path.join(SECONDARY_BACKUP_DIR, 'full_backup.bak')
    dump_command = (
        f"sqlcmd -S {DB_CONFIG_PRIMARY['host']} -U {DB_CONFIG_PRIMARY['user']} "
        f"-P {DB_CONFIG_PRIMARY['password']} "
        f"-Q \"BACKUP DATABASE [{DB_CONFIG_PRIMARY['database']}] TO DISK = '{backup_file}' WITH INIT\""
    )
    if run_sqlcmd(dump_command):
        print(f"Full backup successful: {backup_file}")
        return backup_file
    else:
        print(f"Full backup failed.")
        return None

def restore_full_on_secondary(backup_file):
    # Tentukan lokasi baru untuk file database di server sekunder
<<<<<<< HEAD
    mdf_path = os.path.join(SECONDARY_BACKUP_DIR, 'test50.mdf')
    ldf_path = os.path.join(SECONDARY_BACKUP_DIR, 'test50_log.ldf')
=======
    mdf_path = os.path.join(SECONDARY_BACKUP_DIR, 'test2.mdf')
    ldf_path = os.path.join(SECONDARY_BACKUP_DIR, 'test2_log.ldf')
>>>>>>> 75df43ebf77df6d6a89f6ad58b07932703a02018
    
    restore_command = (
        f"sqlcmd -S {DB_CONFIG_SECONDARY['host']} -U {DB_CONFIG_SECONDARY['user']} "
        f"-P {DB_CONFIG_SECONDARY['password']} "
        f"-Q \"RESTORE DATABASE [{DB_CONFIG_SECONDARY['database']}] FROM DISK = '{backup_file}' "
<<<<<<< HEAD
        f"WITH MOVE 'test1' TO '{mdf_path}', MOVE 'test1_log' TO '{ldf_path}', NORECOVERY\""
=======
        f"WITH MOVE 'programming-in-db' TO '{mdf_path}', MOVE 'programming-in-db_log' TO '{ldf_path}', NORECOVERY\""
>>>>>>> 75df43ebf77df6d6a89f6ad58b07932703a02018
    )
    print(f"Running restore command: {restore_command}")
    if run_sqlcmd(restore_command):
        print(f"Full backup restored successfully on secondary server: {backup_file}")
    else:
        print(f"Failed to restore full backup.")

def drop_database_secondary():
    drop_db_command = (
        f"sqlcmd -S {DB_CONFIG_SECONDARY['host']} -U {DB_CONFIG_SECONDARY['user']} "
        f"-P {DB_CONFIG_SECONDARY['password']} "
        f"-Q \"IF EXISTS (SELECT name FROM sys.databases WHERE name = '{DB_CONFIG_SECONDARY['database']}') "
        f"DROP DATABASE [{DB_CONFIG_SECONDARY['database']}]\""
    )
    print(f"Running drop database command: {drop_db_command}")
    if run_sqlcmd(drop_db_command):
        print(f"Database dropped successfully on secondary server.")
    else:
        print(f"Failed to drop database on secondary server.")

def main():
    # Pastikan database sekunder tidak ada sebelum melakukan restore
    drop_database_secondary()
    
    # Step 1: Full backup and restore
    full_backup_file = full_backup_primary()
    if full_backup_file:
        restore_full_on_secondary(full_backup_file)
    
    # Step 2: Log shipping
    log_file = backup_transaction_log()
    if log_file:
        restore_log_on_secondary(log_file)
    
    # Step 3: Recover the secondary database to make it available
    recovery_secondary()

if __name__ == "__main__":
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 75df43ebf77df6d6a89f6ad58b07932703a02018
