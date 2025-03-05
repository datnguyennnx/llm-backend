from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from .base import BaseResponse

class SourceBase(BaseModel):
    domain: str

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    is_active: Optional[bool] = None

class SourceResponse(SourceBase, BaseResponse):
    is_active: bool
    last_crawled: Optional[datetime]