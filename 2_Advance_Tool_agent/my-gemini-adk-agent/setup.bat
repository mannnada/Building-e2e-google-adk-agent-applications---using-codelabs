@echo off
REM Setup script for Advanced Tool Agent (Windows)

echo ========================================
echo Advanced Tool Agent - Setup Script
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    exit /b 1
)
python --version
echo.

REM Check Node.js
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18 or higher.
    exit /b 1
)
node --version
echo.

REM Install Gemini CLI
echo [3/5] Installing Gemini CLI...
call npm install -g @google/generative-ai-cli
if errorlevel 1 (
    echo ERROR: Failed to install Gemini CLI
    exit /b 1
)
echo Gemini CLI installed successfully
echo.

REM Install Python dependencies
echo [4/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    exit /b 1
)
echo Python dependencies installed successfully
echo.

REM Setup environment file
echo [5/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo.
    echo IMPORTANT: Edit .env file and add your GEMINI_API_KEY
    echo Get your API key from: https://makersuite.google.com/app/apikey
) else (
    echo .env file already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your GEMINI_API_KEY
echo 2. Run: python tests\quick_test.py
echo 3. Start using: python tool_agent.py --interactive
echo.
echo For more information, see README.md
echo.

pause
