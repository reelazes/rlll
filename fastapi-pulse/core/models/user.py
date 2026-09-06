from datetime import datetime
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from core.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))