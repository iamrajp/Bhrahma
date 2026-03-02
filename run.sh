#!/bin/bash

# Bhrahma Run Script

echo "🧠 Starting Bhrahma Agentic System..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start backend in background
echo "Starting backend server..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Start frontend
echo "Starting frontend..."
cd frontend
streamlit run app.py

# Cleanup on exit
kill $BACKEND_PID
