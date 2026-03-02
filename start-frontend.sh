#!/bin/bash
set -e

# Use PORT from environment or default to 8501
PORT=${PORT:-8501}

echo "Starting Bhrahma frontend on port $PORT"

# Start Streamlit with the port
exec streamlit run frontend/app.py --server.port="$PORT" --server.address=0.0.0.0 --server.headless=true
