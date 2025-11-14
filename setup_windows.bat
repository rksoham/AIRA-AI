@echo off
REM AIRA AI Chatbot - Windows Setup Helper
REM This script helps with Conda installation and environment setup

echo.
echo ============================================
echo   AIRA AI Chatbot - Windows Setup
echo ============================================
echo.

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Conda not found!
    echo.
    echo Please install Conda from:
    echo https://www.anaconda.com/download
    echo.
    pause
    exit /b 1
)

echo [✓] Conda found!
echo.

REM Create conda environment
echo [*] Creating conda environment 'aira-ai' with Python 3.10...
call conda create -n aira-ai python=3.10 -y

if %errorlevel% neq 0 (
    echo [!] Failed to create conda environment
    pause
    exit /b 1
)

echo [✓] Conda environment created!
echo.

REM Activate environment
echo [*] Activating conda environment...
call conda activate aira-ai

if %errorlevel% neq 0 (
    echo [!] Failed to activate environment
    pause
    exit /b 1
)

echo [✓] Environment activated!
echo.

REM Install Rasa
echo [*] Installing Rasa 3.6.0 (this may take 5-10 minutes)...
call conda install -c conda-forge rasa=3.6.0 -y

if %errorlevel% neq 0 (
    echo [!] Failed to install Rasa
    pause
    exit /b 1
)

echo [✓] Rasa installed!
echo.

REM Install additional dependencies
echo [*] Installing additional dependencies from requirements.txt...
call pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Failed to install requirements
    pause
    exit /b 1
)

echo [✓] All dependencies installed!
echo.

echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Train the model:
echo    python -m rasa train --domain rasa_minimal/domain.yml --data rasa_minimal/nlu.yml --stories rasa_minimal/stories.yml --config rasa_minimal/config.yml --out rasa_minimal/models
echo.
echo 2. Start Rasa server (Terminal 1):
echo    conda activate aira-ai
echo    python -m rasa run -m rasa_minimal/models --enable-api --cors "*" --port 5005
echo.
echo 3. Start Flask server (Terminal 2):
echo    .\.venv-1\Scripts\activate
echo    python app.py
echo.
echo 4. Open browser:
echo    http://localhost:5000
echo.
echo For more details, see: QUICK_START.md or RASA_COMPLETE_SETUP.md
echo.
pause
