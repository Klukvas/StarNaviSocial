from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "StarNavi social"
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 5

    SECRET_KEY: str = Field()
    REFRESH_SECRET_KEY: str = Field()

    PG_USER: str = Field()
    PG_HOST: str = Field()
    PG_PORT: str = Field()
    PG_PASSWORD: str = Field()
    PG_DB_NAME: str = Field()

    MIN_AGE: int = 13

    # OAuth2PasswordBearer for token retrieval
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/signin")
    # Password hashing
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    DB_URL: str = 'postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}'

    model_config = SettingsConfigDict(env_file=".env")

    def db_url(cls) -> str:
        return (
            "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
                username=cls.PG_USER,
                password=cls.PG_PASSWORD,
                host=cls.PG_HOST,
                port=cls.PG_PORT,
                db_name=cls.PG_DB_NAME,
            )
        )

settings = Settings()
