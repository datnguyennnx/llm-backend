from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from usecases.dify_usecases import DifyUsecases
from adapters.dify_adapter import DifyAdapter
from core.dependencies import get_session
from usecases.source_usecases import SourceUseCases
from usecases.content_usecases import ContentUseCases
from usecases.chunk_usecases import ChunkUseCases
from ports.http.v1.schemas.dify import DifyWorkflowRequest
from adapters.repositories.sqlalchemy.content_repository import SQLAlchemyContentRepository
from adapters.repositories.sqlalchemy.source_repository import SQLAlchemySourceRepository
from adapters.repositories.sqlalchemy.chunk_repository import SQLAlchemyChunkRepository
from adapters.services.vector_service import OpenAIVectorService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

async def get_vector_service() -> OpenAIVectorService:
    return OpenAIVectorService(api_key=settings.OPENAI_API_KEY)

async def get_source_usecases(session: AsyncSession = Depends(get_session)) -> SourceUseCases:
    return SourceUseCases(SQLAlchemySourceRepository(session))

async def get_content_usecases(session: AsyncSession = Depends(get_session)) -> ContentUseCases:
    return ContentUseCases(SQLAlchemyContentRepository(session))

async def get_chunk_usecases(session: AsyncSession = Depends(get_session), vector_service: OpenAIVectorService = Depends(get_vector_service)) -> ChunkUseCases:
    return ChunkUseCases(SQLAlchemyChunkRepository(session), vector_service=vector_service)

@router.post("/run-workflow")
async def run_dify_workflow(
    request_data: DifyWorkflowRequest,
    source_usecases: SourceUseCases = Depends(get_source_usecases),
    content_usecases: ContentUseCases = Depends(get_content_usecases),
    chunk_usecases: ChunkUseCases = Depends(get_chunk_usecases)
):
    try:
        logger.info(f"Entering run_dify_workflow. Request data: {request_data}")
        dify_adapter = DifyAdapter()  # Initialize with API key from settings
        dify_usecases = DifyUsecases(dify_adapter, source_usecases, content_usecases, chunk_usecases)
        logger.info("Calling process_dify_workflow")
        result = await dify_usecases.process_dify_workflow(request_data.inputs, request_data.user)
        logger.info(f"Exiting run_dify_workflow. Result: {result}")
        return result  # Ensure result is returned

    except ValueError as ve:
        logger.error(f"ValueError in run_dify_workflow: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in run_dify_workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")