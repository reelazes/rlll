from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.user.dependencies import get_current_user
from core.models import db_helper
from core.models.user import User
from api.v1.posts.schemas import PostCreate, PostRead, PostUpdate
from api.v1.posts import service

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_in: PostCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await service.create_post(session, post_in, current_user.id)


@router.get("/", response_model=list[PostRead])
async def get_posts(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await service.get_all_posts(session, limit, offset)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service.get_post(session, post_id)
    except service.PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")


@router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        return await service.update_post(session, post_id, post_in, current_user.id)
    except service.PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except service.PostForbiddenError:
        raise HTTPException(status_code=403, detail="Not your post")


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        await service.delete_post(session, post_id, current_user.id)
    except service.PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except service.PostForbiddenError:
        raise HTTPException(status_code=403, detail="Not your post")