import functools
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserActivity, UserModel
from src.schemas import Authorize, UserActivityBase


async def sing_in_activity():
    pass


def track_sign_in():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            session = kwargs['session']
            fn_result = await func(*args, **kwargs)
            if type(fn_result) == Authorize:
                user_email = kwargs['user'].email
                user = await UserModel.find_by_email(session=session, email=user_email)
                last_activity = await UserActivity.get_by_user_id(session=session, user_id=user.id)
                if last_activity:
                    await UserActivity.update_last_signin(user_id=user.id, session=session)
                else:
                    rec = UserActivityBase(user_id=user.id, last_login=datetime.now())
                    await UserActivity.create_activity(user_id=user.id, session=session, data=rec)
            return fn_result
        return wrapped
    return wrapper




async def request_activity(session:AsyncSession, user: UserModel):
    last_activity = await UserActivity.get_by_user_id(session=session, user_id=user.id)
    if last_activity:
        await UserActivity.update_last_request(user_id=user.id, session=session)
    else:
        rec = UserActivityBase(user_id=user.id, last_request=datetime.now())
        await UserActivity.create_activity(user_id=user.id, session=session, data=rec)

def track_requests():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            session = kwargs['session']
            user = kwargs['user']
            await request_activity(user=user, session=session)
            return await func(*args, **kwargs)
        return wrapped
    return wrapper
