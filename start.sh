#!/bin/bash
# Startup script for the Dynamic Question Router

echo "=================================="
echo "Dynamic Question Router - Startup"
echo "=================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your API keys."
    echo ""
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Create feedback files if they don't exist
if [ ! -f feedback_data.json ]; then
    echo "[]" > feedback_data.json
    echo "✅ Created feedback_data.json"
fi

if [ ! -f feedback_data.csv ]; then
    echo "timestamp,question,predicted_domain,predicted_difficulty,chatbot_used,response,feedback_positive,corrected_domain,corrected_difficulty" > feedback_data.csv
    echo "✅ Created feedback_data.csv"
fi

echo ""
echo "=================================="
echo "Starting FastAPI server..."
echo "=================================="
echo ""
echo "Server will be available at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
