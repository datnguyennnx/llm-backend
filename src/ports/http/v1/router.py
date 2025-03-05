from fastapi import APIRouter
from .routes import sources, contents, chunks, dify

router = APIRouter()

router.include_router(
    sources.router,
    prefix="/sources",
    tags=["sources"]
)

router.include_router(
    contents.router,
    prefix="/contents",
    tags=["contents"]
)

router.include_router(
    chunks.router,
    prefix="/chunks",
    tags=["chunks"]
)

router.include_router(
    dify.router,
    prefix="/dify",
    tags=["dify"]
)