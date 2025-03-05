from typing import List, Optional, Tuple
from uuid import UUID
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from domain.entities.chunk import Chunk
from ports.repositories.chunk_repository import ChunkRepository
from .models import ChunkModel

class SQLAlchemyChunkRepository(ChunkRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, chunk: Chunk) -> Chunk:
        chunk_model = ChunkModel(
            id=chunk.id,
            content_id=chunk.content_id,
            sequence=chunk.sequence,
            text=chunk.text,
            token_count=chunk.token_count,
            char_count=chunk.char_count,
            embedding=chunk.embedding.tolist() if chunk.embedding is not None else None,
            embedding_model=chunk.embedding_model
        )
        self.session.add(chunk_model)
        await self.session.commit()
        await self.session.refresh(chunk_model)
        return self._to_entity(chunk_model)

    async def batch_create(self, chunks: List[Chunk]) -> List[Chunk]:
        chunk_models = [
            ChunkModel(
                id=chunk.id,
                content_id=chunk.content_id,
                sequence=chunk.sequence,
                text=chunk.text,
                token_count=chunk.token_count,
                char_count=chunk.char_count,
                embedding=chunk.embedding.tolist() if chunk.embedding is not None else None,
                embedding_model=chunk.embedding_model
            )
            for chunk in chunks
        ]
        self.session.add_all(chunk_models)
        await self.session.commit()
        return [self._to_entity(chunk_model) for chunk_model in chunk_models]


    async def find_similar(
        self,
        query_vector: np.ndarray,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Tuple[Chunk, float]]:
        vector_list = query_vector.tolist()
        stmt = (
            select(ChunkModel, func.cosine_similarity(ChunkModel.embedding, vector_list))
            .filter(func.cosine_similarity(ChunkModel.embedding, vector_list) >= threshold)
            .order_by(func.cosine_similarity(ChunkModel.embedding, vector_list).desc())
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        # Fetch all results as tuples of (ChunkModel, similarity)
        results = result.all()

        return [
            (
                self._to_entity(chunk_model),
                float(similarity)
            )
            for chunk_model, similarity in results
        ]

    async def get_by_content_id(self, content_id: UUID) -> List[Chunk]:
        result = await self.session.execute(
            select(ChunkModel).where(ChunkModel.content_id == content_id)
        )
        chunks = result.scalars().all()
        return [self._to_entity(chunk) for chunk in chunks]

    def _to_entity(self, chunk: ChunkModel) -> Chunk:
        return Chunk(
            id=chunk.id,
            content_id=chunk.content_id,
            sequence=chunk.sequence,
            text=chunk.text,
            embedding=np.array(chunk.embedding) if chunk.embedding is not None else None,
            token_count=chunk.token_count,
            char_count=chunk.char_count,
            embedding_model=chunk.embedding_model,
            created_at=chunk.created_at
        )