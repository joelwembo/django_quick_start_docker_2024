#!/bin/bash
set -e

if [ "$1" = 'runserver' ]; then
    sleep 1
    python manage.py migrate || true
    python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi
