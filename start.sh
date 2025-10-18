#!/bin/bash

# Quick Start Script for Code Context & Prompt Composer

echo "🚀 Starting Code Context & Prompt Composer..."
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run the application
echo ""
echo "✨ Starting application..."
echo "🌐 Opening browser at http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m src.ctx_ui.app
