@echo off
set BACKUP_DIR=backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

echo Creating backup: %BACKUP_DIR%
mkdir %BACKUP_DIR%

copy *.py %BACKUP_DIR%\
copy *.txt %BACKUP_DIR%\
copy .env %BACKUP_DIR%\
copy *.md %BACKUP_DIR%\
if exist logo.png copy logo.png %BACKUP_DIR%\
if exist business.db copy business.db %BACKUP_DIR%\

echo Backup created successfully in %BACKUP_DIR%
pause