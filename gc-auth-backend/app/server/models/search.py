import os
import asyncio
import httpx
from typing import List, Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.models.user import User

MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017/gc25")
EMBEDDING_URL = os.getenv("EMBEDDING_URL", "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy_hf_token")

async def init():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.get_database(), document_models=[User])

async def generate_embedding(text: str) -> Optional[List[float]]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                EMBEDDING_URL,
                json={"inputs": text},
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                timeout=10.0
            )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"Error generating embedding for '{text}': {e}")
        return None

async def vector_search(query: str, num_results: int = 20):
    await init()

    query_embedding = await generate_embedding(query)
    if not query_embedding:
        print("Failed to generate query embedding")
        return

    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "vectorEmbedding",
                "numCandidates": num_results * 2,
                "limit": num_results,
                "index": "vector_index",
                "similarity": "dotProduct"
            }
        },
        {
            "$project": {
                "_id":0,
                "vectorEmbedding":0
            }
        }
    ]

    results = await User.get_motor_collection().aggregate(pipeline).to_list(length=num_results)
    return results