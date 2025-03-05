from typing import Dict, List, Optional
from uuid import UUID
from domain.entities.source import Source
from domain.entities.content import Content
from domain.entities.chunk import Chunk
from ports.repositories.source_repository import SourceRepository
from ports.repositories.content_repository import ContentRepository
from ports.repositories.chunk_repository import ChunkRepository

class InMemorySourceRepository(SourceRepository):
    def __init__(self):
        self.sources: Dict[UUID, Source] = {}
    
    async def save(self, source: Source) -> Source:
        self.sources[source.id] = source
        return source
    
    async def get_by_id(self, id: UUID) -> Optional[Source]:
        return self.sources.get(id)
    
    # ... implement other methods

class InMemoryContentRepository(ContentRepository):
    def __init__(self):
        self.contents: Dict[UUID, Content] = {}
    
    async def save(self, content: Content) -> Content:
        self.contents[content.id] = content
        return content
    
    # ... implement other methods

class InMemoryChunkRepository(ChunkRepository):
    def __init__(self):
        self.chunks: Dict[UUID, Chunk] = {}
    
    async def save(self, chunk: Chunk) -> Chunk:
        self.chunks[chunk.id] = chunk
        return chunk
    
    # ... implement other methods