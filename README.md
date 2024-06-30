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

## Installation
### Step 1: Install Python
Ensure that Python is installed on your system. You can download and install Python from the official Python website.
### Step 2: Install Required Python Modules
Install the necessary Python modules using pip. Run the following command:
  ``` sh
  pip install pyodbc
  ```
### Step 3: Install ODBC Driver
Install the ODBC Driver for SQL Server. You can download it from the Microsoft ODBC Driver for SQL Server.
### Step 4: Clone the Repository
Clone this repository to your local machine using the following command:
  ``` sh
  git clone https://github.com/mahdaf/FPABD.git
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
  ```sh
  python backup.py full
  ```
### Differential Backup
To perform a differential backup, run:
  ```sh
  python backup.py diff
  ```
### Transaction Log Backup
To perform a transaction log backup, run:
  ```sh
  python backup.py translog
  ```
### Automated Backups
To set up automated backups, specify the intervals in seconds for each type of backup:
  ```sh
  python auto_backup.py FULL_BACKUP_INTERVAL DIFF_BACKUP_INTERVAL TRANSLOG_BACKUP_INTERVAL
  ```
### Restore
To restore a database from a backup file, run:
  ```sh
  python restore.py /path/to/backup/file.bak
  ```
### Log Shipping
To perform log shipping from the primary to the secondary server, run:
  ```sh
  python log_shipping.py
  ```


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
