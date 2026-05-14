#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text

REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "repo_synthesis_input_pack_v1.md"
OUTPUT_PATH = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "repo_synthesis_report_v1.md"


def main() -> None:
    source = INPUT_PATH.read_text(encoding="utf-8")
    system = (
        "You are synthesizing a long-form fiction repo. "
        "Work only from the supplied repo control surfaces and source-tier rules. "
        "Do not invent canon. Output markdown only."
    )
    user = f"""
Using the following repo synthesis input pack, produce `Repo Synthesis Report v1`.

Required sections:
1. Canon Baseline
2. Control Surfaces That Must Govern Expansion
3. Source Tier Understanding
4. Book-by-Book Deepening Opportunities
5. Chapter Cluster Priorities
6. Highest-Risk Dryness or Compression Patterns
7. Dossier Production Order
8. Explicit Guardrails For Later Drafting

Rules:
- Cite repo-relative file paths where possible.
- Treat the blog as the strongest external text substrate.
- Treat `03-Resources` and `02-Areas` as filtered support, not governing authority.
- Treat `Documents/noesis/Research` as multimodal support, not canon.
- Be concrete, not poetic.

Input pack:

{source}
"""
    response = chat_completion(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
        max_tokens=2200,
        extra_body={"reasoning_effort": "low"},
    )
    OUTPUT_PATH.write_text(extract_text(response).strip() + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
