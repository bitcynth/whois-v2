#!/bin/sh
source env/bin/activate
exec gunicorn -b :5000 --access-logfile - --error-logfile - whoisclient:app