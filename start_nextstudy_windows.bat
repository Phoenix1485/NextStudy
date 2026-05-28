@echo off
setlocal

rem Startet NextStudy unter Windows aus dem Projektordner heraus.
rem Falls noch keine virtuelle Umgebung existiert, wird sie automatisch angelegt.

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python wurde nicht gefunden.
        echo Bitte installiere Python 3.11 oder neuer von https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

if not exist ".venv\Scripts\python.exe" (
    echo Erstelle virtuelle Python-Umgebung...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Die virtuelle Umgebung konnte nicht erstellt werden.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"

echo Starte NextStudy...
python main.py

echo.
pause

