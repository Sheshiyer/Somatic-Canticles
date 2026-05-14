#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from lib_storyops_expansion import REPO_ROOT

BLOG_ROOT = Path("/Volumes/madara/2026/twc-vault/01-Projects/tryambakam-noesis/synchronocities-blog/src/content/posts")
AREAS_ROOT = Path("/Volumes/madara/2026/twc-vault/02-Areas")
RESOURCES_ROOT = Path("/Volumes/madara/2026/twc-vault/03-Resources")
FILTER_SPEC = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "source_root_filter_spec_v1.json"
VISUAL_REGISTRY = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "expansion_lab" / "generated" / "visual_motif_registry_seed_v1.json"

STOPWORDS = {
    "a",
    "an",
    "and",
    "architecture",
    "article",
    "blog",
    "books",
    "book",
    "carryover",
    "chapter",
    "cluster",
    "critique",
    "dossier",
    "field",
    "guide",
    "if",
    "images",
    "method",
    "of",
    "or",
    "post",
    "pressure",
    "protocol",
    "scenes",
    "sources",
    "story",
    "surfaces",
    "tasks",
    "the",
    "vector",
    "visual",
}


@dataclass
class SourceCandidate:
    path: str
    source_root: str
    source_tier: str
    admissibility: str
    title: str
    summary: str
    reason: str


def tokenize(*values: str) -> list[str]:
    tokens: list[str] = []
    for value in values:
        for token in re.findall(r"[a-z0-9]+", value.lower()):
            if len(token) < 3 or token in STOPWORDS:
                continue
            tokens.append(token)
    seen: set[str] = set()
    ordered: list[str] = []
    for token in tokens:
        if token not in seen:
            ordered.append(token)
            seen.add(token)
    return ordered


def trim_text(text: str, limit: int = 420) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def slug_tokens(path: Path) -> str:
    return path.stem.lower().replace("-", " ")


def score_text(tokens: list[str], *haystacks: str) -> int:
    score = 0
    normalized = " ".join(h.lower() for h in haystacks)
    for token in tokens:
        if token in normalized:
            score += 3
        elif token.replace(" ", "-") in normalized:
            score += 2
    return score


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    lines = text[4:end].splitlines()
    data: dict[str, object] = {}
    current_list_key: str | None = None
    list_values: list[str] = []
    for line in lines:
        if re.match(r"^\s+-\s+", line) and current_list_key:
            list_values.append(re.sub(r"^\s+-\s+", "", line).strip())
            data[current_list_key] = list_values[:]
            continue
        current_list_key = None
        list_values = []
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            current_list_key = key
            data[key] = []
        else:
            data[key] = value
    return data


def extract_body_excerpt(text: str, limit: int = 420) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        lines.append(stripped)
        if len(" ".join(lines)) >= limit:
            break
    return trim_text(" ".join(lines), limit=limit)


@lru_cache(maxsize=1)
def load_filter_spec() -> dict:
    return json.loads(FILTER_SPEC.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_visual_registry() -> list[dict]:
    return json.loads(VISUAL_REGISTRY.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_blog_index() -> list[dict]:
    entries: list[dict] = []
    for path in sorted(BLOG_ROOT.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        entries.append(
            {
                "path": str(path),
                "title": str(meta.get("title") or path.stem.replace("-", " ").title()),
                "summary": trim_text(str(meta.get("excerpt") or extract_body_excerpt(text))),
                "tags": [str(tag) for tag in meta.get("tags", [])] if isinstance(meta.get("tags"), list) else [],
                "slug_text": slug_tokens(path),
            }
        )
    return entries


def summarize_note(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem.replace("-", " ")
    summary = extract_body_excerpt(text)
    return title, summary


def iter_area_files() -> list[Path]:
    spec = load_filter_spec()
    root_cfg = next(root for root in spec["roots"] if root["name"] == "area_notebooks")
    files: list[Path] = []
    for dirname in root_cfg["default_include_dirs"]:
        dirpath = AREAS_ROOT / dirname
        if not dirpath.exists():
            continue
        files.extend(path for path in dirpath.rglob("*.md") if path.is_file())
    return sorted(files)


def iter_resource_files() -> list[Path]:
    spec = load_filter_spec()
    root_cfg = next(root for root in spec["roots"] if root["name"] == "vault_resources")
    files: list[Path] = []
    for dirname in root_cfg["default_include_dirs"]:
        dirpath = RESOURCES_ROOT / dirname
        if not dirpath.exists():
            continue
        files.extend(path for path in dirpath.rglob("*.md") if path.is_file())
    return sorted(files)


def select_blog_candidates(row: dict, limit: int = 4) -> list[SourceCandidate]:
    tokens = tokenize(row["chapter_title"], row["primary_deficit"], *row["best_source_families"])
    scored: list[tuple[int, dict]] = []
    for entry in load_blog_index():
        score = score_text(tokens, entry["title"], entry["summary"], " ".join(entry["tags"]), entry["slug_text"])
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda item: (-item[0], item[1]["path"]))
    result: list[SourceCandidate] = []
    for score, entry in scored[:limit]:
        result.append(
            SourceCandidate(
                path=entry["path"],
                source_root="blog_posts",
                source_tier="published substrate",
                admissibility="text support only",
                title=entry["title"],
                summary=entry["summary"],
                reason=f"Matched chapter/source tokens with score {score}.",
            )
        )
    return result


def select_area_candidates(row: dict, limit: int = 3) -> list[SourceCandidate]:
    if "concept support" not in row["source_tier_focus"]:
        return []
    tokens = tokenize(row["chapter_title"], row["primary_deficit"], *row["best_source_families"])
    scored: list[tuple[int, Path, str, str]] = []
    for path in iter_area_files():
        title, summary = summarize_note(path)
        score = score_text(tokens, path.as_posix(), title, summary)
        if score > 0:
            scored.append((score, path, title, summary))
    scored.sort(key=lambda item: (-item[0], item[1].as_posix()))
    result: list[SourceCandidate] = []
    for score, path, title, summary in scored[:limit]:
        result.append(
            SourceCandidate(
                path=str(path),
                source_root="area_notebooks",
                source_tier="area notebook support",
                admissibility="text support only",
                title=title,
                summary=summary,
                reason=f"Matched concept-support tokens with score {score}.",
            )
        )
    return result


def select_resource_candidates(row: dict, limit: int = 2) -> list[SourceCandidate]:
    if "review-required support" not in row["source_tier_focus"]:
        return []
    tokens = tokenize(row["chapter_title"], row["primary_deficit"], *row["best_source_families"])
    scored: list[tuple[int, Path, str, str]] = []
    for path in iter_resource_files():
        title, summary = summarize_note(path)
        score = score_text(tokens, path.as_posix(), title, summary)
        if score > 0:
            scored.append((score, path, title, summary))
    scored.sort(key=lambda item: (-item[0], item[1].as_posix()))
    result: list[SourceCandidate] = []
    for score, path, title, summary in scored[:limit]:
        result.append(
            SourceCandidate(
                path=str(path),
                source_root="vault_resources",
                source_tier="vault support",
                admissibility="review-required support",
                title=title,
                summary=summary,
                reason=f"Matched review-required tokens with score {score}.",
            )
        )
    return result


def select_visual_candidates(row: dict, limit: int = 2) -> list[SourceCandidate]:
    if "visual support" not in row["source_tier_focus"] and not row["visual_support"]:
        return []
    tokens = tokenize(row["chapter_title"], row["primary_deficit"], *row["best_source_families"], *row["visual_support"])
    scored: list[tuple[int, dict]] = []
    for entry in load_visual_registry():
        score = score_text(
            tokens,
            str(entry.get("motif_summary", "")),
            str(entry.get("symbolic_pressure", "")),
            str(entry.get("biological_or_governance_hook", "")),
            str(entry.get("likely_chapter_use", "")),
            str(entry.get("asset", "")),
        )
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("asset"))))
    result: list[SourceCandidate] = []
    for score, entry in scored[:limit]:
        result.append(
            SourceCandidate(
                path=str(entry["asset"]),
                source_root="visual_support",
                source_tier="visual support",
                admissibility="visual support only",
                title=trim_text(str(entry.get("motif_summary", "visual motif")), 90),
                summary=trim_text(
                    " ".join(
                        [
                            str(entry.get("symbolic_pressure", "")),
                            str(entry.get("biological_or_governance_hook", "")),
                            str(entry.get("likely_chapter_use", "")),
                        ]
                    ),
                    420,
                ),
                reason=f"Matched visual-support tokens with score {score}.",
            )
        )
    return result


def render_candidates(candidates: list[SourceCandidate]) -> str:
    if not candidates:
        return "- none selected\n"
    lines: list[str] = []
    for item in candidates:
        lines.extend(
            [
                f"- path: `{item.path}`",
                f"  - source root: `{item.source_root}`",
                f"  - source tier: `{item.source_tier}`",
                f"  - admissibility: `{item.admissibility}`",
                f"  - title: {item.title}",
                f"  - summary: {item.summary}",
                f"  - reason selected: {item.reason}",
            ]
        )
    return "\n".join(lines) + "\n"
