@echo off
REM AI Prompt Optimizer - Launch Script for Windows

echo ========================================
echo AI PROMPT OPTIMIZER
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found.
    echo Using system Python...
)

echo.
echo Starting Streamlit app...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py

pause
