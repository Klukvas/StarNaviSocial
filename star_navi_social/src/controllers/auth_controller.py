from src.schemas import UserCreateRequest, UserCreateResponse, UserCreateBase, UserBase, Authorize
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserModel
from src.utils.exception import ExceptionError
from fastapi import status
from src.utils.auth import Auth
from src.utils.password_hasher import PasswordHasher



class AuthController:

    @staticmethod
    async def signup(
        user: UserCreateRequest, 
        session: AsyncSession
    ) -> UserCreateResponse:
        existing_user = await UserModel.find_by_email(email=user.email, session=session)
        if existing_user:
            raise ExceptionError(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message="Username already registered"
            )
        user.password = PasswordHasher.get_password_hash(user.password)
        del user.password_confirmation
        created_user = await UserModel.create(user, session)
        token = Auth.create_access_token({"sub": str(created_user.id)})
        refresh_token = Auth.create_refresh_token(
            {"sub": str(created_user.id)}
        )
        return UserCreateResponse(
            message="User registered successfully",
            user=UserCreateBase(**created_user.to_json()),
            access_token=token,
            refresh_token=refresh_token,
        )
    
    async def signin(
        user: UserBase, 
        session: AsyncSession
    ):
        existing_user = await UserModel.find_by_email(
            email=user.email, session=session
        )
        if not existing_user:
            raise ExceptionError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message="User not found")
        password_match = PasswordHasher.verify_password(user.password, existing_user.password)
        if password_match:
            token = Auth.create_access_token({"sub": str(existing_user.id)})
            refresh_token = Auth.create_refresh_token({"sub": str(existing_user.id)})
            return Authorize(refresh_token=refresh_token, access_token=token)
        else:
            raise ExceptionError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message="Wrong password")
