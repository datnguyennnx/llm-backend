from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Source:
    domain: str
    is_active: bool = True
    id: UUID = uuid4()
    last_crawled: datetime | None = None
    created_at: datetime = datetime.now()