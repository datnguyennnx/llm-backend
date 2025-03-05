from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Base repository interface"""
    
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save an entity"""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[T]:
        """Get entity by ID"""
        pass

    @abstractmethod
    async def list(self) -> List[T]:
        """List all entities"""
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Delete an entity"""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an entity"""
        pass