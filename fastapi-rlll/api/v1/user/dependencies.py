import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import repository
from auth.utils import decode_jwt
from core.models import db_helper
from core.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt(token)
    except jwt.InvalidTokenError:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = await repository.get_by_id(session, int(user_id))
    if user is None:
        raise credentials_error

    return user