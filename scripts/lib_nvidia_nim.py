#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import ssl
import sys
import time
import tomllib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def load_nvidia_settings() -> dict[str, str]:
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

    if api_key:
        return {
            "api_key": api_key,
            "base_url": base_url.rstrip("/"),
        }

    config_path = Path.home() / ".codex" / "config.toml"
    if not config_path.exists():
        raise RuntimeError("NVIDIA_API_KEY not found in environment and ~/.codex/config.toml is missing")

    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    policy = data.get("shell_environment_policy", {})
    vars_map = policy.get("set", {})
    api_key = vars_map.get("NVIDIA_API_KEY")
    base_url = vars_map.get("NVIDIA_BASE_URL", base_url)

    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY not found in environment or ~/.codex/config.toml")

    return {
        "api_key": api_key,
        "base_url": str(base_url).rstrip("/"),
    }


def chat_completion(
    *,
    model: str,
    messages: list[dict[str, Any]],
    temperature: float = 0.3,
    max_tokens: int = 1600,
    extra_body: dict[str, Any] | None = None,
    timeout_seconds: int = 600,
    max_attempts: int = 3,
    retry_backoff_seconds: int = 8,
) -> dict[str, Any]:
    settings = load_nvidia_settings()
    context = build_ssl_context()
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if extra_body:
        payload.update(extra_body)

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{settings['base_url']}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {settings['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    retryable_codes = {408, 429, 500, 502, 503, 504}
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout_seconds, context=context) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                if response.status == 202:
                    return poll_request_result(
                        settings=settings,
                        context=context,
                        response_body=parsed,
                        location=response.headers.get("Location"),
                    )
                if parsed.get("requestId") and not parsed.get("choices"):
                    return poll_request_result(
                        settings=settings,
                        context=context,
                        response_body=parsed,
                        location=response.headers.get("Location"),
                    )
                return parsed
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in retryable_codes and attempt < max_attempts:
                time.sleep(retry_backoff_seconds * attempt)
                last_error = RuntimeError(f"NVIDIA API HTTP {exc.code}: {detail}")
                continue
            raise RuntimeError(f"NVIDIA API HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            if attempt < max_attempts:
                time.sleep(retry_backoff_seconds * attempt)
                last_error = RuntimeError(f"NVIDIA API connection error: {exc}")
                continue
            raise RuntimeError(f"NVIDIA API connection error: {exc}") from exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("NVIDIA API call failed without a captured exception")


def extract_text(response: dict[str, Any]) -> str:
    try:
        content = response["choices"][0]["message"]["content"]
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            if parts:
                return "\n".join(parts)
        raise TypeError(f"Unsupported content type: {type(content)!r}")
    except Exception as exc:
        raise RuntimeError(f"Unexpected response shape: {json.dumps(response)[:1000]}") from exc


def image_to_data_url(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    if suffix == "jpg":
        suffix = "jpeg"
    raw = path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:image/{suffix};base64,{encoded}"


def build_ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore
    except Exception:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


def poll_request_result(
    *,
    settings: dict[str, str],
    context: ssl.SSLContext,
    response_body: dict[str, Any],
    location: str | None,
    timeout_seconds: int = 600,
    poll_interval_seconds: int = 2,
) -> dict[str, Any]:
    request_id = response_body.get("requestId")
    if not location:
        if not request_id:
            raise RuntimeError(f"NVIDIA API returned a pending response without requestId: {json.dumps(response_body)[:1000]}")
        location = f"{settings['base_url']}/status/{request_id}"

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        req = urllib.request.Request(
            location,
            headers={"Authorization": f"Bearer {settings['api_key']}"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=120, context=context) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                if response.status == 202:
                    time.sleep(poll_interval_seconds)
                    continue
                return parsed
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 202:
                time.sleep(poll_interval_seconds)
                continue
            raise RuntimeError(f"NVIDIA API polling HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"NVIDIA API polling connection error: {exc}") from exc

    raise RuntimeError(f"NVIDIA API polling timed out for requestId={request_id or 'unknown'}")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)
