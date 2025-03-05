from typing import List, Optional
from uuid import UUID
from domain.entities.source import Source
from ports.repositories.source_repository import SourceRepository

class SourceUseCases:
    def __init__(self, source_repository: SourceRepository):
        self.source_repository = source_repository
    
    async def create(self, domain: str) -> Source:
        source = Source(domain=domain)
        return await self.source_repository.create(source)
    
    async def get_source(self, id: UUID) -> Optional[Source]:
        return await self.source_repository.get_by_id(id)
    
    async def get_active_sources(self) -> List[Source]:
        return await self.source_repository.get_active_sources()
    
    async def deactivate_source(self, id: UUID) -> Optional[Source]:
        source = await self.source_repository.get_by_id(id)
        if source:
            source.deactivate()
            return await self.source_repository.create(source)

    async def upsert(self, domain: str) -> Source:
        source = Source(domain=domain)
        return await self.source_repository.upsert(source)
        return None