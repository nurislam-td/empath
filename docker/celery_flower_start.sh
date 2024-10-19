#!/bin/bash

celery -A app.tasks.celery_app:celery_app flower
