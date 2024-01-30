from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import PostInteractionsModel, UserModel
from src.schemas import LikesAnalyticResponse


class AnalyticsController:

    @staticmethod
    async def get_likes_analyth(
        date_from: str, date_to: str, session: AsyncSession, user: UserModel
    ) -> LikesAnalyticResponse:
        stmt = (
            select(
                func.DATE(PostInteractionsModel.created_at).label("day"),
                func.count().label("count"),
            )
            .where(PostInteractionsModel.created_at.between(date_from, date_to))
            .where(PostInteractionsModel.user_id == user.id)
            .where(PostInteractionsModel.is_like == True)
            .group_by(func.DATE(PostInteractionsModel.created_at))
        )

        result = await session.execute(stmt)
        rows = result.all()

        # Transform rows into a list of Pydantic models
        likes_list = [LikesAnalyticResponse(date=str(row[0]), count=row[1]) for row in rows]

        return likes_list
