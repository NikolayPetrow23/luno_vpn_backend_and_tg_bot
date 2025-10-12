import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from src.api import router as api_router
from src.admin.view import UsersAdmin
from src.admin.auth import authentication_backend
from src.database import engine

app = FastAPI(
    title="FastAPI Template",
    version="0.0.1",
    # docs_url=None,    # Отключить Swagger UI
    # redoc_url=None,   # Отключить ReDoc
    # openapi_url=None  # Отключить OpenAPI JSON
)

# API
app.include_router(api_router)

# Панель Админа
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
