from enum import Enum
from pydantic import BaseModel
from typing import Union
class HttpError(BaseModel):
    field: str
    error_description: str

class StatusCodeErrorResponse(BaseModel):
    timestamp: str
    error_message: str
    errors: list[HttpError] = []


class TokenTypeEnum(str, Enum):
    access = "access"
    refresh = "refresh"


class Token(BaseModel):
    token: str
    token_type: TokenTypeEnum


class Authorize(BaseModel):
    refresh_token: Token
    access_token: Token

class MessageResponse(BaseModel):
    message: str