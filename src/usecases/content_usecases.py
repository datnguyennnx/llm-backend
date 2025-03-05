from typing import List, Optional
from uuid import UUID
from domain.entities.content import Content
import hashlib
from ports.repositories.content_repository import ContentRepository
import logging

logger = logging.getLogger(__name__)

class ContentUseCases:
    def __init__(self, content_repository: ContentRepository):
        self.content_repository = content_repository
    
    async def create(self, url: str, source_id: UUID) -> Content:
        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        content = Content(url=url, source_id=source_id, url_hash=url_hash)
        logger.info(f'{content=}')
        return await self.content_repository.save(content)
    
    async def update(self, id: UUID, raw_content: str) -> Optional[Content]:
        content = await self.content_repository.get_by_id(id)
        if content:
            content.update_content(raw_content)
            return await self.content_repository.save(content)
        return None
    
    async def get_source(self, source_id: UUID) -> List[Content]:
        return await self.content_repository.get_by_source_id(source_id)

    async def upsert(self, url: str, source_id: UUID) -> Content:
        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        content = await self.content_repository.get_by_url_hash(url_hash)
        if content:
            content.source_id = source_id
            content.url = url  # Ensure URL is updated
            # We assume other fields like status might need updating
            return await self.content_repository.upsert(content)
        else:
            content = Content(url=url, source_id=source_id, url_hash=url_hash)
            return await self.content_repository.upsert(content)