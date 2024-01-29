from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.post_schema import PostBase
from .databaseClient import Base
from sqlalchemy import select, update
from datetime import datetime
from sqlalchemy import ForeignKey, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserActivityBase
from .databaseClient import Base


class UserActivity(Base):
    __tablename__ = "user_activity"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    last_login: Mapped[datetime] = mapped_column(nullable=True)
    last_request: Mapped[datetime] = mapped_column(nullable=True)
    user: Mapped["UserModel"] = relationship(back_populates="activity")


    @classmethod
    async def get_by_user_id(cls, user_id: int, session: AsyncSession) -> 'UserActivity':
        stmt = select(cls).where(cls.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def update_last_signin(cls, user_id: int, session: AsyncSession) -> None:
        stmt = update(cls).where(cls.user_id == user_id).values({"last_login": datetime.now()})
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_last_request(cls, user_id: int, session: AsyncSession) -> None:
        stmt = update(cls).where(cls.user_id == user_id).values({"last_request": datetime.now()})
        await session.execute(stmt)
        await session.commit()
    @classmethod
    async def create_activity(cls, user_id: int, session: AsyncSession, data:UserActivityBase ) -> 'UserActivity':
        activity = cls(**data.model_dump())
        session.add(activity)
        await session.commit()
        return activity