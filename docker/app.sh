#!/bin/bash

# Генерим новую миграцию со всеми текущими моделями

alembic upgrade head

gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000



# alembic revision --autogenerate -m "init"

# alembic upgrade head

# gunicorn backend.main:app --workers 4 --certfile=certs/certificate.crt --keyfile=certs/certificate.key --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
