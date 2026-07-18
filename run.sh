#!/bin/bash

echo "========================================"
echo "  CyberSuite - Penetration Testing Suite"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Starting CyberSuite..."
echo ""

# Run the application
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Application failed to start"
    echo "Check the error messages above"
    read -p "Press Enter to exit..."
fi
