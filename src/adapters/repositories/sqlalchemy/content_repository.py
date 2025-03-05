from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from domain.entities.content import Content
from ports.repositories.content_repository import ContentRepository, ABC
from .models import ContentModel

class SQLAlchemyContentRepository(ContentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, content: Content) -> Content:
        content_model = await self._get_by_url_hash(content.url_hash)
        
        if content_model:
            # Update existing model
            content_model.url = content.url
            content_model.source_id = content.source_id
            content_model.raw_content = content.raw_content
            content_model.status = content.status
        else:
            # Create new model
            content_model = ContentModel(
                id=content.id,
                url=content.url,
                url_hash=content.url_hash,
                source_id=content.source_id,
                raw_content=content.raw_content,
                status=content.status,
                created_at=content.created_at
            )
            self.session.add(content_model)

        await self.session.commit()
        await self.session.refresh(content_model)
        return self._to_entity(content_model)

    async def get_by_id(self, id: UUID) -> Optional[Content]:
        content_model = await self._get_by_id(id)
        return self._to_entity(content_model) if content_model else None

    async def get_by_url(self, url: str) -> Optional[Content]:
        content_model = await self._get_by_url(url)
        return self._to_entity(content_model) if content_model else None

    async def _get_by_url(self, url:str) -> Optional[ContentModel]:
         result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.url == url)
        )
         return result.scalar_one_or_none()

    async def get_by_source_id(self, source_id: UUID) -> List[Content]:
        result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.source_id == source_id)
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def update_status(self, id: UUID, status: str) -> Optional[Content]:
        stmt = (
            update(ContentModel)
            .where(ContentModel.id == id)
            .values(status=status)
            .returning(ContentModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()

        content_model = result.scalar_one_or_none()
        return self._to_entity(content_model) if content_model else None

    async def get_by_status(self, status: str) -> List[Content]:
        result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.status == status)
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def _get_by_id(self, id: UUID) -> Optional[ContentModel]:
        result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.id == id)
        )
        return result.scalar_one_or_none()

    async def _get_by_url_hash(self, url_hash: str) -> Optional[ContentModel]:
        result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.url_hash == url_hash)
        )
        return result.scalar_one_or_none()

    def _to_entity(self, model: ContentModel) -> Content:
        return Content(
            id=model.id,
            url=model.url,
            url_hash=model.url_hash,
            source_id=model.source_id,
            raw_content=model.raw_content,
            status=model.status,
            created_at=model.created_at
        )

    async def get_pending_contents(self, limit: int = 10) -> List[Content]:
        result = await self.session.execute(
            select(ContentModel)
            .where(ContentModel.status == 'pending')
            .limit(limit)
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def batch_save(self, contents: List[Content]) -> List[Content]:
        content_models = []
        for content in contents:
            content_model = ContentModel(
                id=content.id,
                url=content.url,
                url_hash=content.url_hash,
                source_id=content.source_id,
                raw_content=content.raw_content,
                status=content.status,
                created_at=content.created_at
            )
            content_models.append(content_model)

        self.session.add_all(content_models)
        await self.session.commit()
        
        for model in content_models:
            await self.session.refresh(model)
        
        return [self._to_entity(model) for model in content_models]

    async def delete(self, id: UUID) -> bool:
        content_model = await self._get_by_id(id)
        if content_model:
            await self.session.delete(content_model)
            await self.session.commit()
            return True
        return False

    async def upsert(self, content: Content) -> Content:
        stmt = (
            insert(ContentModel)
            .values(
                id=content.id,
                url=content.url,
                url_hash=content.url_hash,
                source_id=content.source_id,
                raw_content=content.raw_content,
                status=content.status,
                created_at=content.created_at,
            )
            .on_conflict_do_update(
                index_elements=[ContentModel.url_hash],
                set_={
                    "url": content.url,
                    "url_hash": content.url_hash,
                    "source_id": content.source_id,
                    "raw_content": content.raw_content,
                    "status": content.status,
                },
            )
            .returning(ContentModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        content_model = result.scalar_one_or_none()
        if content_model is None:
            raise Exception("Upsert failed")  # Should not happen
        return self._to_entity(content_model)

    async def get_by_url_hash(self, url_hash: str) -> Optional[Content]:
        content_model = await self._get_by_url_hash(url_hash)
        return self._to_entity(content_model) if content_model else None