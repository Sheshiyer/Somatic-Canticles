#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text, image_to_data_url

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated"
JSON_OUT = OUTPUT_DIR / "visual_motif_registry_seed_v1.json"
MD_OUT = OUTPUT_DIR / "visual_motif_registry_seed_v1.md"
RAW_DIR = OUTPUT_DIR / "visual_motif_raw"

ASSETS = [
    Path("/Users/sheshnarayaniyer/Documents/noesis/Research/Pasted image 20240921170304.png"),
    Path("/Users/sheshnarayaniyer/Documents/noesis/Research/Pasted image 20240921165748.png"),
    Path("/Users/sheshnarayaniyer/Documents/noesis/Research/Pasted image 20240921164241.png"),
    Path("/Users/sheshnarayaniyer/Documents/noesis/Research/Pasted image 20240714224530.png"),
    Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/assets/cards/tarot-16-tower.webp"),
    Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/assets/cards/tarot-21-universe.webp"),
]


def analyze(path: Path) -> dict[str, str]:
    data_url = image_to_data_url(path)
    system = (
        "You are extracting multimodal support cues for a fiction worldbuilding pipeline. "
        "Do not invent canon. Output only the requested single-line key-value fields."
    )
    raw_attempts: list[tuple[str, str]] = []
    payload = try_analyze_with_model(
        path=path,
        data_url=data_url,
        model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
        system=system,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        raw_attempts=raw_attempts,
    )
    if payload is None:
        payload = try_analyze_with_model(
            path=path,
            data_url=data_url,
            model="meta/llama-3.2-11b-vision-instruct",
            system=system,
            extra_body={},
            raw_attempts=raw_attempts,
        )
    if payload is None:
        write_raw_attempts(path, raw_attempts)
        raise RuntimeError(f"Unable to parse multimodal response for {path}. See raw attempts under {RAW_DIR}")
    payload["asset"] = str(path)
    return payload


def try_analyze_with_model(
    *,
    path: Path,
    data_url: str,
    model: str,
    system: str,
    extra_body: dict[str, object],
    raw_attempts: list[tuple[str, str]],
) -> dict[str, str] | None:
    response = chat_completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this image for use as review-required worldbuilding support.\n"
                            "Return exactly these six lines, one per field, with no bullets, fences, or extra commentary:\n"
                            "motif_summary: ...\n"
                            "symbolic_pressure: ...\n"
                            "biological_or_governance_hook: ...\n"
                            "likely_chapter_use: ...\n"
                            "admissibility_note: ...\n"
                            "Each value must stay on a single line, be concise, and never be empty. If uncertain, write unknown."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                ],
            },
        ],
        temperature=0.2,
        max_tokens=500,
        extra_body=extra_body,
    )
    raw = extract_text(response).strip()
    raw_attempts.append((model, raw))
    try:
        return parse_key_value_block(raw)
    except Exception:
        return None


def parse_key_value_block(raw: str) -> dict[str, str]:
    wanted = {
        "motif_summary",
        "symbolic_pressure",
        "biological_or_governance_hook",
        "likely_chapter_use",
        "admissibility_note",
    }
    parsed: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        if key in wanted:
            parsed[key] = " ".join(value.strip().split())
    missing = wanted - parsed.keys()
    if missing:
        raise RuntimeError(f"Missing keys {sorted(missing)} in visual response: {raw[:2000]}")
    return parsed


def write_raw_attempts(path: Path, raw_attempts: list[tuple[str, str]]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    stem = path.name.replace("/", "_")
    lines = [f"# Raw multimodal attempts for {path}", ""]
    for model, raw in raw_attempts:
        lines.append(f"## {model}")
        lines.append("")
        lines.append(raw or "<empty>")
        lines.append("")
    (RAW_DIR / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    items = [analyze(path) for path in ASSETS]
    JSON_OUT.write_text(json.dumps(items, indent=2), encoding="utf-8")

    lines = [
        "# Visual Motif Registry Seed v1",
        "",
        "Seed registry generated from the first curated noesis/blog visual sample set.",
        "",
    ]
    for item in items:
        lines.append(f"## {item['asset']}")
        lines.append("")
        lines.append(f"- `motif_summary`: {item['motif_summary']}")
        lines.append(f"- `symbolic_pressure`: {item['symbolic_pressure']}")
        lines.append(f"- `biological_or_governance_hook`: {item['biological_or_governance_hook']}")
        lines.append(f"- `likely_chapter_use`: {item['likely_chapter_use']}")
        lines.append(f"- `admissibility_note`: {item['admissibility_note']}")
        lines.append("")
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {JSON_OUT}")
    print(f"Wrote {MD_OUT}")


if __name__ == "__main__":
    main()
