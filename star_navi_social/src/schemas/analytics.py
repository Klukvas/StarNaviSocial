from pydantic import BaseModel


class LikesAnalyticResponse(BaseModel):
    date: str
    count: int