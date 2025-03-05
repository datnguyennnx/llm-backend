from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities.source import Source

class SourceRepository(ABC):
    @abstractmethod
    async def create(self, source: Source) -> Source:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Source]:
        pass

    @abstractmethod
    async def get_by_domain(self, domain: str) -> Optional[Source]:
        pass

    @abstractmethod
    async def update(self, source: Source) -> Source:
        pass

    @abstractmethod
    async def list_active(self) -> List[Source]:
        pass