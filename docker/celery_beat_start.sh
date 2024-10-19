#!/bin/bash

cd ../backend

celery -A app.tasks.celery_app:celery_app beat -l info