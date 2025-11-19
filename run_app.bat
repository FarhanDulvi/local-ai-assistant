@echo off
echo ==========================================
echo      Local AI Assistant Setup & Run
echo ==========================================

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if Ollama is reachable (simple check)
echo.
echo Please ensure Ollama is running!
echo We recommend running: ollama pull gemma3:1b
echo.

REM Run the app
echo Starting the application...
streamlit run app.py

pause
