from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ports.http.v1.schemas.sources import (
    SourceCreate, 
    SourceUpdate, 
    SourceResponse
)
from core.dependencies import get_session
from usecases.source_usecases import SourceUseCases
from adapters.repositories.sqlalchemy.source_repository import SQLAlchemySourceRepository

router = APIRouter()

async def get_source_usecases(
    session: AsyncSession = Depends(get_session)
) -> SourceUseCases:
    repository = SQLAlchemySourceRepository(session)
    return SourceUseCases(repository)

@router.post("/", response_model=SourceResponse)
async def create_source(
    source: SourceCreate,
    usecases: SourceUseCases = Depends(get_source_usecases)
):
    """Create a new source"""
    return await usecases.create_source(source.domain)

@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: UUID,
    usecases: SourceUseCases = Depends(get_source_usecases)
):
    """Get a source by ID"""
    source = await usecases.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source