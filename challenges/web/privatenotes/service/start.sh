#!/bin/bash

mongod --fork --logpath /var/log/mongod.log &
gunicorn --bind 0.0.0.0:8080 app:app --workers 3 --worker-class gthread --threads 6 --timeout 15 --graceful-timeout 15 --keep-alive 2