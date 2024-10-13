from enum import Enum
from pydantic import  PostgresDsn, RedisDsn


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"



class Config():
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL: PostgresDsn = ""
    RELEASE_VERSION: str = "0.1"
    SECRET_KEY: str = "secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    REDIS_URL:str = ""


config: Config = Config()
