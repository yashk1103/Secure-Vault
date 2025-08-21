@echo off
REM Development Setup Script for Secure Vault (Windows)

echo Setting up Secure Vault development environment...

REM Backend setup
echo Setting up Python backend...
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Frontend setup
echo Setting up React frontend...
cd frontend-react

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

cd ..

echo Setup complete!
echo.
echo To start the application:
echo 1. Backend: python api/main.py
echo 2. Frontend: cd frontend-react ^&^& npm start
echo.
echo Access the application at http://localhost:3000

pause
