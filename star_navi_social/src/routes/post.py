from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.schemas.post_schema as PostSchemas
from src.controllers import PostController
from src.models import UserModel, get_async_session
from src.schemas import MessageResponse, StatusCodeErrorResponse
from src.utils import Auth, track_requests

post_router = APIRouter(prefix="/post")



@post_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
    response_model=PostSchemas.PostDb,
    responses = {
        status.HTTP_201_CREATED: {"model": PostSchemas.PostDb},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": StatusCodeErrorResponse},
    }
)
@track_requests()
async def create_new_post(post: PostSchemas.PostBase, session: AsyncSession = Depends(get_async_session), user: UserModel = Depends(Auth.get_user_by_token)):
    return await PostController.create_new_post(post=post, session=session, user=user)
    


@post_router.post(
    "/{post_id}/like",
    summary="Like the post by id",
    description="If user already liked the post - like will be removed",
    response_model=MessageResponse,
    responses={
        status.HTTP_200_OK: {"model": MessageResponse},
        status.HTTP_404_NOT_FOUND: {"model": StatusCodeErrorResponse}
    }
)
@track_requests()
async def like_post(
    post_id: int,
    user: UserModel = Depends(Auth.get_user_by_token),
    session: AsyncSession = Depends(get_async_session),
):
    return await PostController.like_post(post_id=post_id, user=user, session=session)


@post_router.post(
    "/{post_id}/dislike",
    summary="Disike the post by id",
    description="If user already disliked the post - dislike will be removed",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse,
    responses={
        status.HTTP_200_OK: {"model": MessageResponse},
        status.HTTP_404_NOT_FOUND: {"model": StatusCodeErrorResponse}
    }
)
@track_requests()
async def dislike_post(
        post_id: int,
        user: UserModel = Depends(Auth.get_user_by_token),
        session: AsyncSession = Depends(get_async_session),
    ):
    return await PostController.dislike_post(post_id=post_id, user=user, session=session)
