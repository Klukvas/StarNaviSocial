from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import PostInteractionsModel, UserActivity, UserModel
from src.schemas import UserActivityBase


class ActivityController:

    @staticmethod
    async def get_activity(
        session: AsyncSession,
        user: UserModel
    ):
        activity = await UserActivity.get_by_user_id(user_id=user.id, session=session)
        return UserActivityBase(user_id=user.id, last_login=activity.last_login, last_request=activity.last_request)

        

        
            



         
