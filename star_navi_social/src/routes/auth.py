from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import src.schemas.user_schema as UserSchemas
from src.models import get_async_session
from src.schemas import Authorize, StatusCodeErrorResponse, UserCreateResponse
from fastapi import status
from src.controllers import AuthController
from src.utils import track_sign_in
auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/signup",
    summary="Create a new user",
    response_model=UserSchemas.UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": UserSchemas.UserCreateResponse},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": StatusCodeErrorResponse}
    },
)
async def signup(user: UserSchemas.UserCreateRequest, session: AsyncSession = Depends(get_async_session)) -> UserCreateResponse:
    return await AuthController.signup(user=user, session=session)


@auth_router.post(
    "/signin",
    summary="Sing in as user",
    responses={
        status.HTTP_200_OK: {"model": Authorize},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": StatusCodeErrorResponse},
    },
)
@track_sign_in()
async def signin(
    user: UserSchemas.UserBase, session: AsyncSession = Depends(get_async_session)
) -> Authorize:
    return await AuthController.signin(user=user, session=session)