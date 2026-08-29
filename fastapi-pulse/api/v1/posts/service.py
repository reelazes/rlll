from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.posts import repository
from api.v1.posts.schemas import PostCreate
from core.models.post import Post


class PostNotFoundError(Exception):
    pass


async def create_post(session: AsyncSession, post_in: PostCreate) -> Post:
    return await repository.create(session, post_in)


async def get_post(session: AsyncSession, post_id: int) -> Post:
    post = await repository.get_by_id(session, post_id)
    if post is None:
        raise PostNotFoundError(f"Post {post_id} not found")
    return post


async def get_all_posts(session: AsyncSession) -> list[Post]:
    return await repository.get_all(session)


async def delete_post(session: AsyncSession, post_id: int) -> None:
    post = await get_post(session, post_id)
    await repository.delete(session, post)