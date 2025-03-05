from abc import ABC, abstractmethod
from typing import List
import numpy as np
from domain.value_objects.embedding import Embedding

class VectorService(ABC):
    @abstractmethod
    async def generate_embedding(self, text: str) -> Embedding:
        pass
    
    @abstractmethod
    async def batch_generate_embeddings(self, texts: List[str]) -> List[Embedding]:
        pass
    
    @abstractmethod
    async def compute_similarity(self, embedding1: Embedding, embedding2: Embedding) -> float:
        pass