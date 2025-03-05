from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl
from .base import BaseResponse

from typing import List
from .sources import SourceCreate

class ContentBase(BaseModel):
    url: str
    source_id: UUID    

class ContentCreate(ContentBase):
    raw_content: Optional[str] = None

class ContentUpdate(BaseModel):
    pass

class ContentResponse(ContentBase, BaseResponse):
    url_hash: str
    raw_content: Optional[str]
    status: str