@echo off
setlocal

rem Startet NextStudy unter Windows per Doppelklick.
rem Die Datei muss im gleichen Ordner wie index.py liegen.

cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo Python wurde nicht gefunden.
        echo Bitte installiere Python 3 und starte diese Datei danach erneut.
        echo.
        pause
        exit /b 1
    )
    set "PYTHON_CMD=python"
)

echo Starte NextStudy...
echo.
%PYTHON_CMD% index.py

echo.
echo NextStudy wurde beendet. Dieses Fenster kann jetzt geschlossen werden.
pause
