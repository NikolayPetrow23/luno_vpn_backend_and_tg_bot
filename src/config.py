import base64
import os

from dotenv import load_dotenv

load_dotenv()


class DataBase:
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')

    USER = f"{DB_USER}:{DB_PASS}"
    DATABASE = f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    URL_DB = f"postgresql+asyncpg://{USER}@{DATABASE}"


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    PLATEGA_URL = os.getenv("PLATEGA_URL")
    MERCHANT_ID = os.getenv("MERCHANT_ID")
    API_KEY = os.getenv("API_KEY")
    URL_DOMAIN = os.getenv("URL_DOMAIN")
    URL_DOMAIN_SUB = os.getenv("URL_DOMAIN_SUB")
    API_TOKEN_SERVER = os.getenv("API_TOKEN_SERVER")
    PORT_API_SERVER = os.getenv("PORT_API_SERVER")
    SBP = 2
    CARD = 10
    CRYPTO = 13


class AuthJWT:
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1


class Settings:
    db: DataBase = DataBase()
    config: Config = Config()
    auth_jwt: AuthJWT = AuthJWT()


settings: Settings = Settings()
