from __future__ import annotations

import base64
import json
from typing import Any

import httpx

from .config import settings


async def embed_text(texts: list[str], model: str | None = None) -> list[list[float]]:
    model = model or settings.embed_model
    if not settings.nvidia_api_key:
        raise RuntimeError("NVIDIA_API_KEY required for embedding. Set via env or config.")
    payload = {
        "model": model,
        "input": texts,
        "input_type": "query" if len(texts) == 1 else "passage",
        "encoding_format": "float",
        "truncate": "END",
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{settings.nvidia_base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {settings.nvidia_api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
    embeddings = []
    for item in data.get("data", []):
        emb = item.get("embedding")
        if emb:
            embeddings.append(emb)
    if len(embeddings) != len(texts):
        raise RuntimeError(f"Embedding count mismatch: got {len(embeddings)}, expected {len(texts)}")
    return embeddings


async def embed_image(image_bytes: bytes, text_prompt: str, model: str | None = None) -> list[float]:
    model = model or settings.vl_embed_model
    if not settings.nvidia_api_key:
        raise RuntimeError("NVIDIA_API_KEY required for VL embedding.")
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "model": model,
        "input": [
            {
                "type": "image_url",
                "url": f"data:image/jpeg;base64,{b64}",
            },
            {
                "type": "text",
                "text": text_prompt,
            },
        ],
        "encoding_format": "float",
        "truncate": "END",
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{settings.nvidia_base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {settings.nvidia_api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
    for item in data.get("data", []):
        emb = item.get("embedding")
        if emb:
            return emb
    raise RuntimeError("No embedding returned from VL model")