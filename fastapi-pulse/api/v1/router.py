from fastapi import APIRouter
from api.v1.posts.router import router as posts_router

router = APIRouter()
router.include_router(posts_router)