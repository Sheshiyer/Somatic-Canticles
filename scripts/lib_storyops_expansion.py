#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHAPTER_SUMMARIES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "chapter_summaries.md"
COMPILED_DIR = REPO_ROOT / "02_MANUSCRIPTS" / "COMPILED"
CHAPTERS_DIR = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "chapters"

BOOK_LABELS = {
    1: "Book 1: The Anamnesis Engine",
    2: "Book 2: The Myocardial Chorus",
    3: "Book 3: The Ripening",
}

BOOK_SLUGS = {
    1: "book_1_anamnesis_engine",
    2: "book_2_myocardial_chorus",
    3: "book_3_the_ripening",
}

COMPILED_BOOK_FILES = {
    1: "02_MANUSCRIPTS/COMPILED/Book_1_Anamnesis_Engine.md",
    2: "02_MANUSCRIPTS/COMPILED/Book_2_The_Myocardial_Chorus.md",
    3: "02_MANUSCRIPTS/COMPILED/Book_3_The_Ripening.md",
}


@dataclass
class ChapterMeta:
    chapter_number: int
    chapter_title: str
    book_number: int
    book_label: str
    summary: str
    working_file: str
    compiled_file: str
    current_words: int


def repo_rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def chapter_book_number(chapter_number: int) -> int:
    if 1 <= chapter_number <= 8:
        return 1
    if 9 <= chapter_number <= 15:
        return 2
    return 3


def load_chapter_summaries() -> dict[int, tuple[str, str]]:
    text = CHAPTER_SUMMARIES.read_text(encoding="utf-8")
    pattern = re.compile(r"- `(?P<num>\d{2})\. (?P<title>[^`]+)` — (?P<summary>.+)")
    result: dict[int, tuple[str, str]] = {}
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        num = int(match.group("num"))
        result[num] = (match.group("title").strip(), match.group("summary").strip())
    return result


def scan_working_files() -> dict[int, tuple[str, int]]:
    result: dict[int, tuple[str, int]] = {}
    pattern = re.compile(r"Chapter-(\d{2})-")
    for path in sorted(CHAPTERS_DIR.glob("book_*/working/Chapter-*.md")):
        match = pattern.search(path.name)
        if not match:
            continue
        chapter_number = int(match.group(1))
        text = path.read_text(encoding="utf-8")
        result[chapter_number] = (repo_rel(path), word_count(text))
    return result


def load_chapter_metadata() -> list[ChapterMeta]:
    summaries = load_chapter_summaries()
    working = scan_working_files()
    items: list[ChapterMeta] = []
    for chapter_number in range(1, 28):
        title, summary = summaries[chapter_number]
        working_file, current_words = working[chapter_number]
        book_number = chapter_book_number(chapter_number)
        items.append(
            ChapterMeta(
                chapter_number=chapter_number,
                chapter_title=title,
                book_number=book_number,
                book_label=BOOK_LABELS[book_number],
                summary=summary,
                working_file=working_file,
                compiled_file=COMPILED_BOOK_FILES[book_number],
                current_words=current_words,
            )
        )
    return items


def slugify_chapter_title(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


def extract_json_list(raw: str) -> list[dict]:
    start = raw.find("[")
    end = raw.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise RuntimeError(f"Could not locate JSON list in model output: {raw[:2000]}")
    return json.loads(raw[start : end + 1])
