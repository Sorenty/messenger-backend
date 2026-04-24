#!/bin/sh
set -e

exec gunicorn \
  --bind "0.0.0.0:${PORT:-5000}" \
  --workers "${WEB_CONCURRENCY:-3}" \
  --graceful-timeout 30 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile - \
  "run:app"