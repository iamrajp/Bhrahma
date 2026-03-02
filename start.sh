#!/bin/bash
set -e

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

echo "Starting Bhrahma backend on port $PORT"

# Start uvicorn with the port
exec uvicorn backend.main:app --host 0.0.0.0 --port "$PORT"
