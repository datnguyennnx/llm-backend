from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities.content import Content

class ContentRepository(ABC):
    @abstractmethod
    async def save(self, content: Content) -> Content:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Content]:
        pass
    
    @abstractmethod
    async def get_by_url(self, url: str) -> Optional[Content]:
        pass

    @abstractmethod
    async def get_by_url_hash(self, url_hash: str) -> Optional[Content]:
        pass
    
    @abstractmethod
    async def get_by_source_id(self, source_id: UUID) -> List[Content]:
        pass
    
    @abstractmethod
    async def update_status(self, id: UUID, status: str) -> Content:
        pass

    @abstractmethod
    async def upsert(self, content: Content) -> Content:
        pass