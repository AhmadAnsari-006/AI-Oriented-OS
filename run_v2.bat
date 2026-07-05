@echo off
cd /d %~dp0
python "Chat-Bot (v2)\main.py" %*
if NOT "%ERRORLEVEL%"=="0" pause
