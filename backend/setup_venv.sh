#!/bin/bash

# IAFA Backend - Virtual Environment Setup Script
# This script creates a virtual environment and installs all dependencies

set -e  # Exit on error

BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BACKEND_DIR"

echo "=========================================="
echo "IAFA Backend - Virtual Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv

if [ ! -d "venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import fastapi; print('✅ FastAPI:', fastapi.__version__)"
python -c "import uvicorn; print('✅ Uvicorn:', uvicorn.__version__)"
python -c "import pandas; print('✅ Pandas:', pandas.__version__)"
python -c "import pyarrow; print('✅ PyArrow:', pyarrow.__version__)"
python -c "import duckdb; print('✅ DuckDB:', duckdb.__version__)"
python -c "import requests; print('✅ Requests:', requests.__version__)"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To start the server, run:"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "To deactivate the virtual environment, run:"
echo "  deactivate"
echo ""
