from datetime import date

from sqlalchemy import Date, ForeignKey, Text, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .databaseClient import Base
from .user_model import UserModel


class PostInteractionsModel(Base):
    __tablename__ = "PostInteractions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    is_like: Mapped[bool]  # Updated naming convention

    post: Mapped["PostModel"] = relationship(back_populates="post_interactions")  # type: ignore
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))

    created_at: Mapped[date] = mapped_column(server_default=func.current_date())

    user: Mapped["UserModel"] = relationship(back_populates="post_interactions")
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    @classmethod
    async def getUserInteractionsByPost(cls, user_id: int, post_id: int, session: AsyncSession):
        stmt = select(cls).where((cls.user_id == user_id) & (cls.post_id == post_id))
        result = await session.execute(stmt)
        interactions = result.scalar()
        return interactions

    @classmethod
    async def updateState(cls, interaction_id: int, new_state: bool, session: AsyncSession):
        stmt = update(cls).where(cls.id == interaction_id).values(is_like=new_state)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def insertNewInteraction(cls, user_id: int, post_id: int, state: bool, session: AsyncSession):
        new_interaction = cls(is_like=state, post_id=post_id, user_id=user_id)
        session.add(new_interaction)
        await session.commit()
        await session.refresh(new_interaction)

    @classmethod
    async def deleteIneraction(cls, interaction_id: int, session: AsyncSession):
        stmt = delete(cls).where(cls.id == interaction_id)
        await session.execute(stmt)
        await session.commit()
