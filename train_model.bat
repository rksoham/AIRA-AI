@echo off
REM Train Rasa model
echo Training Rasa model...
cd /d "%~dp0rasa_minimal"
call ..\.venv-1\Scripts\activate.bat
rasa train
echo.
echo Training complete! Model saved in models/ directory
pause
