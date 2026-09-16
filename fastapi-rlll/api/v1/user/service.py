from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import repository
from api.v1.user.schemas import CreateUser
from auth.utils import create_access_token, hash_password, validate_password
from core.models.user import User

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass



async def create_user(session: AsyncSession, user: CreateUser) -> User:
    existing = await repository.get_by_username(session, user.username)
    if existing is not None:
        raise UserAlreadyExistsError(f"User {user.username} already exists")

    hashed_password = hash_password(user.password)
    try:
        return await repository.create(session, user.username, hashed_password)
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExistsError(f"User {user.username} already exists")

async def login(session: AsyncSession, username: str, password: str) -> str:
    user = await repository.get_by_username(session, username)
    if user is None:
        raise InvalidCredentialsError("Invalid username or password")

    if not validate_password(password, user.hash_password):
        raise InvalidCredentialsError("Invalid username or password")

    return create_access_token(user.id, user.username)



