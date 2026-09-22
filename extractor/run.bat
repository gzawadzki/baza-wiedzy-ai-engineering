@echo off
chcp 65001 > nul
set PYTHON="C:\Users\taki1\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"

if not exist %PYTHON% (
    set PYTHON=python
)

%PYTHON% scripts/extract_kunchen_tips.py %*
pause
