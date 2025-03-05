from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Content:
    url: str
    url_hash: str
    source_id: UUID
    raw_content: str | None = None
    status: str = "pending"
    id: UUID = uuid4()
    created_at: datetime = datetime.now()