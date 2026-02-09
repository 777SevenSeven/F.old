#!/bin/bash

# GarimpoBot - Quick Setup

echo "Starting GarimpoBot setup..."

echo ""
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Install Python 3.10+"
    exit 1
fi

echo "Python found."

if ! command -v flutter &> /dev/null; then
    echo "Flutter not found. Frontend setup will be skipped."
    FLUTTER_AVAILABLE=false
else
    FLUTTER_AVAILABLE=true
fi

echo "Installing backend dependencies..."
pip install -r requirements.txt
playwright install chromium

echo "Backend ready."

if [ "$FLUTTER_AVAILABLE" = true ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    flutter pub get
    cd ..
    echo "Frontend ready."
fi

echo "Setup complete."
echo ""
echo "Start backend:"
echo "  python run.py --mode api"

if [ "$FLUTTER_AVAILABLE" = true ]; then
    echo "Start frontend:"
    echo "  cd frontend && flutter run -d chrome"
fi

echo "Read QUICKSTART.md for more info."
