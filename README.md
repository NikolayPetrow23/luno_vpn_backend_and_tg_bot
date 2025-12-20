# fastapi_template

Technology:
FastApi
Postgres
Alembic
SQLAlchemy
SQLAdmin
Docker
Docker-compose


Initial Project

# 1

Создание виртального окружения: 
`python3 -m venv venv`

# 2

Активировать виртуальное окружение: 
`source venv/bin/activate`

# 3

Устновить зависимости из файла:
`pip install -r requirements.txt`


Other:

# Обновить список зависимостей
`pip freeze > requirements.txt`

# Деактивировать виртуальное окружение
`deactivate`


FastAPI commands

# Запуск приложения с помощью команды
`uvicorn src.main:app --reload`


Alembic commands 

# Инициализировать alembic
`alembic init migrations`

# Сгенерировать миграцию
`alembic revision --autogenerate -m "init"`

# Применить миграцию
`alembic upgrade head`


Create DB
`docker run -p 5432:5432 --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3`

На случай если происходят ошибки с номером версии!
`DROP TABLE alembic_version;`


File .env для разарботки

DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

ACCESS_SECRET_KEY=5d7d+h5R0NLjcCmNlN5l6v40hIyH5/h/yJ7KrDJc7xo=
REFRESH_SECRET_KEY=BYovezMkkn7d51i6gWZSQWucMkw5VYaYNT1UhJr8P4o=
ALGORITHM=HS256

python3 src/admin/create_super_user.py