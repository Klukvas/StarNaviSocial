from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "StarNavi social"
    SECRET_KEY: str = "your-secret-key"
    REFRESH_SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 5

    MIN_AGE: int = 13

    # OAuth2PasswordBearer for token retrieval
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/signin")
    # Password hashing
    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()
