#!/bin/bash

cd src
alembic upgrade head
cd ..


python3.12  src/main.py

# gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000