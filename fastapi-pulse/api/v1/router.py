from fastapi import APIRouter
from api.v1.posts.router import router as posts_router
from api.v1.user.router import router as users_router

router = APIRouter()
router.include_router(posts_router)
router.include_router(users_router)