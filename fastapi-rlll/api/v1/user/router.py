from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.v1.user.schemas import CreateUser, TokenInfo, UserRead
from api.v1.user import service, schemas

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserRead)
async def register(
        user: CreateUser,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    try:
        return await service.create_user(session, user)
    except service.UserAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Username already taken")


@router.post("/login", response_model=TokenInfo)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        token = await service.login(session, form_data.username, form_data.password)
    except service.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenInfo(access_token=token)




