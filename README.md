# Firebird-Database-Repair-Tool
The Firebird Database Repair Tool is a powerful utility designed to address and resolve issues within Firebird databases. Whether you encounter corruption, data inconsistencies, or other database-related challenges, this tool serves as a reliable solution to restore and optimize your Firebird database.

Download and extract the Restore DOS executable. Place it in the your folder. Execute Restore DOS.exe; it will open with a prompt asking for the Firebird path. Click the button to select the Firebird bin folder, typically located at: C:\Program Files\Firebird\Firebird_2_5\bin.

On this screen, select the corrupted database, the path for .GBK, and also the path for the new .FB database. Click "Run Restore," and it will perform gfix on the corrupted database. After this, it will start creating the new database without the errors found in gfix.

Note: Do not close Restore DOS during this process, as it is manipulating the database, and sudden closure may lead to further errors.

When the new database is ready, the following message will be displayed:

The same applies if an error occurs during any of the processes; it will notify you of the issue.

Once the process is completed, generating the NewBanco.FB, this will be the new database with all the corrected errors.

Obs.: The source code is written in Python (main.py) and compiled using Python 3.8 so that it can run on Windows 7 or later devices.
