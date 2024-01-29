from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserActivityBase(BaseModel):
    user_id: int
    last_login: Optional[datetime] = None
    last_request: Optional[datetime] = None


class UserActivityInDb(UserActivityBase):
    id: int
