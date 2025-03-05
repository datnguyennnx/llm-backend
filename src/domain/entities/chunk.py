from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from ..value_objects.embedding import Embedding

@dataclass
class Chunk:
    content_id: UUID
    sequence: int
    text: str
    embedding: Embedding | None = None
    token_count: int | None = None
    char_count: int | None = None
    embedding_model: str | None = None
    id: UUID = uuid4()
    created_at: datetime = datetime.now()