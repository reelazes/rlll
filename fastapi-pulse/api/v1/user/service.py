from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import repository
from api.v1.user.schemas import CreateUser
from auth.utils import hash_password
from core.models.user import User

async def create_user(session: AsyncSession, user: CreateUser) -> User:
    hashed_password = hash_password(user.password)
    return await repository.create(session, user.username, hashed_password)
