#!/usr/bin/env bash

# start background tasks 
gunicorn blaze_backend.wsgi:application &

python manage.py process_tasks