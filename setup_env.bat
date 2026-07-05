@echo off
cd /d %~dp0
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist requirements.txt (
  pip install -r requirements.txt
) else (
  echo requirements.txt not found.
)
echo Setup complete.
if NOT "%ERRORLEVEL%"=="0" pause
