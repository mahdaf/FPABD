# Database Backup and Restore Utility

A Python-based utility for automating the backup and restore processes of a SQL Server database. This tool supports full, differential, and transaction log backups, as well as log shipping to a secondary server.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Modules](#modules)
  - [auto_backup.py](#auto_backuppy)
  - [backup.py](#backuppy)
  - [restore.py](#restorepy)
  - [log_shipping.py](#log_shippingpy)
  - [utils.py](#utilspy)
  - [config.py](#configpy)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/db-backup-restore.git
    cd db-backup-restore
    ```

2. Create a virtual environment and install dependencies:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Configuration

Edit the `config.py` file to set your SQL Server database configuration:
```python
DB_CONFIG = {
    'server': 'localhost',
    'port': '1433',
    'user': 'sa',
    'password': '123',
    'database': 'programming-in-db',
    'driver': 'ODBC Driver 18 for SQL Server'
}

BACKUP_DIR = 'backup'
LOG_FILE = 'logs/backup_restore.log'
```


## Usage
### Full Backup
To perform a full backup, run:
```python backup.py full```
### Differential Backup
To perform a differential backup, run:
```python backup.py diff```
### Transaction Log Backup
To perform a transaction log backup, run:
```python backup.py translog```
### Automated Backups
To set up automated backups, specify the intervals in seconds for each type of backup:
```python auto_backup.py FULL_BACKUP_INTERVAL DIFF_BACKUP_INTERVAL TRANSLOG_BACKUP_INTERVAL```
### Restore
To restore a database from a backup file, run:
```python restore.py /path/to/backup/file.bak```
### Log Shipping
To perform log shipping from the primary to the secondary server, run:
```python log_shipping.py```


## Modules
### auto_backup.py
Automates the full, differential, and transaction log backup processes based on specified intervals.
### backup.py
Provides command-line interface (CLI) for performing full, differential, and transaction log backups.
### restore.py
Provides CLI for restoring a database from a backup file.
### log_shipping.py
Automates the log shipping process to a secondary server for disaster recovery purposes.
### utils.py
Contains utility functions for logging setup and error reporting.
### config.py
Contains the configuration settings for database connection and file paths.


## Logging
Log files are stored in the logs directory. The main log file is backup_restore.log. Error reports are stored in error_report.txt.


## Error Handling
Errors encountered during backup or restore processes are logged and appended to error_report.txt.
