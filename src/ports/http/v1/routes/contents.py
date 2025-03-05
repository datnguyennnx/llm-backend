from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ports.http.v1.schemas.sources import SourceResponse
from ports.http.v1.schemas.chunks import ChunkResponse
from ports.http.v1.schemas.contents import (
    ContentCreate, 
    ContentUpdate, 
    ContentResponse
)
from core.dependencies import get_session
from usecases import source_usecases, content_usecases, chunk_usecases
from usecases.content_usecases import ContentUseCases
from adapters.repositories.sqlalchemy.content_repository import SQLAlchemyContentRepository

router = APIRouter()

async def get_content_usecases(
    session: AsyncSession = Depends(get_session)
) -> ContentUseCases:
    repository = SQLAlchemyContentRepository(session)
    return ContentUseCases(repository)

@router.post("/", response_model=ContentResponse)
async def create_content(
    content: ContentCreate,
    usecases: ContentUseCases = Depends(get_content_usecases)
):
    """Create new content"""
    return await usecases.create_content(
        url=content.url,
        source_id=content.source_id
    )

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: UUID,
    usecases: ContentUseCases = Depends(get_content_usecases)
):
    """Get content by ID"""
    content = await usecases.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.get("/source/{source_id}", response_model=List[ContentResponse])
async def get_source_contents(
    source_id: UUID,
    usecases: ContentUseCases = Depends(get_content_usecases)
):
    """Get all contents for a source"""
    return await usecases.get_source_contents(source_id)

@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    content: ContentUpdate,
    usecases: ContentUseCases = Depends(get_content_usecases)
):
    """Update content"""
    updated_content = await usecases.update_content(
        id=content_id,
        raw_content=content.raw_content
    )
    if not updated_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated_content
    