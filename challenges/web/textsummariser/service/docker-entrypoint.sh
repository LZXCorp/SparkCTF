#!/bin/bash
set -e

# Start cron in the background
echo "Starting cron service..."
cron

# Start the application
echo "Starting application..."
exec su -s /bin/bash appuser -c "gunicorn --bind 0.0.0.0:8550 --workers 2 --timeout 120 app:app"
