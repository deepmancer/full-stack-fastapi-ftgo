#!/bin/sh

echo "Starting the application..."
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
