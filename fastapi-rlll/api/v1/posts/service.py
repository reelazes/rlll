from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.posts import repository
from api.v1.posts.schemas import PostCreate, PostUpdate
from core.models.post import Post


class PostNotFoundError(Exception):
    pass


class PostForbiddenError(Exception):
    pass


async def create_post(session: AsyncSession, post_in: PostCreate, user_id: int) -> Post:
    return await repository.create(session, post_in, user_id)


async def get_post(session: AsyncSession, post_id: int) -> Post:
    post = await repository.get_by_id(session, post_id)
    if post is None:
        raise PostNotFoundError(f"Post {post_id} not found")
    return post


async def get_all_posts(session: AsyncSession, limit: int, offset: int) -> list[Post]:
    return await repository.get_all(session, limit, offset)


async def update_post(
        session: AsyncSession, post_id: int, post_in: PostUpdate, user_id: int
) -> Post:
    post = await get_post(session, post_id)
    if post.user_id != user_id:
        raise PostForbiddenError(f"User {user_id} cannot edit post {post_id}")
    return await repository.update(session, post, post_in)


async def delete_post(session: AsyncSession, post_id: int, user_id: int) -> None:
    post = await get_post(session, post_id)
    if post.user_id != user_id:
        raise PostForbiddenError(f"User {user_id} cannot delete post {post_id}")
    await repository.delete(session, post)