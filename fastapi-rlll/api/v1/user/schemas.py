from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from core.models.user import USERNAME_MAX_LENGTH

Username = Annotated[str, Field(min_length=3, max_length=USERNAME_MAX_LENGTH)]


class UserCreate(BaseModel):
    username: Username
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password must not exceed 72 bytes")
        return v


class UserUpdate(BaseModel):
    username: Username


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "bearer"