from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User

async def create(session: AsyncSession, username, hashed_password) -> User:
    user = User(username=username, hash_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)