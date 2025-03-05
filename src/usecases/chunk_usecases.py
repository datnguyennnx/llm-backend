from typing import List, Optional, Tuple
from uuid import UUID, uuid4
import numpy as np

from domain.entities.chunk import Chunk
from ports.repositories.chunk_repository import ChunkRepository
from ports.services.vector_service import VectorService

class ChunkUseCases:
    def __init__(
        self,
        chunk_repository: ChunkRepository, vector_service: VectorService
    ):
        self.chunk_repository = chunk_repository
        self.vector_service = vector_service

    async def create_chunk_with_embedding(
        self,
        content_id: UUID,
        sequence: int,
        text: str
    ) -> Chunk:
        # Generate embedding
        embedding = await self.vector_service.generate_embedding(text)

        # Create chunk with a new UUID
        chunk = Chunk(
            id=uuid4(),  # Generate a new UUID here
            content_id=content_id,
            sequence=sequence,
            text=text,
            embedding=embedding.vector,
            embedding_model=self.vector_service.model
        )
        
        # Save chunk
        saved_chunk = await self.chunk_repository.create(chunk)
        return saved_chunk

    async def find_similar_chunks(
        self,
        query_text: str,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Tuple[Chunk, float]]:
        # Generate query embedding
        query_vector = await self.vector_service.generate_embedding(query_text)
        
        # Find similar chunks
        similar_chunks = await self.chunk_repository.find_similar(
            query_vector,
            limit=limit,
            threshold=threshold
        )
        
        return similar_chunks