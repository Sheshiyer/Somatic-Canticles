#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT, word_count
from run_nep_chapter_expansion import (
    RAW_ROOT,
    load_matrix_row,
    matrix_control_model,
    resolve_control_model,
    run_style_gate,
    validate_style_gate,
    working_meta,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the chapter style gate over the current working chapter.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument("--stage", type=int, default=None)
    parser.add_argument("--control-model", default=None)
    return parser.parse_args()


def chapter_slug(chapter_number: int, chapter_title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", chapter_title.lower()).strip("-")
    return f"{chapter_number:02d}-{slug}"


def gate_sort_key(path: Path) -> int:
    match = re.search(r"\.gate-(\d+)\.md$", path.name)
    return int(match.group(1)) if match else -1


def next_gate_stage(raw_dir: Path, slug: str) -> int:
    gates = sorted(raw_dir.glob(f"{slug}.gate-*.md"), key=gate_sort_key)
    if not gates:
        return 1
    return max(gate_sort_key(path) for path in gates) + 1


def main() -> None:
    args = parse_args()
    meta = working_meta(args.chapter)
    if meta.book_number != args.book:
        raise RuntimeError(f"Chapter {args.chapter:02d} does not belong to Book {args.book}")
    matrix_row = load_matrix_row(args.chapter)
    raw_dir = RAW_ROOT / f"book_{args.book}"
    slug = chapter_slug(args.chapter, meta.chapter_title)
    stage = args.stage if args.stage is not None else next_gate_stage(raw_dir, slug)
    working_path = REPO_ROOT / meta.working_file
    raw_path = raw_dir / f"{slug}.raw.md"
    working_text = working_path.read_text(encoding="utf-8")
    raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
    if raw_text != working_text:
        raise RuntimeError(f"Raw artifact does not match working chapter: {raw_path}")
    control_model, route_notes = resolve_control_model(matrix_row=matrix_row, override=args.control_model)
    print(f"matrix_control_model={matrix_control_model(matrix_row)}")
    print(f"effective_control_model={control_model}")
    for note in route_notes:
        print(f"route_note={note}")
    gate = run_style_gate(
        model=control_model,
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        candidate_text=working_text,
        raw_dir=raw_dir,
        slug=slug,
        stage_index=stage,
    )
    validate_style_gate(gate)
    print(f"chapter={args.chapter:02d}")
    print(f"words={word_count(working_text)}")
    print(f"gate_stage={stage}")
    print(f"scores={gate.get('scores', {})}")


if __name__ == "__main__":
    main()
