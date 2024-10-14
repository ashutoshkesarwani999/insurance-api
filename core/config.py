import os
from dotenv import load_dotenv
from enum import Enum
from pydantic import  PostgresDsn, RedisDsn

load_dotenv()

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"

def create_postgres_url():
    scheme = "postgresql+asyncpg"
    username = os.getenv("user", "postgres")
    password = os.getenv("password", "password123")
    host = os.getenv("DB_HOST", "0.0.0.0")
    port = int(os.getenv("port", "5432"))
    database = os.getenv("db", "dbtest")

    return f"{scheme}://{username}:{password}@{host}:{port}/{database}"

class Config():
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL:PostgresDsn=   create_postgres_url()
    RELEASE_VERSION: str = "0.1"
    SECRET_KEY: str = "secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    REDIS_URL:str = ""
    S3_BUCKET:str = os.getenv("S3_BUCKET")
    REDIS_HOST: str = os.getenv("REDIST_HOST","localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT",6379))


config: Config = Config()
