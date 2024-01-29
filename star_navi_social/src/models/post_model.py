from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.post_schema import PostBase
from .databaseClient import Base
from sqlalchemy import select, update
from .user_model import UserModel


class PostModel(Base):
    __tablename__ = "Post"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)

    placed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    placed: Mapped[bool] = mapped_column(default=True)

    author: Mapped[UserModel] = relationship(back_populates="posts")
    author_id: Mapped[int] = mapped_column(ForeignKey("User.id"))

    post_interactions: Mapped[List["PostInteractionsModel"]] = relationship( # type: ignore
        back_populates="post"
    )

    likes: Mapped[int] = mapped_column(nullable=False, default=0)
    dislikes: Mapped[int] = mapped_column(nullable=False, default=0)

    @classmethod
    async def create(cls, post: PostBase, author_id: int, session: AsyncSession):
        new_post = PostModel(author_id=author_id, **post.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post
    
    @classmethod
    async def find_by_id(cls, post_id: int, session: AsyncSession):
        stmt = select(PostModel).where(PostModel.id == post_id)
        result = await session.execute(stmt)
        post = result.scalar()
        return post
    
    @classmethod
    async def switch_count_interactions(cls, post_id: int, incrementToLikes: bool, session: AsyncSession):
        # TODO: enum || pydantic for incrementToLikes
        if incrementToLikes:
            statement = (
                update(cls)
                .where(cls.id == post_id)
                .values(
                    {
                        "likes": cls.__dict__["likes"] + 1,
                        "dislikes": cls.__dict__["dislikes"] - 1,
                    }
                )
            )
        else:
            statement = (
                update(cls)
                .where(cls.id == post_id)
                .values(
                    {
                        "dislikes": cls.__dict__["dislikes"] + 1,
                        "likes": cls.__dict__["likes"] - 1,
                    }
                )
            )
        await session.execute(statement)
        await session.commit()
    

    @classmethod
    async def decrease_likes(cls, post_id: int, session: AsyncSession):
        stmt = (
            update(cls)
            .where(cls.id == post_id)
            .values({"likes": cls.__dict__["likes"] - 1})
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def increase_likes(cls, post_id: int, session: AsyncSession):
        stmt = (
            update(cls)
            .where(cls.id == post_id)
            .values({"likes": cls.__dict__["likes"] + 1})
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def decrease_dislikes(cls, post_id: int, session: AsyncSession):
        stmt = (
            update(cls)
            .where(cls.id == post_id)
            .values({"dislikes": PostModel.__dict__["dislikes"] - 1})
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def increase_dislikes(cls, post_id: int, session: AsyncSession):
        stmt = (
            update(cls)
            .where(cls.id == post_id)
            .values({"dislikes": cls.__dict__["dislikes"] + 1})
        )
        await session.execute(stmt)
        await session.commit()
