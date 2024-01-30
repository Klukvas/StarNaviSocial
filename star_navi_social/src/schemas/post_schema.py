from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str


class PostDb(PostBase):
    id: int
    placed_at: datetime
    placed: bool
    author_id: int
    likes: int
    dislikes: int

    class Config:
        from_attributes = True
