from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

class ChunkBase(BaseModel):
    content_id: UUID
    sequence: int
    text: str

class ChunkCreate(ChunkBase):
    pass

class ChunkUpdate(BaseModel):
    embedding_model: Optional[str] = None

class ChunkResponse(ChunkBase):
    id: UUID
    token_count: Optional[int]
    char_count: Optional[int]
    embedding_model: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class SimilaritySearch(BaseModel):
    text: str
    limit: Optional[int] = 10
    threshold: Optional[float] = 0.7

class SimilarityResult(BaseModel):
    chunk: ChunkResponse
    similarity: float