from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.post import Post

USERNAME_MAX_LENGTH = 30


class User(Base):
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    posts: Mapped[list["Post"]] = relationship(back_populates="author")