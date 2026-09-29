@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=python"
if exist ".venv\Scripts\python.exe" set "PYTHON=.venv\Scripts\python.exe"

set "ENV_NAME=%~1"
if "%ENV_NAME%"=="" set "ENV_NAME=test"
if not "%~1"=="" shift

"%PYTHON%" run.py --env "%ENV_NAME%" %*
exit /b %ERRORLEVEL%
