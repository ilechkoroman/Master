#!/bin/bash
exec gunicorn \
--bind 0.0.0.0:5000 \
--timeout 6000 \
--worker-class gthread \
manage:app
