import datetime
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.middlewares import LogMiddleware
from src.models import (UserActivity, UserModel, databaseClient,
                        get_async_session)
from src.routes import (activity_router, analytics_router, auth_router,
                        post_router)
from src.schemas import UserActivityBase
from src.schemas.common import HttpError, StatusCodeErrorResponse
from src.utils.auth import Auth
from src.utils.exception import ExceptionError
from src.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await databaseClient.create_database_if_not_exist()
    await databaseClient.create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(activity_router)

app.add_middleware(LogMiddleware)


origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ExceptionError)
def exception_handler(request: Request, ex: ExceptionError) -> JSONResponse:
    res = JSONResponse(
        status_code=ex.status_code,
        content=StatusCodeErrorResponse(
            timestamp=datetime.datetime.now().isoformat(),
            error_message=ex.message,
        ).model_dump()
    )
    res.body
    return res

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, ex: RequestValidationError) -> JSONResponse:
    parsed_errors = []
    b = request.body
    for err in ex.errors():
        # Here is such strange error field ename parsing, because pydantic error can be one of two options:
        # "{'loc': ('body', 'email')" or "{'loc': ('body',)" where "loc" value can contain 1 or 2 strings.
        parsed_errors.append({err["loc"][1] if len(err["loc"]) > 1 else err["loc"][0]: err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StatusCodeErrorResponse(
            timestamp=datetime.datetime.now().isoformat(),
            error_message='Request validation error',
            errors=[HttpError(error_description=list(error.values())[0], field=list(error.keys())[0]) for error in parsed_errors]
        ).model_dump(),
    )

if __name__ == "__main__":
    breakpoint()
    uvicorn.run(app, host="0.0.0.0", port=8000)