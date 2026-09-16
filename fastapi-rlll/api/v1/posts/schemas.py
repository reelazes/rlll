from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

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