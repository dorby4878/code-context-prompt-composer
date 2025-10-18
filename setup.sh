#!/usr/bin/env bash
set -e

echo "🚀 Setting up Code Context & Prompt Composer..."

# Check Python version
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 not found. Please install Python 3.11 first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.11 -m venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p .ctx/tasks
mkdir -p .ctx/templates

# Initialize database
echo "💾 Initializing database..."
python3 -c "
from pathlib import Path
from src.ctx_ui.storage.store import MetadataStore
db = MetadataStore(Path('.ctx/metadata.db'))
print('✓ Database initialized')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  source .venv/bin/activate"
echo "  python src/ctx_ui/app.py"
echo ""
