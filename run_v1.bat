@echo off
cd /d %~dp0
python "Chat-Bot (v1)\main.py" %*
if NOT "%ERRORLEVEL%"=="0" pause
