#!/bin/bash

# IAFA Frontend - Setup Script
# Installs all npm dependencies and sets up the frontend

set -e

FRONTEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$FRONTEND_DIR"

echo "=========================================="
echo "IAFA Frontend - Setup"
echo "=========================================="
echo ""

# Check Node.js version
echo "Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

node --version
npm --version

# Check if node_modules exists
if [ -d "node_modules" ]; then
    echo ""
    echo "⚠️  node_modules already exists. Removing..."
    rm -rf node_modules package-lock.json
fi

# Install dependencies
echo ""
echo "Installing npm dependencies..."
echo "This may take a few minutes..."
npm install

# Verify installation
echo ""
echo "Verifying installation..."
if [ -d "node_modules" ]; then
    echo "✅ Dependencies installed successfully"
    
    # Check key packages
    if [ -d "node_modules/react" ]; then
        echo "✅ React installed"
    fi
    if [ -d "node_modules/vite" ]; then
        echo "✅ Vite installed"
    fi
    if [ -d "node_modules/tailwindcss" ]; then
        echo "✅ Tailwind CSS installed"
    fi
    if [ -d "node_modules/axios" ]; then
        echo "✅ Axios installed"
    fi
else
    echo "❌ Installation failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Frontend Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  npm run dev"
echo ""
echo "The frontend will be available at:"
echo "  http://localhost:5173"
echo ""
echo "Make sure the backend is running at:"
echo "  http://localhost:8000"
echo ""
