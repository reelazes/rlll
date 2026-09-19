from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user import service
from api.v1.user.dependencies import get_current_user
from api.v1.user.schemas import TokenInfo, UserCreate, UserRead, UserUpdate
from core.models import User, db_helper

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=UserRead)
async def register(
        user: UserCreate,
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


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service.update_username(session, current_user, user_in.username)
    except service.UserAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Username already taken")
