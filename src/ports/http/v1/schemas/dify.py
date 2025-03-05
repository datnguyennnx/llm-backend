from typing import Dict, Any
from pydantic import BaseModel

class DifyWorkflowRequest(BaseModel):
    inputs: Dict[str, Any]
    user: str