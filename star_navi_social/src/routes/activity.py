from datetime import date
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
import src.schemas.user_schema as UserSchemas
from src.config import settings
from src.models import UserModel, get_async_session
from src.utils.auth import Auth
from fastapi import status
from src.controllers import ActivityController
from src.schemas import UserActivityBase
from src.utils import track_requests

activity_router = APIRouter(prefix="/user_info")


@activity_router.get(
    "/activity",
    summary="Get user activity",
    status_code=status.HTTP_200_OK,
    response_model=UserActivityBase,
)
@track_requests()
async def get_user_activity(
    user: UserModel = Depends(Auth.get_user_by_token),
    session: AsyncSession = Depends(get_async_session),
):
    return await ActivityController.get_activity(session=session, user=user)
