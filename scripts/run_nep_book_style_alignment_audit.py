#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import (
    BOOK_LABELS,
    REPO_ROOT,
    load_chapter_metadata,
    slugify_chapter_title,
    word_count,
)

GENERATED_DIR = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
)
RAW_ROOT = GENERATED_DIR / "chapter_expansion_raw"
MATRIX_JSON = GENERATED_DIR / "chapter_expansion_matrix_v1.json"
TARGET_PROFILE_JSON = GENERATED_DIR / "trilogy_length_target_profile_v1.json"
BOOK_RULES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "book_rules.md"
DIALOGUE_MATRIX = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "dialogue_voice_matrix.md"
EDITORIAL_BRIEF = REPO_ROOT / "03_EDITORIAL" / "EDITORIAL_BRIEF.md"

CONTROL_MODEL_DEFAULT = "openai/gpt-oss-120b"

FORBIDDEN_RESIDUE = [
    "Somatic Event",
    "Character Focus",
    "Political Context",
    "Territory Context",
    "Cultural Context",
    "Chapter Status",
    "RESONANCE PROFILE",
    "PubMed",
    "doi",
    "Alex Grey",
    "visual archive",
    "CLIP-Vision",
    "WORLD_BIBLE.md",
    "Quantum Systems",
    "manifestation",
    "Rider-Waite",
    "Rider Waite",
]

BIOLOGY_TERMS = {
    "blood",
    "brain",
    "cell",
    "genome",
    "hormone",
    "cortisol",
    "synapse",
    "neuron",
    "receptor",
    "endocrine",
    "body",
    "breath",
    "immune",
    "marrow",
}
PHILOSOPHY_TERMS = {
    "meaning",
    "truth",
    "choice",
    "will",
    "self",
    "memory",
    "consent",
    "soul",
    "attention",
    "field",
    "belief",
    "world",
    "reality",
    "pattern",
}
TECH_TERMS = {
    "protocol",
    "interface",
    "system",
    "signal",
    "data",
    "code",
    "machine",
    "sensor",
    "calibration",
    "algorithm",
    "network",
    "device",
    "monitor",
    "diagnostic",
}
WIT_MARKERS = {
    "almost",
    "absurd",
    "ridiculous",
    "joke",
    "smiled",
    "smile",
    "laugh",
    "of course",
    "apparently",
    "technically",
    "congratulations",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit expanded Book chapters for cross-chapter style alignment.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--model", default=CONTROL_MODEL_DEFAULT)
    parser.add_argument("--max-excerpt-chars", type=int, default=1500)
    parser.add_argument("--skip-model", action="store_true")
    return parser.parse_args()


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_excerpt(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def load_json_rows(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "chapters" in data:
        return list(data["chapters"])
    if isinstance(data, list):
        return data
    raise RuntimeError(f"Unsupported JSON row shape in {path}")


def load_row(rows: list[dict[str, Any]], chapter_number: int) -> dict[str, Any]:
    for row in rows:
        if int(row["chapter_number"]) == chapter_number:
            return row
    raise RuntimeError(f"Missing row for Chapter {chapter_number:02d}")


def chapter_slug(chapter_number: int, title: str) -> str:
    return f"{chapter_number:02d}-{slugify_chapter_title(title)}"


def gate_sort_key(path: Path) -> int:
    match = re.search(r"\.gate-(\d+)\.md$", path.name)
    return int(match.group(1)) if match else -1


def latest_gate(raw_dir: Path, slug: str) -> tuple[Path | None, dict[str, Any] | None, int | None]:
    gates = sorted(raw_dir.glob(f"{slug}.gate-*.md"), key=gate_sort_key)
    if not gates:
        return None, None, None
    path = gates[-1]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {"parse_error": path.read_text(encoding="utf-8")[:1000]}
    return path, payload, gate_sort_key(path)


def count_terms(text: str, terms: set[str]) -> int:
    lowered = text.lower()
    total = 0
    for term in terms:
        total += len(re.findall(rf"\b{re.escape(term)}\b", lowered))
    return total


def sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text.strip()))
    return [word_count(sentence) for sentence in sentences if word_count(sentence) > 0]


def sentence_temperature_metric(text: str) -> dict[str, Any]:
    lengths = sentence_lengths(text)
    if not lengths:
        return {"average_sentence_words": 0, "short_sentence_share": 0, "long_sentence_share": 0}
    short = sum(1 for length in lengths if length <= 8)
    long = sum(1 for length in lengths if length >= 32)
    return {
        "average_sentence_words": round(sum(lengths) / len(lengths), 2),
        "short_sentence_share": round(short / len(lengths), 3),
        "long_sentence_share": round(long / len(lengths), 3),
    }


def representative_excerpts(text: str, max_chars: int) -> dict[str, str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    if not paragraphs:
        return {"opening": "", "middle": "", "closing": ""}
    middle_index = max(0, len(paragraphs) // 2 - 2)
    chunks = {
        "opening": "\n\n".join(paragraphs[:5]),
        "middle": "\n\n".join(paragraphs[middle_index : middle_index + 5]),
        "closing": "\n\n".join(paragraphs[-5:]),
    }
    return {
        key: value[: max_chars - 3].rstrip() + "..." if len(value) > max_chars else value
        for key, value in chunks.items()
    }


def residue_hits(text: str) -> list[str]:
    hits = []
    for token in FORBIDDEN_RESIDUE:
        pattern = rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(token)
    return hits


def local_risk_score(
    *,
    current_words: int,
    macro_target_low: int,
    gate_stage: int | None,
    gate_payload: dict[str, Any] | None,
    raw_match: bool,
    residue: list[str],
) -> int:
    score = 0
    if macro_target_low and current_words < int(macro_target_low * 0.72):
        score += 3
    elif macro_target_low and current_words < int(macro_target_low * 0.85):
        score += 2
    if gate_stage is None:
        score += 3
    elif gate_stage < 4:
        score += 2
    scores = (gate_payload or {}).get("scores") or {}
    if scores:
        minimum = min(value for value in scores.values() if isinstance(value, (int, float)))
        if minimum < 7:
            score += 2
        elif minimum == 7:
            score += 1
    if not raw_match:
        score += 3
    if residue:
        score += 3
    return min(score, 10)


def build_chapter_packet(
    *,
    book: int,
    matrix_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    max_excerpt_chars: int,
) -> list[dict[str, Any]]:
    raw_dir = RAW_ROOT / f"book_{book}"
    packets: list[dict[str, Any]] = []
    for meta in load_chapter_metadata():
        if meta.book_number != book:
            continue
        working_path = REPO_ROOT / meta.working_file
        working_text = working_path.read_text(encoding="utf-8")
        slug = chapter_slug(meta.chapter_number, meta.chapter_title)
        raw_path = raw_dir / f"{slug}.raw.md"
        raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
        gate_path, gate_payload, gate_stage = latest_gate(raw_dir, slug)
        matrix_row = load_row(matrix_rows, meta.chapter_number)
        target_row = load_row(target_rows, meta.chapter_number)
        current_words = word_count(working_text)
        hits = residue_hits(working_text)
        raw_match = bool(raw_path.exists() and raw_text == working_text)
        local_metrics = {
            "word_count": current_words,
            "macro_target_low": target_row.get("macro_target_low"),
            "macro_target_high": target_row.get("macro_target_high"),
            "macro_low_completion": round(current_words / target_row["macro_target_low"], 3),
            "intermediate_3x_floor": target_row.get("intermediate_3x_floor"),
            "gate_stage": gate_stage,
            "gate_path": repo_rel(gate_path) if gate_path else None,
            "gate_pass": (gate_payload or {}).get("pass"),
            "gate_scores": (gate_payload or {}).get("scores"),
            "raw_path": repo_rel(raw_path) if raw_path.exists() else None,
            "raw_match": raw_match,
            "residue_hits": hits,
            "dialogue_quote_count": working_text.count('"'),
            "biology_term_count": count_terms(working_text, BIOLOGY_TERMS),
            "philosophy_term_count": count_terms(working_text, PHILOSOPHY_TERMS),
            "technology_term_count": count_terms(working_text, TECH_TERMS),
            "wit_marker_count": count_terms(working_text, WIT_MARKERS),
            "sentence_temperature": sentence_temperature_metric(working_text),
        }
        local_metrics["local_risk_score"] = local_risk_score(
            current_words=current_words,
            macro_target_low=int(target_row["macro_target_low"]),
            gate_stage=gate_stage,
            gate_payload=gate_payload,
            raw_match=raw_match,
            residue=hits,
        )
        packets.append(
            {
                "chapter_number": meta.chapter_number,
                "chapter_title": meta.chapter_title,
                "summary": meta.summary,
                "working_file": meta.working_file,
                "matrix_focus": {
                    "primary_deficit": matrix_row.get("primary_deficit"),
                    "layer_gaps": matrix_row.get("layer_gaps"),
                    "best_source_families": matrix_row.get("best_source_families"),
                    "notes": matrix_row.get("notes"),
                },
                "local_metrics": local_metrics,
                "gate_notes": (gate_payload or {}).get("notes", []),
                "excerpts": representative_excerpts(working_text, max_excerpt_chars),
            }
        )
    return packets


def build_input_pack(*, book: int, packets: list[dict[str, Any]], max_excerpt_chars: int) -> str:
    contract = f"""
# Book {book} Style Alignment Audit Input Pack

Book: {BOOK_LABELS[book]}

## Audit Contract

- Identify whether Book {book} is stylistically stable as a continuous lane, not merely whether each chapter passed its own local gate.
- Find the two most likely chapters that still need style or length alignment before a Book {book} commit.
- Use the existing trilogy contract: biology / philosophy / technology braid, character-specific wit lanes, sentence-temperature variation, double-meaning density, pressure-release humor, implicit Toth/Crowley symbolic scaffold, no production residue.
- Do not ask for a full rewrite unless the evidence requires it. Prefer constrained repair actions.
- Treat shorter chapters, missing gate depth, raw/working mismatch, one-register solemnity, biology-heavy imbalance, and weak character-specific wit as risks.
"""
    context = f"""
## Editorial Brief Excerpt

```md
{read_excerpt(EDITORIAL_BRIEF, 2400)}
```

## Book Rules Excerpt

```md
{read_excerpt(BOOK_RULES, 2400)}
```

## Dialogue Voice Matrix Excerpt

```md
{read_excerpt(DIALOGUE_MATRIX, 2400)}
```
"""
    chapter_sections = []
    for packet in packets:
        chapter_sections.append(
            f"""
## Chapter {packet['chapter_number']:02d}: {packet['chapter_title']}

Summary: {packet['summary']}

Working file: `{packet['working_file']}`

Matrix focus:

```json
{json.dumps(packet['matrix_focus'], ensure_ascii=False, indent=2)}
```

Local metrics:

```json
{json.dumps(packet['local_metrics'], ensure_ascii=False, indent=2)}
```

Latest gate notes:

```json
{json.dumps(packet['gate_notes'], ensure_ascii=False, indent=2)}
```

Opening excerpt:

```md
{packet['excerpts']['opening']}
```

Middle excerpt:

```md
{packet['excerpts']['middle']}
```

Closing excerpt:

```md
{packet['excerpts']['closing']}
```
"""
        )
    return "\n".join([contract, context, "\n".join(chapter_sections)]).strip() + "\n"


def extract_json_object(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Could not locate JSON object in model output: {text[:1000]}")
    return json.loads(match.group(0))


def build_audit_prompt(input_pack: str, book: int) -> str:
    return f"""
You are auditing an expanded novel book lane for style alignment.

Return JSON only with this schema:
{{
  "book": {book},
  "overall_verdict": "pass|flag|block",
  "summary": "...",
  "repair_order": [4, 6],
  "chapters": [
    {{
      "chapter_number": 1,
      "verdict": "pass|watch|repair",
      "risk_score": 0,
      "primary_failure_modes": ["..."],
      "evidence": ["..."],
      "recommended_action": "...",
      "must_repair_before_book_commit": false
    }}
  ],
  "book_level_notes": ["..."],
  "next_action": "..."
}}

Rules:
- Be strict. A local gate pass is not enough if the chapter is still a book-level outlier.
- If exactly two chapters look weaker, name them in `repair_order` first.
- If only one chapter truly needs work, put only that chapter first and use `watch` for the next nearest risk.
- Prioritize evidence from local metrics plus the excerpts.
- Penalize one-register solemnity, generic wit, weak pressure release, biology-heavy flattening, missing final gate depth, residue, and large macro target gaps.
- Do not recommend opening Book 2 or Book 3 work here. This audit is only Book {book}.

Input pack:

```md
{input_pack}
```
"""


def local_fallback_audit(book: int, packets: list[dict[str, Any]], error: str | None = None) -> dict[str, Any]:
    ranked = sorted(
        packets,
        key=lambda packet: (
            packet["local_metrics"]["local_risk_score"],
            0 if packet["local_metrics"].get("gate_stage") == 4 else 1,
            -packet["local_metrics"]["word_count"],
        ),
        reverse=True,
    )
    chapters = []
    for packet in packets:
        metrics = packet["local_metrics"]
        risk = int(metrics["local_risk_score"])
        verdict = "repair" if risk >= 4 else "watch" if risk >= 2 else "pass"
        failures = []
        if metrics.get("gate_stage") is None:
            failures.append("missing saved style gate")
        elif metrics.get("gate_stage") < 4:
            failures.append("latest saved gate does not reach gate-4")
        if metrics["macro_low_completion"] < 0.72:
            failures.append("short against macro target low band")
        if metrics.get("residue_hits"):
            failures.append("production or forbidden residue present")
        if not metrics.get("raw_match"):
            failures.append("working/raw artifact mismatch")
        if not failures:
            failures.append("no deterministic blocker found")
        chapters.append(
            {
                "chapter_number": packet["chapter_number"],
                "verdict": verdict,
                "risk_score": risk,
                "primary_failure_modes": failures,
                "evidence": [
                    f"word_count={metrics['word_count']}",
                    f"macro_low_completion={metrics['macro_low_completion']}",
                    f"gate_stage={metrics.get('gate_stage')}",
                    f"gate_scores={metrics.get('gate_scores')}",
                    f"raw_match={metrics.get('raw_match')}",
                ],
                "recommended_action": "Run constrained style/length repair if this remains in the top repair order.",
                "must_repair_before_book_commit": verdict == "repair",
            }
        )
    repair_order = [packet["chapter_number"] for packet in ranked if packet["local_metrics"]["local_risk_score"] >= 2][:2]
    return {
        "book": book,
        "overall_verdict": "flag" if repair_order else "pass",
        "summary": "Local deterministic fallback audit completed." + (f" Model error: {error}" if error else ""),
        "repair_order": repair_order,
        "chapters": chapters,
        "book_level_notes": [
            "Fallback is metric-led and should be superseded by the model audit when available.",
            "A Chapter 04 risk is expected if its latest saved style gate stops before gate-4.",
        ],
        "next_action": "Inspect the top repair candidate and run a constrained chapter repair only if prose samples confirm drift.",
    }


def render_markdown(audit: dict[str, Any], packets: list[dict[str, Any]]) -> str:
    packet_by_chapter = {packet["chapter_number"]: packet for packet in packets}
    lines = [
        f"# Book {audit.get('book')} Style Alignment Audit",
        "",
        f"Overall verdict: `{audit.get('overall_verdict')}`",
        "",
        str(audit.get("summary", "")).strip(),
        "",
        f"Repair order: `{audit.get('repair_order', [])}`",
        "",
        "## Chapter Verdicts",
        "",
    ]
    for chapter in sorted(audit.get("chapters", []), key=lambda row: int(row.get("chapter_number", 0))):
        chapter_number = int(chapter.get("chapter_number", 0))
        packet = packet_by_chapter.get(chapter_number, {})
        metrics = packet.get("local_metrics", {})
        lines.extend(
            [
                f"### Chapter {chapter_number:02d}: {packet.get('chapter_title', 'Unknown')}",
                "",
                f"- Verdict: `{chapter.get('verdict')}`",
                f"- Risk score: `{chapter.get('risk_score')}`",
                f"- Working words: `{metrics.get('word_count')}`",
                f"- Macro low completion: `{metrics.get('macro_low_completion')}`",
                f"- Latest gate: `gate-{metrics.get('gate_stage')}`",
                f"- Gate scores: `{metrics.get('gate_scores')}`",
                f"- Raw match: `{metrics.get('raw_match')}`",
                f"- Residue hits: `{metrics.get('residue_hits')}`",
                f"- Failure modes: `{chapter.get('primary_failure_modes', [])}`",
                f"- Recommended action: {chapter.get('recommended_action', '')}",
                "",
            ]
        )
        evidence = chapter.get("evidence") or []
        if evidence:
            lines.append("Evidence:")
            for item in evidence:
                lines.append(f"- {item}")
            lines.append("")
    notes = audit.get("book_level_notes") or []
    if notes:
        lines.append("## Book-Level Notes")
        lines.append("")
        for note in notes:
            lines.append(f"- {note}")
        lines.append("")
    lines.extend(["## Next Action", "", str(audit.get("next_action", "")).strip(), ""])
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    matrix_rows = load_json_rows(MATRIX_JSON)
    target_rows = load_json_rows(TARGET_PROFILE_JSON)
    packets = build_chapter_packet(
        book=args.book,
        matrix_rows=matrix_rows,
        target_rows=target_rows,
        max_excerpt_chars=args.max_excerpt_chars,
    )
    input_pack = build_input_pack(book=args.book, packets=packets, max_excerpt_chars=args.max_excerpt_chars)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    input_path = GENERATED_DIR / f"book_{args.book}_style_alignment_input_pack_v1.md"
    raw_model_path = GENERATED_DIR / f"book_{args.book}_style_alignment_audit_v1.raw.md"
    json_path = GENERATED_DIR / f"book_{args.book}_style_alignment_audit_v1.json"
    md_path = GENERATED_DIR / f"book_{args.book}_style_alignment_audit_v1.md"
    metrics_path = GENERATED_DIR / f"book_{args.book}_style_alignment_local_metrics_v1.json"
    input_path.write_text(input_pack, encoding="utf-8")
    metrics_path.write_text(json.dumps(packets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit: dict[str, Any]
    if args.skip_model:
        audit = local_fallback_audit(args.book, packets)
        raw_model_path.write_text("Model call skipped; local fallback audit used.\n", encoding="utf-8")
    else:
        prompt = build_audit_prompt(input_pack, args.book)
        print(f"[book {args.book}] nvidia_call=style_alignment_audit model={args.model} timeout=900s", flush=True)
        try:
            response = chat_completion(
                model=args.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict novel continuity and prose-style auditor. Return valid JSON only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=5000,
                timeout_seconds=900,
                max_attempts=3,
                retry_backoff_seconds=12,
            )
            raw_text = extract_text(response)
            raw_model_path.write_text(raw_text.strip() + "\n", encoding="utf-8")
            audit = extract_json_object(raw_text)
        except Exception as exc:
            raw_model_path.write_text(f"MODEL ERROR:\n{exc}\n", encoding="utf-8")
            audit = local_fallback_audit(args.book, packets, error=str(exc))

    json_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(audit, packets), encoding="utf-8")

    print(f"[book {args.book}] wrote {repo_rel(input_path)}", flush=True)
    print(f"[book {args.book}] wrote {repo_rel(metrics_path)}", flush=True)
    print(f"[book {args.book}] wrote {repo_rel(raw_model_path)}", flush=True)
    print(f"[book {args.book}] wrote {repo_rel(json_path)}", flush=True)
    print(f"[book {args.book}] wrote {repo_rel(md_path)}", flush=True)
    print(f"[book {args.book}] verdict={audit.get('overall_verdict')} repair_order={audit.get('repair_order')}", flush=True)


if __name__ == "__main__":
    main()
