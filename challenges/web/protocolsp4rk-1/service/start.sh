#!/bin/bash

mongod --fork --logpath /var/log/mongod.log &
gunicorn --bind 0.0.0.0:8080 app:app --workers 5 --worker-class gthread