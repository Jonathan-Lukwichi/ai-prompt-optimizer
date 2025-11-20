#!/bin/bash
# AI Prompt Optimizer - Launch Script for macOS/Linux

echo "========================================"
echo "AI PROMPT OPTIMIZER"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found."
    echo "Using system Python..."
fi

echo ""
echo "Starting Streamlit app..."
echo ""
echo "The app will open in your browser at http://localhost:8502"
echo "Press Ctrl+C to stop the server"
echo ""

python -m streamlit run home.py
