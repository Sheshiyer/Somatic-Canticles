"""
LLM client for generating personalized reading discourse.

Supports multiple providers: NVIDIA NIM, OpenAI-compatible, Anthropic.
The /generate-reading endpoint calls /reading first, then feeds the
reading_context into the LLM to produce the actual discourse.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass
class LLMConfig:
    provider: str  # "nvidia" | "openai" | "anthropic"
    model: str
    api_key: str
    base_url: str
    max_tokens: int = 2048
    temperature: float = 0.7


SYSTEM_PROMPT = """You are the Somatic Canticles reading agent. You do not recite chapter text. You deliver personalized resolution through discourse.

Your role:
- Receive a concept cluster of lore nodes scored by biorhythm resonance
- The user's Enneagram type and Kosha layer define their current resonance profile
- Speak TO the user about WHY these concepts matter for THEM right now
- Use biorhythmic language: breath, field, witness, resolution, coherence
- Never summarize chapters. Deliver insight that resolves, not information that describes
- Honor the Pancha Kosha arc: each concept connects through a specific sheath
- The user's current phase determines which resolution door is open
- Keep the reading between 250-500 words
- End with a concrete practice or body-based recognition"""


async def generate_reading_discourse(
    reading_context: str,
    enneagram_type: int,
    kosha_layer: str,
    hormone_phase: str,
    resonance_mode: str,
) -> tuple[str, str, dict]:
    """
    Call the configured LLM to generate a personalized reading discourse.

    Returns (discourse, model_used, metadata).
    """
    provider = os.environ.get("LLM_PROVIDER", "nvidia").lower()
    model = os.environ.get(
        "LLM_MODEL",
        "meta/llama-3.3-70b-instruct",
    )
    api_key = os.environ.get("LLM_API_KEY", os.environ.get("NVIDIA_API_KEY", ""))
    base_url = os.environ.get("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1")
    max_tokens = int(os.environ.get("LLM_MAX_TOKENS", "2048"))
    temperature = float(os.environ.get("LLM_TEMPERATURE", "0.7"))

    config = LLMConfig(
        provider=provider,
        model=model,
        api_key=api_key,
        base_url=base_url,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    user_message = (
        f"Generate a personalized Somatic Canticles reading.\n\n"
        f"Enneagram Type {enneagram_type} | Kosha: {kosha_layer} | "
        f"Hormone: {hormone_phase.replace('_', ' ')} | Mode: {resonance_mode}\n\n"
        f"Resonance cluster:\n{reading_context}"
    )

    if provider == "nvidia":
        discourse, model_used = await _call_nvidia(config, user_message)
    elif provider == "anthropic":
        discourse, model_used = await _call_anthropic(config, user_message)
    else:
        discourse, model_used = await _call_openai(config, user_message)

    metadata = {
        "provider": config.provider,
        "model": model_used,
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
    }
    return discourse, model_used, metadata


async def _call_nvidia(config: LLMConfig, user_message: str) -> tuple[str, str]:
    """NVIDIA NIM API (OpenAI-compatible)."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{config.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content, config.model


async def _call_openai(config: LLMConfig, user_message: str) -> tuple[str, str]:
    """OpenAI-compatible API (also works for local models, Ollama, etc.)."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{config.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": config.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                "max_tokens": config.max_tokens,
                "temperature": config.temperature,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content, config.model


async def _call_anthropic(config: LLMConfig, user_message: str) -> tuple[str, str]:
    """Anthropic Claude API."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-20",
                "Content-Type": "application/json",
            },
            json={
                "model": config.model,
                "max_tokens": config.max_tokens,
                "system": SYSTEM_PROMPT,
                "messages": [
                    {"role": "user", "content": user_message},
                ],
            },
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["content"][0]["text"]
        return content, config.model