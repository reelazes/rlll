from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.post import Post
from api.v1.posts.schemas import PostCreate


async def create(session: AsyncSession, post_in: PostCreate) -> Post:
    post = Post(**post_in.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_by_id(session: AsyncSession, post_id: int) -> Post | None:
    result = await session.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[Post]:
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    return list(result.scalars().all())


async def delete(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()