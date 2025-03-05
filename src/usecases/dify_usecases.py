from typing import Dict, Any
from adapters.dify_adapter import DifyAdapter
import re
from usecases.source_usecases import SourceUseCases
import json
from usecases.content_usecases import ContentUseCases
from usecases.chunk_usecases import ChunkUseCases
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)

class DifyUsecases:
    def __init__(self, dify_adapter: DifyAdapter, source_usecases: SourceUseCases, content_usecases: ContentUseCases, chunk_usecases: ChunkUseCases):
        self.dify_adapter = dify_adapter
        self.source_usecases = source_usecases
        self.content_usecases = content_usecases
        self.chunk_usecases = chunk_usecases

    async def process_dify_workflow(self, inputs: Dict[str, Any], user: str):
        content_url = inputs.get('url')
        source_domain = content_url.split("//")[-1].split("/")[0] if content_url else "unknown"
        try:
            dify_response = await self.dify_adapter.run_workflow(inputs=inputs, user=user)
            logger.info(f"Dify workflow response: {dify_response}")

            if 'data' not in dify_response:
                logger.error(f"Invalid Dify response format: {dify_response}")
                raise ValueError("Invalid Dify response format: missing 'data' field")
            
            dify_data = dify_response['data']

            if not isinstance(dify_data, dict) or 'outputs' not in dify_data or 'output' not in dify_data['outputs']:
                logger.error(f"Invalid Dify response data format: {dify_data}")
                raise ValueError("Invalid Dify response data format: missing 'outputs' or 'text' field")
            
            workflow_output = dify_data['outputs']['output']

            if isinstance(workflow_output, str):
                try:
                    workflow_output = json.loads(workflow_output.strip())
                except json.JSONDecodeError as e:
                    logger.error(f"Dify workflow returned invalid JSON: {workflow_output} - {e}")                    
                    raise ValueError(f"Dify workflow returned invalid JSON: {workflow_output}") from e
            
            urls = workflow_output.get('url', [])
            contents = workflow_output.get('contents', [])
            
            if not isinstance(urls, list) or not isinstance(contents, list) or len(urls) != len(contents):
                raise ValueError("Invalid Dify response: 'url' and 'contents' must be lists of the same length.")

            results = []            
            for url, content_text in zip(urls, contents):
                domain = url.split("//")[-1].split("/")[0] if url else "unknown"
                source = await self.source_usecases.upsert(domain=domain)
                content = await self.content_usecases.upsert(url=url, source_id=source.id)
                markdown_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=600,
                    chunk_overlap=60,
                    separators=[
                        "\\n## ",
                        "\\n### ",
                        "\\n- ",
                        "\\n\\n",
                        "\\n",
                        ". ",
                        " ",
                        ""
                    ]
                )

                chunks = markdown_splitter.split_text(content_text)
                for j, chunk_text in enumerate(chunks):
                    chunk = await self.chunk_usecases.create_chunk_with_embedding(content_id=content.id, sequence=j + 1, text=chunk_text)
                    results.append({"source_id": source.id, "content_id": content.id, "chunk_id": chunk.id})

            return results
        except Exception as e:
            logger.error(f"Error processing Dify workflow: {e}")
            raise
