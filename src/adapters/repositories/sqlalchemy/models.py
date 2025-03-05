from sqlalchemy import (
    Column, DateTime, Boolean, String, Text, Integer, ForeignKey, Index
)
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector as VECTOR
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from .base import Base

class SourceModel(Base):
    __tablename__ = 'sources'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    domain = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    last_crawled = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    contents = relationship("ContentModel", back_populates="source")

class ContentModel(Base):
    __tablename__ = 'contents'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey('sources.id'))
    url = Column(Text, nullable=False)
    url_hash = Column(String(64), unique=True, nullable=False)
    raw_content = Column(Text)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    source = relationship("SourceModel", back_populates="contents")
    chunks = relationship("ChunkModel", back_populates="content")

    __table_args__ = (
        Index('ix_contents_url_hash', 'url_hash'),
        Index('ix_contents_source_id', 'source_id'),
        Index('ix_contents_status', 'status'),
    )

class ChunkModel(Base):
    __tablename__ = 'chunks'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey('contents.id'))
    sequence = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    token_count = Column(Integer)
    char_count = Column(Integer)
    embedding = Column(VECTOR(1536))
    embedding_model = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    content = relationship("ContentModel", back_populates="chunks")