from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.source import Source
from ports.repositories.source_repository import SourceRepository
from .models import SourceModel


class SQLAlchemySourceRepository(SourceRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, source: Source) -> Source:
        source_model = SourceModel(
            id=source.id,
            domain=source.domain,
            is_active=source.is_active,
            last_crawled=source.last_crawled,
            created_at=source.created_at
        )
        self.session.add(source_model)
        await self.session.commit()
        await self.session.refresh(source_model)
        return self._to_entity(source_model)

    async def get_by_id(self, id: UUID) -> Optional[Source]:
        result = await self.session.execute(
            select(SourceModel).where(SourceModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_domain(self, domain: str) -> Optional[Source]:
        result = await self.session.execute(
            select(SourceModel).where(SourceModel.domain == domain)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_active_sources(self) -> List[Source]:
        result = await self.session.execute(
            select(SourceModel).where(SourceModel.is_active == True)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def list_active(self) -> List[Source]:
        return await self.get_active_sources()

    async def update(self, source: Source) -> Source:
        result = await self.session.execute(
            select(SourceModel).where(SourceModel.id == source.id)
        )
        source_model = result.scalar_one_or_none()
        if source_model:
            source_model.domain = source.domain
            source_model.is_active = source.is_active
            source_model.last_crawled = source.last_crawled
            await self.session.commit()
            await self.session.refresh(source_model)
        return self._to_entity(source_model) if source_model else None
    
    async def upsert(self, source: Source) -> Source:
        existing_source = await self.get_by_domain(source.domain)
        if existing_source:
            # Update existing source
            existing_source.is_active = source.is_active
            existing_source.last_crawled = source.last_crawled
            result = await self.session.execute(
                select(SourceModel).where(SourceModel.id == existing_source.id)
            )
            source_model = result.scalar_one_or_none()
            if source_model:
                source_model.domain = existing_source.domain
                source_model.is_active = existing_source.is_active
                source_model.last_crawled = existing_source.last_crawled
                await self.session.commit()
                await self.session.refresh(source_model)
            return self._to_entity(source_model) if source_model else None
        else:
            # Create new source
            source_model = SourceModel(
                id=source.id,
                domain=source.domain,
                is_active=source.is_active,
                last_crawled=source.last_crawled,
                created_at=source.created_at
            )
            self.session.add(source_model)
            await self.session.commit()
            await self.session.refresh(source_model)
            return self._to_entity(source_model)



    # Test comment

    def _to_entity(self, model: SourceModel) -> Source:
        return Source(
            id=model.id,
            domain=model.domain,
            is_active=model.is_active,
            last_crawled=model.last_crawled,
            created_at=model.created_at
        )