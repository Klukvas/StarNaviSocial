from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Security, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import UserModel
from src.models.databaseClient import get_async_session
from src.schemas import Token, TokenTypeEnum


class Auth:

    @staticmethod
    def create_access_token(data: dict) -> Token:
        to_encode = data.copy()
        to_encode["type"] = TokenTypeEnum.access
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return Token(token=encoded_jwt, token_type=TokenTypeEnum.access.value)

    @staticmethod
    def create_refresh_token(data: dict) -> Token:
        to_encode = data.copy()
        to_encode["type"] = TokenTypeEnum.refresh
        expire = datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, settings.ALGORITHM)
        return Token(token=encoded_jwt, token_type=TokenTypeEnum.refresh.value)

    @staticmethod
    async def _middleware_get_user_by_token(
        token: str,
        session: AsyncSession,
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            token_type = payload.get("type")
            if token_type != TokenTypeEnum.access or user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await UserModel.find_by_id(int(user_id), session)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    async def get_user_by_token(
        # token: Annotated[str, Depends(settings.oauth2_scheme)],
        authorization_header: str = Security(settings.api_key_header),
        session: AsyncSession = Depends(get_async_session),
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if authorization_header is None:
            raise credentials_exception

        if "Bearer " not in authorization_header:
            raise credentials_exception

        token = authorization_header.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            token_type = payload.get("type")
            if token_type != TokenTypeEnum.access or user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await UserModel.find_by_id(int(user_id), session)
        if user is None:
            raise credentials_exception
        return user
