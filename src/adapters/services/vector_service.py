from typing import List
import numpy as np
from openai import AsyncOpenAI
from domain.value_objects.embedding import Embedding
from ports.services.vector_service import VectorService

class OpenAIVectorService(VectorService):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "text-embedding-ada-002"
    
    async def generate_embedding(self, text: str) -> Embedding:
        response = await self.client.embeddings.create(
            input=text,
            model=self.model
        )
        vector = np.array(response.data[0].embedding)
        return Embedding(vector=vector, model=self.model)
    
    async def batch_generate_embeddings(self, texts: List[str]) -> List[Embedding]:
        response = await self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return [
            Embedding(
                vector=np.array(data['embedding']),
                model=self.model
            )
            for data in response['data']
        ]
    
    async def compute_similarity(self, embedding1: Embedding, embedding2: Embedding) -> float:
        return float(np.dot(embedding1.vector, embedding2.vector) / 
                    (np.linalg.norm(embedding1.vector) * np.linalg.norm(embedding2.vector)))