from datetime import date
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .databaseClient import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas import UserCreateRequest
from .user_activity import UserActivity

class UserModel(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phoneNum: Mapped[str] = mapped_column(unique=True, nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    subscribed_for_newsletter: Mapped[bool] = mapped_column(default=False)
    activity: Mapped["UserActivity"] = relationship(back_populates="user")
    posts: Mapped[List["PostModel"]] = relationship(back_populates="author")
    post_interactions: Mapped[List["PostInteractionsModel"]] = relationship(
        back_populates="user"
    )

    def __repr__(self):
        return f"User: {self.username}"

    @classmethod
    async def find_by_email(cls, email: str, session: AsyncSession):
        stmt = select(UserModel).where(UserModel.email == email)
        result = await session.execute(stmt)
        user = result.scalar()
        return user
    
    @classmethod
    async def find_by_id(cls, user_id: int, session: AsyncSession):
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar()
        return user
    
    @staticmethod
    async def create(user: UserCreateRequest, session: AsyncSession):
        new_user = UserModel(**user.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    def to_json(self) -> dict:
        result = {}
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if value and key != "password":
                result[key] = value
        return result
