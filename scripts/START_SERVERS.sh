#!/bin/bash

# IAFA - Quick Start Script
# Starts both backend and frontend servers

set -e

echo "=========================================="
echo "IAFA - Starting Servers"
echo "=========================================="
echo ""

# Check if backend server is already running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server is already running on port 8000"
else
    echo "⚠️  Backend server is not running"
    echo ""
    echo "Please start the backend server in Terminal 1:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload --port 8000"
    echo ""
fi

# Check if frontend server is already running
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend server is already running on port 5173"
else
    echo "⚠️  Frontend server is not running"
    echo ""
    echo "Please start the frontend server in Terminal 2:"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
fi

echo "=========================================="
echo "After starting both servers:"
echo "=========================================="
echo ""
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Pinterest project should appear on the Projects page!"
echo ""
