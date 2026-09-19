from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from core.models.post import TITLE_MAX_LENGTH

CONTENT_MAX_LENGTH = 10_000

Title = Annotated[str, Field(min_length=1, max_length=TITLE_MAX_LENGTH)]
Content = Annotated[str, Field(min_length=1, max_length=CONTENT_MAX_LENGTH)]


class PostCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Title
    content: Content


class PostUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Title | None = None
    content: Content | None = None

    @field_validator("title", "content")
    @classmethod
    def not_null(cls, v: str | None) -> str | None:
        if v is None:
            raise ValueError("cannot be null")
        return v


class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int