DB_CONFIG = {
    'server': 'localhost',
    'port': '1433',
    'user': 'sa', #Sesuaikan dengan user SQL Server
    'password': '123', # Sesuaikan dengan password SQL Server
    'database': 'programming-in-db', # Sesuaikan dengan nama database yang akan di backup
    'driver': 'ODBC Driver 18 for SQL Server'
}

BACKUP_DIR = 'backup'
LOG_FILE = 'logs/backup_restore.log'