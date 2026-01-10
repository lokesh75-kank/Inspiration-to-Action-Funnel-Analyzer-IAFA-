#!/bin/bash

# IAFA Backend - Simple Virtual Environment Setup
# Uses latest compatible versions for Python 3.13

set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "IAFA Backend - Virtual Environment Setup"
echo "=========================================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install core packages first (already compatible)
echo ""
echo "Installing core data processing packages..."
pip install pandas pyarrow duckdb

# Install web framework with compatible versions
echo ""
echo "Installing web framework packages..."
pip install "fastapi>=0.115.0" "uvicorn[standard]>=0.32.0" "pydantic>=2.10.0" "pydantic-settings>=2.6.0"

# Install remaining packages
echo ""
echo "Installing remaining dependencies..."
pip install python-multipart python-jose[cryptography] passlib[bcrypt] aiofiles httpx requests python-dotenv

# Install development packages (optional)
echo ""
echo "Installing development packages..."
pip install pytest pytest-asyncio pytest-cov black isort mypy pylint

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import fastapi; print(f'✅ FastAPI: {fastapi.__version__}')" || echo "❌ FastAPI import failed"
python -c "import uvicorn; print(f'✅ Uvicorn: {uvicorn.__version__}')" || echo "❌ Uvicorn import failed"
python -c "import pydantic; print(f'✅ Pydantic: {pydantic.__version__}')" || echo "❌ Pydantic import failed"
python -c "import pandas; print(f'✅ Pandas: {pandas.__version__}')" || echo "❌ Pandas import failed"
python -c "import pyarrow; print(f'✅ PyArrow: {pyarrow.__version__}')" || echo "❌ PyArrow import failed"
python -c "import duckdb; print(f'✅ DuckDB: {duckdb.__version__}')" || echo "❌ DuckDB import failed"

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To activate: source venv/bin/activate"
echo "To start server: uvicorn app.main:app --reload --port 8000"
echo ""
