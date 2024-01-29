from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserActivityBase(BaseModel):
    user_id: int
    last_login: Optional[datetime] = None
    last_request: Optional[datetime] = None


class UserActivityInDb(UserActivityBase):
    id: int
