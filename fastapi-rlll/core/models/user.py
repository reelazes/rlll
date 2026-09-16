from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))

    posts: Mapped[list["Post"]] = relationship(back_populates="author")