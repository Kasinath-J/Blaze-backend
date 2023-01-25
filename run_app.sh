#!/usr/bin/env bash

# start background tasks 
python manage.py runserver &

python manage.py process_tasks