from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.v1.posts.schemas import PostCreate, PostRead
from api.v1.posts import service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await service.create_post(session, post_in)


@router.get("/", response_model=list[PostRead])
async def get_posts(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await service.get_all_posts(session)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service.get_post(session, post_id)
    except service.PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        await service.delete_post(session, post_id)
    except service.PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")