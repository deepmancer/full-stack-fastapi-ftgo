#!/bin/sh

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "Database is ready, running migrations..."
alembic upgrade head

echo "Starting the application..."
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 5020
