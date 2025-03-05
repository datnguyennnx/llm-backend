from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ports.http.v1.schemas.chunks import (
    ChunkCreate, 
    ChunkResponse, 
    SimilaritySearch, 
    SimilarityResult
)
from core.dependencies import get_session, get_vector_service
from usecases.chunk_usecases import ChunkUseCases
from adapters.repositories.sqlalchemy.chunk_repository import SQLAlchemyChunkRepository
from adapters.services.vector_service import OpenAIVectorService

router = APIRouter()

async def get_chunk_usecases(
    session: AsyncSession = Depends(get_session),
    vector_service: OpenAIVectorService = Depends(get_vector_service)
) -> ChunkUseCases:
    repository = SQLAlchemyChunkRepository(session)
    return ChunkUseCases(repository, vector_service)

@router.post("/", response_model=ChunkResponse)
async def create_chunk(
    chunk: ChunkCreate,
    usecases: ChunkUseCases = Depends(get_chunk_usecases)
):
    return await usecases.create_chunk_with_embedding(
        content_id=chunk.content_id,
        sequence=chunk.sequence,
        text=chunk.text
    )

@router.post("/search", response_model=List[SimilarityResult])
async def search_similar_chunks(
    search: SimilaritySearch,
    usecases: ChunkUseCases = Depends(get_chunk_usecases)
):
    results = await usecases.find_similar_chunks(
        query_text=search.text,
        limit=search.limit,
        threshold=search.threshold
    )
    return [
        SimilarityResult(chunk=chunk, similarity=similarity)
        for chunk, similarity in results
    ]

@router.get("/content/{content_id}", response_model=List[ChunkResponse])
async def get_content_chunks(
    content_id: UUID,
    usecases: ChunkUseCases = Depends(get_chunk_usecases)
):
    return await usecases.get_chunks_by_content(content_id)