from datetime import date, datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.config import settings
from src.schemas.common import Token


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreateBase(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: EmailStr
    phoneNum: Optional[str] = None
    birthday: Optional[date] = None
    username: Optional[str] = None
    subscribed_for_newsletter: Optional[bool] = False


class UserCreateResponse(BaseModel):
    message: str
    refresh_token: Token
    access_token: Token
    user: Optional[UserCreateBase]


class UserCreateRequest(UserBase, UserCreateBase):
    password_confirmation: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, password):
        min_length = 8
        errors = []

        if len(password) < min_length:
            errors.append("Password must be at least 8 characters long.")

        if not any(character.islower() for character in password):
            errors.append("Password should contain at least one lowercase character.")

        if errors:
            raise ValueError(". ".join(errors))

        return password

    @field_validator("password_confirmation", mode="before")
    @classmethod
    def validate_password_confirmation(cls, password_confirmation: str, info: FieldValidationInfo, **kwargs):
        if "password" in info.data and password_confirmation != info.data["password"]:
            raise ValueError("Passwords do not match")
        return password_confirmation

    @field_validator("birthday", mode="before")
    @classmethod
    def validate_birthday(cls, value):
        if isinstance(value, str):
            date_format = "%Y-%m-%d"
            try:
                birthday_datetime = datetime.strptime(value, date_format).date()
            except ValueError:
                raise ValueError("Invalid date format.")
            age_delta = relativedelta(date.today(), birthday_datetime)
            age = age_delta.years
            if age < settings.MIN_AGE:
                raise ValueError("User must be at least 13 y.o.")
        return value
