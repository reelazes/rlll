from pydantic import BaseModel, ConfigDict, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=72)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "bearer"