from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from uuid import UUID
from domain.entities.chunk import Chunk
from domain.value_objects.embedding import Embedding

class ChunkRepository(ABC):
    @abstractmethod
    async def create(self, chunk: Chunk) -> Chunk:
        pass

    @abstractmethod
    async def batch_create(self, chunks: List[Chunk]) -> List[Chunk]:
        pass

    @abstractmethod
    async def find_similar(
        self, 
        embedding: Embedding, 
        limit: int = 10, 
        threshold: float = 0.7
    ) -> List[Tuple[Chunk, float]]:
        pass

    @abstractmethod
    async def get_by_content_id(self, content_id: UUID) -> List[Chunk]:
        pass