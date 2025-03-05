import httpx
import json
from typing import Dict, Any
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class DifyAdapter:
    def __init__(self, api_key: str = None):
        self.base_url = "https://api.dify.ai/v1"
        self.api_key = api_key or settings.DIFY_API_KEY
        if not self.api_key:
            raise ValueError("Dify API key is required")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def run_workflow(self, inputs: Dict[str, Any], user: str, response_mode: str = "blocking") -> Dict[str, Any]:
        url = f"{self.base_url}/workflows/run"
        data = { 
            "inputs": inputs,
            "user": user,
            "response_mode": response_mode
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, json=data, timeout=120) # Increased timeout
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Dify API request failed: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Dify API request failed: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Dify API request failed: {e}")
            raise Exception(f"Dify API request failed: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise