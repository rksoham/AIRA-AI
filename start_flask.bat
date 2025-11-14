@echo off
REM Start Flask server
echo Starting Flask app on http://localhost:5000
cd /d "%~dp0"
call .venv-1\Scripts\activate.bat
python app.py
pause
