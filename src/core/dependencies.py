from typing import AsyncGenerator, Dict
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from adapters.repositories.sqlalchemy.base import Database
from adapters.services.vector_service import OpenAIVectorService
from ports.repositories.source_repository import SourceRepository
from ports.repositories.content_repository import ContentRepository
from ports.repositories.chunk_repository import ChunkRepository
from adapters.repositories.sqlalchemy.source_repository import SQLAlchemySourceRepository
from adapters.repositories.sqlalchemy.content_repository import SQLAlchemyContentRepository
from adapters.repositories.sqlalchemy.chunk_repository import SQLAlchemyChunkRepository

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Database(settings.DATABASE_URL).SessionLocal() as session:
        yield session

async def get_vector_service() -> OpenAIVectorService:
    return OpenAIVectorService(settings.OPENAI_API_KEY)

async def get_repositories(
    session: AsyncSession = Depends(get_session)
) -> Dict[str, SourceRepository | ContentRepository | ChunkRepository]:
    return {
        'source_repository': SQLAlchemySourceRepository(session),
        'content_repository': SQLAlchemyContentRepository(session),
        'chunk_repository': SQLAlchemyChunkRepository(session)
    }