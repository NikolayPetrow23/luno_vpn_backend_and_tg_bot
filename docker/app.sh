#!/bin/bash

alembic revision --autogenerate -m "Initial DataBase."

alembic upgrade head

gunicorn backend.main:app --workers 4 --certfile=certs/certificate.crt --keyfile=certs/certificate.key --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000