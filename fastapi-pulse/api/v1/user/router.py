from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.v1.user.schemas import CreateUser, UserRead
from api.v1.user import service, schemas

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register",response_model=UserRead)
async def register(
        user: CreateUser,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    return await service.create_user(session, user)





