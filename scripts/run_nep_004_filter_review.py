#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text

REPO_ROOT = Path(__file__).resolve().parents[1]
INTAKE_PATH = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "source_root_intake_v1.md"
SPEC_PATH = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "source_root_filter_spec_v1.md"
OUTPUT_PATH = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "source_family_priority_map_v1.md"


def main() -> None:
    intake = INTAKE_PATH.read_text(encoding="utf-8")
    spec = SPEC_PATH.read_text(encoding="utf-8")
    system = (
        "You are reviewing a source-root filtering plan for a fiction expansion system. "
        "You improve prioritization and execution order, not canon."
    )
    user = f"""
Review the following source-root intake and filter spec and produce `Source Family Priority Map v1`.

Required sections:
1. Root-by-root execution priority
2. Fastest wins for dossier production
3. Highest-risk noise families to exclude aggressively
4. First-pass families for Book 1
5. First-pass families for Book 2
6. First-pass families for Book 3
7. Recommended helper-script targets for the tooling lane

Rules:
- Do not widen admissibility beyond the current contract.
- Prefer practical prioritization over theory.
- Output markdown only.

Source intake:

{intake}

Filter spec:

{spec}
"""
    response = chat_completion(
        model="minimaxai/minimax-m2.7",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        max_tokens=1800,
    )
    OUTPUT_PATH.write_text(extract_text(response).strip() + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
