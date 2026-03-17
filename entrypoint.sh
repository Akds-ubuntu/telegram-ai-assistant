#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
echo "PostgreSQL is ready."

echo "Running migrations..."
alembic upgrade head
echo "Starting Gunicorn..."
exec gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --log-level info