from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import repository
from api.v1.user.schemas import UserCreate
from auth.utils import create_access_token, hash_password, validate_password
from core.models.user import User

class UserAlreadyExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass



async def create_user(session: AsyncSession, user: UserCreate) -> User:
    existing = await repository.get_by_username(session, user.username)
    if existing is not None:
        raise UserAlreadyExistsError(f"User {user.username} already exists")

    password_hash = hash_password(user.password)
    try:
        return await repository.create(session, user.username, password_hash)
    except IntegrityError:
        await session.rollback()
        raise UserAlreadyExistsError(f"User {user.username} already exists")

async def login(session: AsyncSession, username: str, password: str) -> str:
    user = await repository.get_by_username(session, username)
    if user is None:
        raise InvalidCredentialsError("Invalid username or password")

    if not validate_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid username or password")

    return create_access_token(user.id, user.username)


async def update_username(
    session: AsyncSession, current_user: User, new_username: str
) -> User:
    existing = await repository.get_by_username(session, new_username)
    if existing is not None:
        raise UserAlreadyExistsError(f"User {new_username} already exists")
    return await repository.update_username(session, current_user, new_username)
