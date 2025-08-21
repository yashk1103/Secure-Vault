#!/bin/bash

# Development Setup Script for Secure Vault

echo "Setting up Secure Vault development environment..."

# Backend setup
echo "Setting up Python backend..."
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || venv\Scripts\activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Frontend setup
echo "Setting up React frontend..."
cd frontend-react

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

cd ..

echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Backend: python api/main.py"
echo "2. Frontend: cd frontend-react && npm start"
echo ""
echo "Access the application at http://localhost:3000"
