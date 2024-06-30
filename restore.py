import os
import argparse
import logging
from config import DB_CONFIG, LOG_FILE
from utils import setup_logging, run_shell_command, write_error_report

ERROR_REPORT_FILE = 'logs/error_report.txt'

def restore(filename):
    try:
        setup_logging(LOG_FILE)
        
        # # Tambahkan pernyataan untuk mengubah database ke dalam keadaan offline
        # offline_command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"ALTER DATABASE [{DB_CONFIG['database']}] SET OFFLINE WITH ROLLBACK IMMEDIATE\""
        # run_shell_command(offline_command)

        # # Tambahkan pernyataan untuk mengubah database ke dalam keadaan online
        # online_command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"ALTER DATABASE [{DB_CONFIG['database']}] SET ONLINE\""
        # run_shell_command(online_command)

        # Lakukan restore setelah database dalam keadaan offline
        command = f"sqlcmd -S {DB_CONFIG['server']} -U {DB_CONFIG['user']} -P {DB_CONFIG['password']} -Q \"RESTORE DATABASE [{DB_CONFIG['database']}] FROM DISK='{filename}' WITH REPLACE, NORECOVERY\""
        result = run_shell_command(command)
        if result and "Msg" in result:
            raise Exception(result)
        logging.info(f"Restore successful: {filename}")
        print(f"Restore successful: {filename}")
    except Exception as e:
        error_message = f"Restore failed: {str(e)}"
        logging.error(error_message)
        write_error_report(error_message, ERROR_REPORT_FILE)
        print(error_message)
        return

def main():
    parser = argparse.ArgumentParser(description='Database Restore CLI')
    parser.add_argument('filename', help='Backup file to restore from')
    args = parser.parse_args()

    # Ubah path relatif menjadi absolut
    backup_file = os.path.abspath(args.filename)
    try:
        restore(backup_file)
    except Exception as e:
        print(f"Restore failed: {str(e)}")

if __name__ == "__main__":
    main()