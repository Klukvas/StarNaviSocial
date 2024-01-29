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
from src.controllers import AnalyticsController
from src.schemas import LikesAnalyticResponse
from src.utils import track_requests
analytics_router = APIRouter(prefix="/analytics")


@analytics_router.get(
    "/likes",
    summary="Create a new user",
    response_model=list[LikesAnalyticResponse],
    status_code=status.HTTP_200_OK,
)
@track_requests()
async def get_likes_analyth(
    date_from: date = Query(..., title="Start date"),
    date_to: date = Query(..., title="End date"),
    user: UserModel = Depends(Auth.get_user_by_token),
    session: AsyncSession = Depends(get_async_session),
) -> list[LikesAnalyticResponse]:
    return await AnalyticsController.get_likes_analyth(date_from=date_from, date_to=date_to, session=session, user=user)