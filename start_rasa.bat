@echo off
REM Start Rasa server
echo Starting Rasa server on http://localhost:5005
cd /d "%~dp0rasa_minimal"
call ..\.venv-1\Scripts\activate.bat
rasa run -m models --enable-api --cors "*" --port 5005
pause
