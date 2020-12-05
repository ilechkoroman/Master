#!/bin/bash
exec celery worker -A app.celery.app --loglevel=info