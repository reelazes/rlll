from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User

async def create(session: AsyncSession, username, hashed_password) -> User:
    user = User(username=username, hash_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user