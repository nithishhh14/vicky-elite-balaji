@echo off
REM Wrapper for Vicky's scheduled jobs. Called by Task Scheduler.
REM
REM Everything is absolute on purpose: a scheduler-launched process does not
REM inherit the interactive shell's PATH, so a bare `python` fails silently
REM while the task still reports exit 0.
REM
REM Keep CRLF line endings. cmd.exe mis-parses LF and starts complaining
REM about its own REM lines.
REM
REM   run_job.cmd daily | health | weekly | backfill
setlocal
set "ROOT=C:\Users\gardo\Vicky_organized\Vicky"
set "PY=C:\Users\gardo\AppData\Local\Python\pythoncore-3.14-64\python.exe"
set "LOG=%ROOT%\vicky_data\state\logs\schedule.log"
cd /d "%ROOT%"
echo [%date% %time%] --- %* --- >> "%LOG%" 2>&1
"%PY%" -m agents.seo %* >> "%LOG%" 2>&1
echo [%date% %time%] exit=%errorlevel% >> "%LOG%" 2>&1
endlocal
