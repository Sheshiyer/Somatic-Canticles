#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from lib_nvidia_nim import chat_completion, extract_text
from lib_storyops_expansion import REPO_ROOT, load_chapter_metadata, word_count

DOSSIER_MANIFEST = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "dossier_manifest_v1.json"
)
MATRIX_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_expansion_matrix_v1.json"
)
TARGET_PROFILE_JSON = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "trilogy_length_target_profile_v1.json"
)
BOOK_RULES = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "book_rules.md"
DIALOGUE_MATRIX = REPO_ROOT / "06_WORKBENCH" / "SC_STORYOPS" / "story" / "dialogue_voice_matrix.md"
EDITORIAL_BRIEF = REPO_ROOT / "03_EDITORIAL" / "EDITORIAL_BRIEF.md"
RAW_ROOT = (
    REPO_ROOT
    / "06_WORKBENCH"
    / "SC_STORYOPS"
    / "story"
    / "expansion_lab"
    / "generated"
    / "chapter_expansion_raw"
)
CONTROL_MODEL_DEFAULT = "openai/gpt-oss-120b"
SAFE_DRAFT_MODEL_DEFAULT = "qwen/qwen3.5-122b-a10b"
PROBED_UNSAFE_DEFAULT_DRAFT_MODELS = {
    "moonshotai/kimi-k2.6",
    "moonshotai/kimi-k2-instruct",
    "moonshotai/kimi-k2-thinking",
    "minimaxai/minimax-m2.7",
    "z-ai/glm-5.1",
    "deepseek-ai/deepseek-v4-pro",
    "writer/palmyra-creative-122b",
    "mistralai/mistral-large-3-675b-instruct-2512",
}
PROBED_UNSAFE_DEFAULT_CONTROL_MODELS = {
    "nvidia/nemotron-3-super-120b-a12b",
}
STAGE_TIMEOUT_SECONDS = 900
REPAIR_TIMEOUT_SECONDS = 420
INSERT_TIMEOUT_SECONDS = 480
STYLE_TIMEOUT_SECONDS = 420
VOICE_REPAIR_TIMEOUT_SECONDS = 700
LATE_STAGE_FULL_REPAIR_WORD_LIMIT = 5000
INSERT_FALLBACK_ATTEMPTS = 8
VOICE_REPAIR_ATTEMPTS = 2
DUPLICATE_INSERT_FALLBACK_AFTER = 2
INSERT_FIRST_STAGE_START = 1
MAX_INSERT_REQUEST_WORDS = 1100
POST_HARD_FAILURE_MAX_INSERT_WORDS = 500
LONG_INSERT_CONTEXT_WORDS = 5000
STYLE_FAILURE_MARKERS = (
    "below 6",
    "solemn",
    "clinical",
    "wit_lane",
    "humor_pressure_release",
    "double_meaning",
    "braid",
)
LEXICAL_STYLE_GUIDANCE = (
    "Use field, lattice, deep-field, pulse, thrum, tremor, pressure, cadence, and resonance language; "
    "avoid legacy subatomic-mechanics jargon and generic oscillation wording."
)
LEXICAL_REPLACEMENTS = (
    ("Quantum Systems", "field systems"),
    ("Chetana Yantra", "awareness instrument"),
    ("quantum foam", "deep-field substrate"),
    ("quantum core", "chamber core"),
    ("quantum lattice", "field lattice"),
    ("quantum states", "field states"),
    ("quantum state", "field state"),
    ("quantum cache", "lattice cache"),
    ("quantum filaments", "lattice filaments"),
    ("quantum filament", "lattice filament"),
    ("quantum substrate", "field substrate"),
    ("quantum flux", "field flux"),
    ("quantum conduits", "field conduits"),
    ("quantum conduit", "field conduit"),
    ("quantum", "field"),
    ("Quantum", "Field"),
    ("vibrations", "tremors"),
    ("Vibrations", "Tremors"),
    ("vibration", "tremor"),
    ("Vibration", "Tremor"),
    ("vibrating", "shivering"),
    ("Vibrating", "Shivering"),
    ("vibrated", "trembled"),
    ("Vibrated", "Trembled"),
    ("vibrate", "tremble"),
    ("Vibrate", "Tremble"),
    ("manifestation", "appearance"),
    ("Manifestation", "Appearance"),
    ("manifesting", "appearing"),
    ("Manifesting", "Appearing"),
    ("manifested", "appeared"),
    ("Manifested", "Appeared"),
    ("frequencies", "cadences"),
    ("Frequencies", "Cadences"),
    ("frequency", "cadence"),
    ("Frequency", "Cadence"),
    ("shattering", "splintering"),
    ("Shattering", "Splintering"),
    ("shattered", "splintered"),
    ("Shattered", "Splintered"),
    ("shatter", "splinter"),
    ("Shatter", "Splinter"),
    ("filaments", "threads"),
    ("Filaments", "Threads"),
    ("filament", "thread"),
    ("Filament", "Thread"),
    ("corridors", "passages"),
    ("Corridors", "Passages"),
    ("corridor", "passage"),
    ("Corridor", "Passage"),
    ("energies", "forces"),
    ("Energies", "Forces"),
    ("energy", "charge"),
    ("Energy", "Charge"),
)
PREAMBLE_LABELS = [
    "Somatic Event",
    "Character Focus",
    "Family Context",
    "Political Context",
    "Territory Context",
    "Cultural Context",
    "Chapter Status",
    "Resonance Profile",
]
FORBIDDEN_TOKENS = [
    "**Somatic Event:**",
    "**Character Focus:**",
    "**Family Context:**",
    "**Political Context:**",
    "**Territory Context:**",
    "**Cultural Context:**",
    "PubMed",
    "NIH",
    "Alex Grey",
    "visual archive",
    "CLIP-Vision",
    "Quantum",
    "quantum",
    "vibration",
    "vibrations",
    "vibrate",
    "vibrated",
    "vibrating",
    "frequency",
    "frequencies",
    "shatter",
    "shattered",
    "shattering",
    "manifestation",
    "manifested",
    "manifesting",
    "Chetana Yantra",
    "WORLD_BIBLE.md",
    "Preface.md",
    "failed candidate",
    "failed candidate’s",
    "failed candidate's",
    "Crystal Conductor",
    "living tapestry",
    "newborn star",
    "Kael",
    "Jory",
    "Mara",
    "Lira",
    "Juna",
    "Toth",
    "Tothian",
    "Crowley",
    "Crowleyan",
    "Enneagram",
    "Hanged Man",
    "Tarot",
    "tarot",
    "corridor",
    "bulkhead",
    "reactor",
    "pipes",
    "plumbing",
    "marshmallow",
    "cockpit",
    "parachute",
    "lower deck",
    "lower-deck",
]
CHAPTER_FORBIDDEN_TOKENS = {
    16: [
        "Atrium",
        "atrium",
        "filament",
        "filaments",
        "injector",
        "injectors",
        "nanofiber",
        "side-arm",
        "suit",
        "suits",
        "gauntlet",
        "gauntlets",
        "fragment",
        "fragments",
        "spectrometer",
        "spectrometers",
        "respirator",
        "propulsion fields",
        "holo-grid",
        "data core",
        "optic lenses",
        "field-generator",
        "modulators",
        "actuators",
        "emitter",
        "emitters",
        "conduit",
        "conduits",
        "secondary feed",
        "secondary lattice",
        "semi-corporeal",
        "broadcast",
        "controlled wilt",
        "data packet",
        "external relay",
        "portable data",
        "protocol offered",
        "weaponized protocol",
        "House of Continuity",
        "House of Resonance",
        "Hall of Governance",
        "Veridian",
        "Cormac",
        "House of Lumen",
        "descent shaft",
        "hidden corridors",
        "The descent began",
        "field was willing to listen",
        "field was willing to cooperate",
        "Mira's outline",
        "Mira’s outline",
        "Mira stood",
        "Mira closed",
        "Mira kept",
        "Mira asked",
        "Mira gave",
        "Mira felt",
    ],
    17: [
        "Crystallization Interface protocols",
        "Quantum Systems",
        "Chetana Yantra",
        "energy",
        "energies",
        "homeostasis",
        "mechanism was the universe",
        "law of nature",
        "maintenance algorithm",
        "villain",
        "evil",
        "sneer",
        "sneered",
        "gloat",
        "gloated",
        "hatred",
        "defeat the Gardener",
        "destroy the Gardener",
        "kill the Gardener",
        "Mira said",
        "Mira asked",
        "Mira answered",
        "Mira stood",
        "Mira moved",
    ],
    18: [
        "The Gardener said",
        "The Gardener asked",
        "The Gardener answered",
        "The Gardener replied",
        "The Gardener spoke",
        "Gardener said",
        "Gardener asked",
        "Gardener answered",
        "Gardener replied",
        "Gardener spoke",
        "law of nature",
        "homeostasis",
        "maintenance algorithm",
        "mechanism was the universe",
        "system sermon",
        "The Synthesis Protocol was complete",
        "protocol was complete",
        "merged field",
        "single voice",
        "became one",
        "fused into",
        "operator",
        "operators",
        "Mira said",
        "Mira asked",
        "Mira answered",
        "Mira stood",
        "Mira moved",
    ],
    11: [
        "Mira",
        "Jax",
        "Arlen",
        "Selene",
        "Asha",
        "Kian",
        "J-X",
        "J‑X",
    ],
}
CHAPTER_CAST_HINTS = {
    16: (
        "For Chapter 16, keep named people limited to Corv, Sona, Jian, Gideon, and Mira Verath. "
        "Mira Verath may appear only as a subject, memory, data trace, or resonance reference; do not make her speak, operate equipment, "
        "stand in the chamber, or act as a semi-corporeal helper. The Gardener and Entropy Plague may be named as concepts or distant pressure, "
        "but not as on-page speaking roles yet."
    ),
    17: (
        "For Chapter 17, keep named people limited to Corv, Sona, Jian, Gideon, Mira Verath, and The Gardener. "
        "Mira Verath may appear only as subject, interior terrain, memory, or case trace; do not make her speak or operate as a helper. "
        "The Gardener may appear and communicate, but its voice must remain conservational, calm, sorrowfully necessary, and non-villainous."
    ),
    18: (
        "For Chapter 18, keep named people limited to Corv, Sona, Jian, Gideon, and Mira Verath. "
        "Mira Verath may appear only as the case subject, data trace, lineage lattice, or recovery consequence; do not make her speak or act as a helper. "
        "The Gardener may be referenced only as the prior encounter, residue, pressure, or correction logic; do not give it new dialogue or an on-page presence."
    ),
    11: (
        "For Chapter 11, keep named people limited to Corv, Sona, Jian, and Gideon. "
        "Council monitors, operators, avatars, or assistants may appear only as unnamed roles."
    ),
    12: (
        "For Chapter 12, keep the on-page cast limited to Corv, Sona, Jian, and Gideon. "
        "Do not add operators, assistants, monitors, observers, patients, council voices, helper names, or extra spoken roles; "
        "show external/system pressure through instruments, status text, silence, and the existing team's dialogue."
    ),
    13: (
        "For Chapter 13, keep the on-page cast limited to Corv, Sona, Jian, and Gideon. "
        "The chorus may appear as field behavior or unnamed collective pressure, not as new named speakers."
    ),
    14: (
        "For Chapter 14, keep the on-page cast limited to Corv, Sona, Jian, and Gideon. "
        "House names such as Seter are lineage/field terms here, not permission to add new named people."
    ),
    15: (
        "For Chapter 15, keep the on-page cast limited to Corv, Sona, Jian, and Gideon. "
        "Witness systems, councils, or distributed observers must remain environmental pressure unless already named in the accepted draft."
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Expand a working chapter from its dossier and macro target band.")
    parser.add_argument("--book", type=int, required=True, choices=[1, 2, 3])
    parser.add_argument("--chapter", type=int, required=True)
    parser.add_argument(
        "--minimum-words",
        type=int,
        default=None,
        help="Override the default pass floor for constrained macro-length repairs.",
    )
    parser.add_argument(
        "--draft-model",
        default=None,
        help="Override the matrix draft model when the preferred creative route is unavailable.",
    )
    parser.add_argument(
        "--control-model",
        default=None,
        help="Override the matrix control_pass/control_model route for gates and acceptance repair.",
    )
    parser.add_argument(
        "--print-route",
        action="store_true",
        help="Print the resolved model route and exit without generating prose.",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def read_excerpt(path: Path, max_chars: int = 4000) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def load_manifest_row(chapter_number: int) -> dict:
    rows = json.loads(DOSSIER_MANIFEST.read_text(encoding="utf-8"))
    for row in rows:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing dossier manifest row for chapter {chapter_number:02d}")


def load_matrix_row(chapter_number: int) -> dict:
    rows = json.loads(MATRIX_JSON.read_text(encoding="utf-8"))
    for row in rows:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing matrix row for chapter {chapter_number:02d}")


def load_target_row(chapter_number: int) -> dict:
    payload = json.loads(TARGET_PROFILE_JSON.read_text(encoding="utf-8"))
    for row in payload["chapters"]:
        if row["chapter_number"] == chapter_number:
            return row
    raise RuntimeError(f"Missing target profile row for chapter {chapter_number:02d}")


def matrix_control_model(matrix_row: dict) -> str:
    return matrix_row.get("control_model") or matrix_row.get("control_pass") or CONTROL_MODEL_DEFAULT


def resolve_draft_model(*, book_number: int, matrix_row: dict, override: str | None) -> tuple[str, list[str]]:
    matrix_model = matrix_row.get("draft_model")
    notes: list[str] = []
    if override:
        return override, ["draft override supplied"]
    if matrix_model in PROBED_UNSAFE_DEFAULT_DRAFT_MODELS:
        notes.append(f"draft rerouted from probed unsafe/default-slow model {matrix_model}")
        return SAFE_DRAFT_MODEL_DEFAULT, notes
    if not matrix_model:
        notes.append("draft missing from matrix; using safe default draft route")
        return SAFE_DRAFT_MODEL_DEFAULT, notes
    if book_number == 2 and matrix_model != SAFE_DRAFT_MODEL_DEFAULT:
        notes.append(f"Book 2 draft route preserved from matrix: {matrix_model}")
    return matrix_model, notes


def resolve_control_model(*, matrix_row: dict, override: str | None) -> tuple[str, list[str]]:
    matrix_model = matrix_control_model(matrix_row)
    notes: list[str] = []
    if override:
        return override, ["control override supplied"]
    if matrix_model in PROBED_UNSAFE_DEFAULT_CONTROL_MODELS:
        notes.append(f"control rerouted from unverified matrix route {matrix_model}")
        return CONTROL_MODEL_DEFAULT, notes
    return matrix_model, notes


def working_meta(chapter_number: int):
    for item in load_chapter_metadata():
        if item.chapter_number == chapter_number:
            return item
    raise RuntimeError(f"Missing chapter metadata for chapter {chapter_number:02d}")


def chapter_slug(chapter_number: int, chapter_title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", chapter_title.lower()).strip("-")
    return f"{chapter_number:02d}-{slug}"


def chapter_cast_hint(chapter_number: int) -> str:
    return CHAPTER_CAST_HINTS.get(
        chapter_number,
        "Do not invent additional named people; keep any new person unnamed unless the current chapter authority already names them.",
    )


def chapter_insert_guidance(chapter_number: int) -> str:
    if chapter_number == 16:
        return (
            "Chapter 16 insertion lane: stay inside the Anamnesis Engine chamber and the Verath lineage visualization. "
            "Do not turn the chapter into an action repair, hardware procedure, atrium mission, lattice-splice, injector, conduit, suit, gauntlet, fragment, or spectrometer sequence. "
            "Do not solve or stabilize the Wilt; any counter-move must fail, clarify the threat, or buy only diagnostic humility. "
            "Do not invent House names, export a data packet, transmit a relay, or begin the descent on-page. "
            "Deepen discovery, dread, House-political consequence, team disagreement, chamber ecology, Mira as a distant subject/data trace, and the unresolved decision to descend toward Chapter 17."
        )
    if chapter_number == 17:
        return (
            "Chapter 17 insertion lane: remain inside Mira Verath's interior terrain and the post-encounter chamber aftermath. "
            "Do not villain-code The Gardener; do not make it sneer, rage, gloat, or seek cruelty. "
            "Do not over-mechanize it into universe/law/homeostasis/system-theory monologue; dramatize sorrowful necessity through encounter pressure, pruning action, and calm offer language. "
            "Deepen the four refusals: Corv refuses false mercy of meaning, Sona refuses anesthetic peace, Jian refuses the cage of explanation, and Gideon allows protection to be reclassified rather than broken. "
            "Keep the close embodied and procedural: ejected from depth, field-lock breath exchange, and a concrete handoff into Chapter 18's synthesis work."
        )
    if chapter_number == 18:
        return (
            "Chapter 18 insertion lane: stay in the immediate post-Gardener Anamnesis Engine chamber and turn the encounter into enacted procedure. "
            "Do not repeat the Gardener sermon, add new Gardener dialogue, or explain the encounter as universe/law/homeostasis/system theory. "
            "Do not present the Synthesis Protocol as complete, perfect, mastered, salvific, or as merger/fusion/unity of the team. "
            "Deepen field-surgery pressure: hands on interfaces, telemetry lag, House classification risk, Verath-lattice evidence, failed timing attempts, and exact threshold discipline. "
            "Keep the three vectors exact and role-bound: Sona holds Pure Joy as calibrated aliveness, Corv holds Catalyst Clarity as the undecorated Bell moment, Gideon holds Present Coherence as passage discipline, and Jian tracks the moving constellation without pretending the map is sovereign. "
            "Build toward Chapter 19 by making the Three-Point Problem harder and more concrete, not by solving it."
        )
    return "No extra chapter-specific insert guidance."


def cleaned_heading(chapter_number: int, chapter_title: str) -> str:
    return f"# Chapter {chapter_number}: {chapter_title}\n"


def strip_preamble_residue(lines: list[str]) -> list[str]:
    labels = "|".join(re.escape(label) for label in PREAMBLE_LABELS)
    label_line = re.compile(
        rf"^\s*(?:[-*]\s*)?(?:\*\*)?\s*(?:{labels})\s*(?:\*\*)?\s*:",
        flags=re.IGNORECASE,
    )
    heading_line = re.compile(
        rf"^\s*#+\s*(?:{labels})\s*$",
        flags=re.IGNORECASE,
    )
    return [line for line in lines if not label_line.match(line) and not heading_line.match(line)]


def find_preamble_residue(text: str) -> str | None:
    labels = "|".join(re.escape(label) for label in PREAMBLE_LABELS)
    label_line = re.compile(
        rf"^\s*(?:[-*]\s*)?(?:\*\*)?\s*(?:{labels})\s*(?:\*\*)?\s*:",
        flags=re.IGNORECASE,
    )
    heading_line = re.compile(
        rf"^\s*#+\s*(?:{labels})\s*$",
        flags=re.IGNORECASE,
    )
    for line in text.splitlines():
        if label_line.match(line) or heading_line.match(line):
            return line.strip()
    return None


def normalize_lexical_carryovers(text: str) -> str:
    cleaned = text
    for old, replacement in LEXICAL_REPLACEMENTS:
        cleaned = cleaned.replace(old, replacement)
    return cleaned


def forbidden_tokens_for(chapter_number: int | None = None) -> list[str]:
    tokens = list(FORBIDDEN_TOKENS)
    if chapter_number is not None:
        tokens.extend(CHAPTER_FORBIDDEN_TOKENS.get(chapter_number, []))
    return tokens


def find_forbidden_token(text: str, *, chapter_number: int | None = None) -> str | None:
    for token in forbidden_tokens_for(chapter_number):
        if token in text:
            return token
    return None


def has_hard_validation_failure(text: str, *, chapter_number: int | None = None) -> bool:
    return bool(find_preamble_residue(text) or find_forbidden_token(text, chapter_number=chapter_number))


def sanitize_failure_note(reason: str, *, chapter_number: int | None = None) -> str:
    cleaned = reason
    for token in sorted(forbidden_tokens_for(chapter_number), key=len, reverse=True):
        cleaned = re.sub(re.escape(token), "[hard-banned term]", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r"unsupported new teammate\s+[\"“][^\"”]+[\"”]",
        "unsupported new teammate",
        cleaned,
        flags=re.IGNORECASE,
    )
    return cleaned


def normalize_insert_text(text: str) -> str:
    cleaned = normalize_lexical_carryovers(text).replace("\ufeff", "").strip()
    lines = []
    for line in cleaned.splitlines():
        if re.match(r"^\s*#*\s*Chapter\s+\d+\b", line, flags=re.IGNORECASE):
            continue
        lines.append(line)
    lines = strip_preamble_residue(lines)
    return "\n".join(lines).strip() + "\n"


def paragraph_key(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def overlap_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def word_shingles(text: str, *, size: int = 10) -> set[str]:
    words = overlap_key(text).split()
    if len(words) < size:
        return set()
    return {" ".join(words[index : index + size]) for index in range(len(words) - size + 1)}


def has_high_shingle_overlap(candidate: str, base_shingles: set[str], *, size: int = 10) -> bool:
    shingles = word_shingles(candidate, size=size)
    if len(shingles) < 4:
        return False
    return len(shingles & base_shingles) / len(shingles) >= 0.72


def dedupe_repeated_paragraphs(text: str) -> str:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]
    kept: list[str] = []
    kept_keys: set[str] = set()
    kept_overlap_stream = ""
    kept_shingles: set[str] = set()
    for paragraph in paragraphs:
        key = paragraph_key(paragraph)
        overlap = overlap_key(paragraph)
        if not key:
            continue
        if paragraph.startswith("# Chapter"):
            kept.append(paragraph)
            kept_keys.add(key)
            continue
        duplicate = key in kept_keys
        if not duplicate and len(overlap) >= 220 and overlap in kept_overlap_stream:
            duplicate = True
        if not duplicate and has_high_shingle_overlap(paragraph, kept_shingles):
            duplicate = True
        if duplicate:
            continue
        kept.append(paragraph)
        kept_keys.add(key)
        kept_overlap_stream = f"{kept_overlap_stream} {overlap}".strip()
        kept_shingles.update(word_shingles(paragraph))
    return "\n\n".join(kept).strip() + ("\n" if kept else "")


def dedupe_insert_against_base(*, base_text: str, insert_text: str) -> str:
    base_paragraphs = [paragraph_key(part) for part in re.split(r"\n\s*\n", base_text) if paragraph_key(part)]
    base_key_set = set(base_paragraphs)
    base_long_keys = [key for key in base_paragraphs if len(key) >= 180]
    base_overlap_stream = overlap_key(base_text)
    base_shingles = word_shingles(base_text)
    seen_insert_keys: set[str] = set()
    kept: list[str] = []
    for paragraph in re.split(r"\n\s*\n", normalize_insert_text(insert_text)):
        key = paragraph_key(paragraph)
        overlap = overlap_key(paragraph)
        if not key or key in seen_insert_keys or key in base_key_set:
            continue
        seen_insert_keys.add(key)
        if len(overlap) >= 180 and overlap in base_overlap_stream:
            continue
        if has_high_shingle_overlap(paragraph, base_shingles):
            continue
        if len(key) >= 180 and any(
            abs(len(key) - len(base_text_key)) < 140 and SequenceMatcher(None, key, base_text_key).ratio() >= 0.9
            for base_text_key in base_long_keys
        ):
            continue
        kept.append(paragraph.strip())
    return "\n\n".join(kept).strip() + ("\n" if kept else "")


def merge_insert_before_last_paragraph(base_text: str, insert_text: str) -> str:
    base = base_text.strip()
    insert = normalize_insert_text(insert_text).strip()
    paragraphs = re.split(r"\n\s*\n", base)
    if len(paragraphs) < 3:
        return base + "\n\n" + insert + "\n"
    merged = paragraphs[:-1] + [insert, paragraphs[-1]]
    return "\n\n".join(part.strip() for part in merged if part.strip()) + "\n"


def normalize_chapter_text(text: str, *, chapter_number: int, chapter_title: str) -> str:
    expected = f"# Chapter {chapter_number}: {chapter_title}"
    cleaned = normalize_lexical_carryovers(text).replace("\ufeff", "").strip()
    lines = cleaned.splitlines()
    chapter_line = re.compile(r"^\s*#*\s*Chapter\s+\d+\b", flags=re.IGNORECASE)
    for idx, line in enumerate(lines[:12]):
        if chapter_line.match(line):
            lines = lines[idx:]
            lines[0] = expected
            lines = strip_preamble_residue(lines)
            return "\n".join(lines).strip() + "\n"
    cleaned_lines = strip_preamble_residue(lines)
    return expected + "\n\n" + "\n".join(cleaned_lines).strip() + "\n"


def extract_dossier_section(dossier_text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## \d+\. |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(dossier_text)
    if not match:
        return ""
    return match.group("body").strip()


def build_dossier_context(dossier_text: str) -> str:
    sections = [
        ("2. Canon Function", extract_dossier_section(dossier_text, "2. Canon Function")),
        ("3. Character-Arc Obligations", extract_dossier_section(dossier_text, "3. Character-Arc Obligations")),
        ("8a. Implicit Symbolic Scaffold", extract_dossier_section(dossier_text, "8a. Implicit Symbolic Scaffold")),
        ("9. Scene Growth Opportunities", extract_dossier_section(dossier_text, "9. Scene Growth Opportunities")),
        ("10. Vocabulary and Voice Constraints", extract_dossier_section(dossier_text, "10. Vocabulary and Voice Constraints")),
    ]
    rendered: list[str] = []
    for heading, body in sections:
        if body:
            rendered.append(f"## {heading}\n{body}")
    return "\n\n".join(rendered)


def build_stage_targets(*, current_words: int, minimum_words: int) -> list[int]:
    targets = [
        max(current_words + 1200, min(minimum_words, max(3200, int(minimum_words * 0.35)))),
        max(current_words + 2400, min(minimum_words, max(5000, int(minimum_words * 0.60)))),
        max(current_words + 4200, min(minimum_words, max(7000, int(minimum_words * 0.82)))),
        minimum_words,
    ]
    result: list[int] = []
    previous = current_words
    for target in targets:
        if target <= previous:
            continue
        if result and target <= result[-1]:
            continue
        result.append(target)
        previous = target
    return result


def build_stage_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    current_draft: str,
    dossier_context: str,
    matrix_row: dict,
    target_row: dict,
    stage_index: int,
    stage_count: int,
    stage_low: int,
    stage_high: int,
) -> str:
    matrix_focus = {
        "primary_deficit": matrix_row["primary_deficit"],
        "layer_gaps": matrix_row["layer_gaps"],
        "best_source_families": matrix_row["best_source_families"],
        "notes": matrix_row["notes"],
    }
    preserve_existing = (
        "Preserve at least 85% of the existing sentences verbatim and grow by insertion around them."
        if stage_index > 1
        else "Preserve the existing beats and tonal spine while enlarging the chapter additively."
    )
    return f"""
Expand this novel chapter additively. This is stage {stage_index} of {stage_count}.

Rules:
- Output markdown only.
- First line must be exactly: `# Chapter {chapter_number}: {chapter_title}`
- Do not include section labels like `Somatic Event`, `Character Focus`, `Political Context`, or any dossier metadata.
- Do not include notes, explanations, or bullet lists.
- Preserve canon, scene order, and the outbound obligation from the dossier.
- Do not invent additional Somanaut teammates or named operators. Any new named person must already be present in the current draft, dossier, chapter summary, or required source context.
- {chapter_cast_hint(chapter_number)}
- Treat the current draft as a base text that must survive. Do not compress, omit, summarize, or skip existing beats.
- Every existing paragraph and scene skeleton from the current draft must visibly survive in order unless a microscopic line edit is unavoidable for continuity.
- The correct operation is insertion, not replacement. If your output is shorter than the input draft, it is invalid.
- {preserve_existing}
- Keep the same POV center and chapter identity, but deepen atmosphere, somatic rhythm, relational consequence, and world pressure.
- Add new material before, between, and after existing beats so the chapter breathes.
- Use dossier deepening sources only through scene, image, sensation, dialogue, behavior, and consequence. Do not lecture.
- Keep dialogue role-bound per the voice matrix.
- Preserve and correctly use project lexicon such as `Khalorēē field`, `Manas Interface`, `Adawat al-Wa'i`, `Klei Toda'ah`, and `The Vine` when relevant.
- If the chapter draws on the project's submerged symbolic-muse logic, use it only as scene architecture, pressure, reversal, and image selection.
- The full submerged scaffold may also include cyclical recurrence and archetypal patterning. Use the whole chain as an emotional and stylistic regulator, not as overt exposition.
- Keep that symbolic lattice subliminal through pacing, tonal reversal, and biological emphasis. Do not have characters explain it aloud.
- Maintain a three-lane braid at all times:
  - somatic / biological precision
  - philosophical or field-intelligence pressure
  - technological / protocol atmosphere
- Do not let biology dominate the chapter. Each strong biological image or diagnostic beat should be counterweighted by either a technological consequence, a field/philosophical implication, or a sharp relational turn within the next few sentences.
- Keep the delivery punchy. Use short declarative lines at pressure points so the prose does not become a continuous clinical wash.
- Bring layered meanings and verbal play where natural. Let phrases do double duty without turning ornamental.
- Allow intelligent pressure-release humor or dry wit when character-true. Do not make everyone speak in the same solemn register.
- Use a supplemental structured-tone reference, not a replacement voice: grounded, direct, respectful-challenging; clinical precision at visionary scale; conviction over hedging.
- {LEXICAL_STYLE_GUIDANCE}
- Let humor be structural when it appears: funny because true at multiple scales, not because the chapter starts performing jokes.
- Modulate the emotional temperature. Let fear, wonder, irony, intimacy, technical focus, and grief alter the sentence texture rather than flattening into one style.
- Assign wit lanes by character where they appear:
  - Jian: dry, precision-cut wit
  - Gideon: blunt, defensive wit
  - Corv: oblique, double-meaning wit
  - Sona: gentle, relational wit
- Vary sentence temperature across the scene. Alternate clipped protocol lines, sensuous dread, lucid philosophical turns, and occasional pressure-release lines so the prose does not move in one emotional cadence.
- Ensure at least two of those wit lanes actually land on the page in dialogue or tightly focalized thought during this stage. Do not leave wit as subtext only.
- Add at least one distinct pressure-release beat before the chapter's deepest descent, and make it character-true rather than jokey.
- Add at least one phrase or exchange that can be read on two levels at once: technical and emotional, clinical and devotional, or procedural and relational.
- Banned carryover terms or patterns: `Quantum Systems`, `vibration`, `manifestation`, lore-dump monologues, pseudo-spiritual filler, production scaffolding.
- Remove the old preamble metadata entirely and integrate its information into the prose itself.
- This is a smoke pass for the first live expansion wave, so the draft should materially deepen the chapter, not just line-edit it.
- The goal of this stage is to land the chapter in the `{stage_low:,}-{stage_high:,}` word range while keeping every existing scene beat intact.

Matrix focus:

```json
{json.dumps(matrix_focus, ensure_ascii=False, indent=2)}
```

Macro target profile row:

```json
{json.dumps(target_row, ensure_ascii=False, indent=2)}
```

Compact dossier context:

```md
{dossier_context}
```

Current chapter draft to expand without compression:

```md
{current_draft}
```

Now write the full revised chapter at this stage length.
"""


def build_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    accepted_draft: str,
    failed_candidate: str,
    stage_low: int,
    stage_high: int,
    accepted_words: int,
    required_min_words: int,
    repair_attempt: int,
    focus_notes: str,
) -> str:
    required_new_words = max(required_min_words - accepted_words, 300)
    return f"""
Repair this expanded chapter so it grows materially without losing any existing beats. This is repair attempt {repair_attempt}.

Requirements:
- Keep the same title line: `# Chapter {chapter_number}: {chapter_title}`
- The output must be at least `{required_min_words:,}` words.
- The accepted base draft is `{accepted_words:,}` words, so add at least `{required_new_words:,}` words of scene-native material.
- Preserve all existing canon beats and invented prose that is already working.
- Do not invent additional Somanaut teammates or named operators. Any new named person must already be present in the accepted draft, failed candidate, or dossier context.
- {chapter_cast_hint(chapter_number)}
- Do not compress or summarize the draft you are given.
- Every existing paragraph and scene skeleton must still be present in order after repair unless a microscopic line edit is unavoidable for continuity.
- The correct operation is insertion, not replacement. If the repaired output is shorter than the input draft, it is invalid.
- Preserve the draft's tonal spine. Extend it by insertion and local deepening, not by revoicing the chapter into a colder or more clinical register.
- Use the accepted base draft as the mandatory spine.
- The failed candidate may contain useful tonal moves, wit, or imagery, but it compressed the chapter. Harvest from it selectively without inheriting its shrinkage.
- Do not add metadata, notes, or bullet lists.
- Do not include preamble labels or production markers such as `Somatic Event`, `Character Focus`, `Political Context`, `RESONANCE PROFILE`, or `Chapter Status`.
- Increase scene dwell time, sensory embodiment, relational consequence, and aftermath.
- Add only scene-native material; do not add essays or lore-dump paragraphs.
- Keep any symbolic-muse scaffolding implicit through scene pressure and tonal reversal rather than overtly explained.
- Preserve the chapter's layered meaning, wit, and emotional temperature shifts. If humor or irony is already present or naturally available, sharpen it rather than sanding it away.
- Keep the tone grounded, direct, and structurally intelligent. Borrow conviction and multi-scale humor if helpful, but do not drift into content-marketing voice.
- {LEXICAL_STYLE_GUIDANCE}
- Reinforce character-specific wit lanes instead of adding generic humor:
  - Jian: dry technical understatement
  - Gideon: blunt protective edge
  - Corv: oblique doubleness
  - Sona: soft connective wit
- Make at least two of those wit lanes concretely audible on the page through dialogue or tightly focalized interior phrasing.
- Keep the biology / philosophy / technology braid intact. Do not over-index on raw anatomy or biomarker description.
- Add punch: short decisive lines, cleaner turns, and stronger protocol aura where the prose gets soggy.
- Ensure at least one pressure-release beat and at least one true double-meaning phrase survive in the repaired chapter.
- Bring the chapter into the `{stage_low:,}-{stage_high:,}` word range if possible.

Repair specifically for these failures:

{focus_notes}

Accepted base draft that must survive:

```md
{accepted_draft}
```

Failed candidate that may contain salvageable phrases or tonal gains:

```md
{failed_candidate}
```

Return the full revised chapter only.
"""


def build_insert_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    accepted_draft: str,
    failed_candidate: str,
    required_new_words: int,
    focus_notes: str,
    insert_attempt: int,
) -> str:
    base_paragraphs = [part.strip() for part in re.split(r"\n\s*\n", accepted_draft.strip()) if part.strip()]
    base_tail = "\n\n".join(base_paragraphs[-5:])
    accepted_draft_words = word_count(accepted_draft)
    attempt_directives = {
        1: (
            "Attempt lane 1: write a clean bridge beat that expands consequence before the final paragraph. "
            "Do not reopen an already-rendered corridor, palace, threshold, staircase, or door image."
        ),
        2: (
            "Attempt lane 2: the prior insert likely repeated existing scene architecture. Change vectors completely: "
            "write relational and field-technology consequence with character-specific dialogue. Avoid new palace, corridor, door, "
            "staircase, crayon, card, window, marrow-column, or CSF-floor description."
        ),
        3: (
            "Attempt lane 3: write a compact dialogue-forward recovery insert with minimal visionary architecture. "
            "Make the growth come from protocol stakes, wit lanes, consent pressure, and aftermath, not from another sensory set-piece."
        ),
        4: (
            "Attempt lane 4: write only a present-tense team coordination beat. No new palace, corridor, arch, card, mercury, star, "
            "door, staircase, seam, ledger, or receipt imagery. Use body-risk telemetry, field protocol, and role-bound dialogue."
        ),
        5: (
            "Attempt lane 5: write a sparse pressure-release and protocol-recalibration insert. No visionary architecture nouns. "
            "Use clipped lines, character-specific wit, and concrete mission consequence."
        ),
    }
    attempt_directive = attempt_directives.get(insert_attempt, attempt_directives[5])
    if insert_attempt >= 3 or accepted_draft_words > LONG_INSERT_CONTEXT_WORDS:
        accepted_reference = (
            "The full accepted base draft is intentionally omitted for this long-base or late duplicate-recovery attempt because earlier retries copied it or made calls too slow. "
            "Use only the forbidden ending/context excerpt above for continuity, and write fresh material that can be inserted before that ending."
        )
        failed_reference = (
            "The failed candidate is intentionally omitted for this long-base or late duplicate-recovery attempt because it may reinforce compression, repetition, or context bloat."
        )
    else:
        accepted_reference = f"""```md
{accepted_draft}
```"""
        failed_reference = f"""```md
{failed_candidate}
```"""
    return f"""
Write only new scene-native insertion material for Chapter {chapter_number}: {chapter_title}.

This is not a full chapter rewrite. Return only the new paragraphs to insert before the chapter's final paragraph.

Requirements:
- Output markdown prose paragraphs only.
- Do not include a title, heading, notes, bullets, metadata, or labels.
- Do not include preamble labels such as `Somatic Event`, `Character Focus`, `Political Context`, `RESONANCE PROFILE`, or `Chapter Status`.
- Do not repeat, quote, paraphrase, or restate paragraphs that already exist in the accepted base draft.
- Write only new material that can be inserted once. The insert is invalid if it loops corridor descriptions, repeats existing sensory beats, or recaps the accepted draft.
- Do not repeat the accepted base ending shown below. Lead into it by consequence, silence, decision, or pressure-release, not by replaying its images.
- Write `{required_new_words:,}` to `{required_new_words + 350:,}` words of new material.
- The insert must preserve canon and feel like it belongs inside the accepted base draft.
- Do not invent additional Somanaut teammates or named operators. Any new named person must already be present in the accepted base draft or failed candidate.
- {chapter_cast_hint(chapter_number)}
- {chapter_insert_guidance(chapter_number)}
- Use the failed candidate only as a source of salvageable tone, imagery, wit, or pressure-release moves.
- Add scene dwell time, relational consequence, atmosphere, and one pressure-release beat.
- Keep the biology / philosophy / technology braid intact.
- Keep the submerged symbolic-muse logic implicit through pacing, pressure, reversal, and image selection.
- {LEXICAL_STYLE_GUIDANCE}
- Use character-specific wit sparingly and concretely where natural.
- If this insert is repairing style gate failures, prioritize calm counter-rhythm, distinct character voice, one clean technical consequence, and one character-true pressure-release exchange over more visionary sensory escalation.
- The insert must transition cleanly into the base draft's final paragraph.

{attempt_directive}

Repair specifically for these failures:

{focus_notes}

Accepted base ending that must not be repeated:

```md
{base_tail}
```

Accepted base draft:

{accepted_reference}

Failed candidate:

{failed_reference}

Return only the insertion prose.
"""


def extract_json_object(text: str) -> dict:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Style gate did not return JSON.")
    return json.loads(match.group(0))


def build_style_gate_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    candidate_text: str,
) -> str:
    return f"""
Evaluate this expanded novel chapter candidate strictly for tone balance and stylistic vitality.

Return JSON only with this schema:
{{
  "pass": true,
  "scores": {{
    "braid_balance": 0,
    "wit_lane_distinction": 0,
    "temperature_variation": 0,
    "double_meaning_density": 0,
    "humor_pressure_release": 0
  }},
  "failures": ["..."],
  "notes": ["..."]
}}

Scoring guide:
- 9-10: excellent
- 7-8: clearly working
- 5-6: partial / fragile
- 0-4: under target

Pass rules:
- fail if any score is below 6
- fail if the prose still reads mostly in one solemn or one clinical register
- fail if the biology / philosophy / technology braid is unbalanced
- fail if character-specific wit lanes are generic, absent, or indistinguishable
- fail if there is no meaningful pressure-release beat
- fail if character identity or pronouns drift inside the chapter
- fail if an unsupported new Somanaut teammate or named operator appears

Target chapter:
- Chapter {chapter_number}: {chapter_title}

Cast authority:
- {chapter_cast_hint(chapter_number)}

Candidate text:

```md
{candidate_text}
```
"""


def build_voice_repair_prompt(
    *,
    chapter_number: int,
    chapter_title: str,
    candidate_text: str,
    minimum_words: int,
    gate_notes: str,
    dialogue_matrix: str,
) -> str:
    candidate_words = word_count(candidate_text)
    return f"""
Perform a final acceptance repair on this already-expanded chapter.

This is not another growth insert. The candidate already reached `{candidate_words:,}` words against a floor of `{minimum_words:,}` words, but failed the style gate. Return the full repaired chapter only.

Hard requirements:
- First line must remain exactly: `# Chapter {chapter_number}: {chapter_title}`
- Output markdown prose only. Do not include notes, headings, labels, bullets, metadata, or explanations.
- Keep the repaired chapter at least `{minimum_words:,}` words.
- Preserve canon, scene order, and the existing chapter spine. Do not delete whole beats to tighten style.
- Do not introduce new architecture, new lore dumps, new named systems, or a new plot turn.
- Do not invent additional Somanaut teammates or named operators. Any named person in the repaired chapter must already exist in the candidate or the dialogue matrix excerpt.
- {chapter_cast_hint(chapter_number)}
- Do not add preamble labels such as `Somatic Event`, `Character Focus`, `Political Context`, `RESONANCE PROFILE`, or `Chapter Status`.
- Treat character identity as canon. Corv uses he/him pronouns. Sona uses she/her. Jian and Gideon use he/him. Remove any pronoun drift.
- Fix style locally and surgically: revise flat passages, add connective tissue, sharpen exchanges, and rebalance paragraphs without replacing the chapter's substance.

Repair targets:
- Break the one-note lyrical / clinical wash by alternating short protocol beats, embodied dread, technical consequence, and relational pressure.
- Rebalance the biology / philosophy / technology braid inside the same scene logic rather than letting one strand dominate a long block.
- Make character-specific wit lanes audible and distinct:
  - Corv: oblique double-meaning, patient but not coy
  - Sona: sensory and connective, never generic mystic
  - Jian: dry precision, falsifiability, abrupt respect
  - Gideon: blunt protective edge, boundary and load language
- Add or sharpen one pressure-release beat that matters because it lowers tension without breaking stakes.
- Increase double-meaning density through phrases that read both technically and emotionally. Do not decorate for its own sake.
- Keep the submerged symbolic-muse lattice implicit through pacing, pressure, reversal, and image selection. Never name the scaffold.
- {LEXICAL_STYLE_GUIDANCE}

Style gate failures to repair:

{gate_notes}

Dialogue voice matrix excerpt:

```md
{dialogue_matrix}
```

Candidate chapter:

```md
{candidate_text}
```

Return the full repaired chapter only.
"""


def validate_chapter(text: str, *, chapter_number: int, chapter_title: str, current_words: int, minimum_words: int) -> None:
    first_line = text.splitlines()[0].strip() if text.splitlines() else ""
    expected = f"# Chapter {chapter_number}: {chapter_title}"
    if first_line != expected:
        raise RuntimeError(f"Expanded chapter missing exact heading: {expected}")
    residue = find_preamble_residue(text)
    if residue:
        raise RuntimeError(f"Expanded chapter contains preamble residue: {residue}")
    forbidden = find_forbidden_token(text, chapter_number=chapter_number)
    if forbidden:
        raise RuntimeError(f"Expanded chapter contains forbidden token: {forbidden}")
    expanded_words = word_count(text)
    if expanded_words <= current_words:
        raise RuntimeError(f"Expanded chapter did not grow: current={current_words}, expanded={expanded_words}")
    if expanded_words < minimum_words:
        raise RuntimeError(f"Expanded chapter below minimum pass floor: {expanded_words} < {minimum_words}")


def validate_stage(
    text: str,
    *,
    chapter_number: int,
    chapter_title: str,
    previous_words: int,
    stage_floor: int,
    stage_index: int,
) -> None:
    relaxed_floor = stage_required_floor(
        previous_words=previous_words,
        stage_floor=stage_floor,
        stage_index=stage_index,
    )
    validate_chapter(
        text,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        current_words=previous_words,
        minimum_words=relaxed_floor,
    )


def validate_candidate_progress(
    text: str,
    *,
    chapter_number: int,
    chapter_title: str,
    current_words: int,
    previous_words: int,
    stage_floor: int,
    stage_index: int,
    final_stage: bool,
    minimum_words: int,
) -> None:
    if final_stage:
        validate_chapter(
            text,
            chapter_number=chapter_number,
            chapter_title=chapter_title,
            current_words=current_words,
            minimum_words=minimum_words,
        )
        return
    validate_stage(
        text,
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        previous_words=previous_words,
        stage_floor=stage_floor,
        stage_index=stage_index,
    )


def full_repair_attempt_limit(*, stage_index: int, stage_count: int, accepted_words: int, reason: str) -> int:
    reason_lower = reason.lower()
    if any(marker in reason_lower for marker in STYLE_FAILURE_MARKERS):
        return 0
    if accepted_words >= LATE_STAGE_FULL_REPAIR_WORD_LIMIT:
        return 0
    if stage_index == stage_count and ("did not grow" in reason_lower or "below minimum" in reason_lower):
        return 0
    return 2


def stage_required_floor(*, previous_words: int, stage_floor: int, stage_index: int) -> int:
    if stage_index == 1:
        return max(previous_words + 300, int(stage_floor * 0.68))
    elif stage_index == 2:
        return max(previous_words + 450, int(stage_floor * 0.75))
    return max(previous_words + 600, int(stage_floor * 0.85))


def validate_style_gate(result: dict) -> None:
    if not result.get("pass"):
        failures = result.get("failures") or ["Style gate failed without detailed reasons."]
        raise RuntimeError(" | ".join(failures))
    scores = result.get("scores") or {}
    weak = [name for name, value in scores.items() if isinstance(value, (int, float)) and value < 6]
    if weak:
        raise RuntimeError(f"Style gate scores below floor: {', '.join(weak)}")


def is_style_failure(reason: str) -> bool:
    reason_lower = reason.lower()
    return any(marker in reason_lower for marker in STYLE_FAILURE_MARKERS)


def is_hard_failure_reason(reason: str) -> bool:
    reason_lower = reason.lower()
    hard_markers = (
        "forbidden token",
        "preamble residue",
        "unsupported new character",
        "unsupported new characters",
        "unsupported character",
        "unsupported characters",
        "unsupported new teammate",
        "unsupported teammate",
        "unsupported new operator",
        "unsupported operator",
        "introduced unsupported",
        "introduces unsupported",
        "invented named",
        "unnamed operator",
        "extra spoken role",
        "new spoken role",
        "additional somanaut teammate",
    )
    return any(marker in reason_lower for marker in hard_markers)


def stage_output_path(raw_dir: Path, slug: str, stage_index: int, kind: str = "stage") -> Path:
    return raw_dir / f"{slug}.{kind}-{stage_index}.md"


def run_stage(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    dossier_context: str,
    matrix_row: dict,
    target_row: dict,
    current_draft: str,
    stage_index: int,
    stage_count: int,
    stage_low: int,
    stage_high: int,
    raw_dir: Path,
    slug: str,
) -> str:
    prompt = build_stage_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        current_draft=current_draft,
        dossier_context=dossier_context,
        matrix_row=matrix_row,
        target_row=target_row,
        stage_index=stage_index,
        stage_count=stage_count,
        stage_low=stage_low,
        stage_high=stage_high,
    )
    max_tokens = min(10000, 4000 + stage_index * 1500)
    print(
        f"[chapter {chapter_number:02d}] stage={stage_index} nvidia_call=stage model={model} max_tokens={max_tokens} timeout={STAGE_TIMEOUT_SECONDS}s",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are expanding an existing literary science-fantasy chapter into a longer, more embodied novel chapter. "
                    "Preserve canon, grow additively, and output markdown only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
        max_tokens=max_tokens,
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=STAGE_TIMEOUT_SECONDS,
        max_attempts=6,
        retry_backoff_seconds=20,
    )
    text = normalize_chapter_text(
        extract_text(response),
        chapter_number=chapter_number,
        chapter_title=chapter_title,
    )
    stage_output_path(raw_dir, slug, stage_index).write_text(text, encoding="utf-8")
    return text


def run_stage_repair(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    accepted_draft: str,
    failed_candidate: str,
    stage_index: int,
    stage_low: int,
    stage_high: int,
    accepted_words: int,
    required_min_words: int,
    repair_attempt: int,
    focus_notes: str,
    raw_dir: Path,
    slug: str,
) -> str:
    prompt = build_repair_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        accepted_draft=accepted_draft,
        failed_candidate=failed_candidate,
        stage_low=stage_low,
        stage_high=stage_high,
        accepted_words=accepted_words,
        required_min_words=required_min_words,
        repair_attempt=repair_attempt,
        focus_notes=focus_notes,
    )
    max_tokens = min(12000, max(6500, int(stage_high * 1.45)))
    print(
        f"[chapter {chapter_number:02d}] stage={stage_index} nvidia_call=repair attempt={repair_attempt} model={model} max_tokens={max_tokens} timeout={REPAIR_TIMEOUT_SECONDS}s",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You repair an expanded chapter by preserving all existing beats and deepening it additively. "
                    "Output markdown only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=max_tokens,
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=REPAIR_TIMEOUT_SECONDS,
        max_attempts=2,
        retry_backoff_seconds=20,
    )
    text = normalize_chapter_text(
        extract_text(response),
        chapter_number=chapter_number,
        chapter_title=chapter_title,
    )
    stage_output_path(raw_dir, slug, stage_index, kind=f"repair-{repair_attempt}").write_text(text, encoding="utf-8")
    return text


def run_insert_repair(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    accepted_draft: str,
    failed_candidate: str,
    required_new_words: int,
    focus_notes: str,
    raw_dir: Path,
    slug: str,
    stage_index: int,
    insert_attempt: int,
) -> str:
    prompt = build_insert_repair_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        accepted_draft=accepted_draft,
        failed_candidate=failed_candidate,
        required_new_words=required_new_words,
        focus_notes=focus_notes,
        insert_attempt=insert_attempt,
    )
    max_tokens = min(8000, max(3000, int((required_new_words + 350) * 1.8)))
    print(
        f"[chapter {chapter_number:02d}] stage={stage_index} nvidia_call=insert attempt={insert_attempt} model={model} required_new_words={required_new_words} max_tokens={max_tokens} timeout={INSERT_TIMEOUT_SECONDS}s",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You write only additive insertion material for an existing literary science-fantasy chapter. "
                    "Do not rewrite or summarize the full chapter."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.75,
        max_tokens=max_tokens,
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=INSERT_TIMEOUT_SECONDS,
        max_attempts=3,
        retry_backoff_seconds=20,
    )
    raw_insert = normalize_insert_text(extract_text(response))
    stage_output_path(raw_dir, slug, stage_index, kind=f"insert-raw-{insert_attempt}").write_text(
        raw_insert,
        encoding="utf-8",
    )
    insert = dedupe_insert_against_base(base_text=accepted_draft, insert_text=raw_insert)
    if not insert.strip():
        raise RuntimeError("Insert repair returned only duplicate material.")
    insert_path = stage_output_path(raw_dir, slug, stage_index, kind=f"insert-{insert_attempt}")
    insert_path.write_text(insert, encoding="utf-8")
    merged = dedupe_repeated_paragraphs(merge_insert_before_last_paragraph(accepted_draft, insert))
    stage_output_path(raw_dir, slug, stage_index, kind=f"insert-merged-{insert_attempt}").write_text(
        merged,
        encoding="utf-8",
    )
    return merged


def run_style_gate(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    candidate_text: str,
    raw_dir: Path,
    slug: str,
    stage_index: int,
) -> dict:
    prompt = build_style_gate_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        candidate_text=candidate_text,
    )
    print(
        f"[chapter {chapter_number:02d}] stage={stage_index} nvidia_call=style_gate model={model} timeout={STYLE_TIMEOUT_SECONDS}s",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict literary control pass. Output JSON only. "
                    "Assess tone, wit, emotional modulation, and braid balance without rewriting the chapter."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1200,
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=STYLE_TIMEOUT_SECONDS,
        max_attempts=4,
        retry_backoff_seconds=12,
    )
    result = extract_json_object(extract_text(response))
    stage_output_path(raw_dir, slug, stage_index, kind="gate").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def run_voice_repair(
    *,
    model: str,
    chapter_number: int,
    chapter_title: str,
    candidate_text: str,
    minimum_words: int,
    gate_notes: str,
    raw_dir: Path,
    slug: str,
    stage_index: int,
    insert_attempt: int,
    voice_attempt: int,
) -> str:
    prompt = build_voice_repair_prompt(
        chapter_number=chapter_number,
        chapter_title=chapter_title,
        candidate_text=candidate_text,
        minimum_words=minimum_words,
        gate_notes=gate_notes,
        dialogue_matrix=read_excerpt(DIALOGUE_MATRIX, max_chars=5000),
    )
    max_tokens = min(14000, max(9000, int(word_count(candidate_text) * 1.35)))
    print(
        f"[chapter {chapter_number:02d}] stage={stage_index} nvidia_call=voice_repair insert_attempt={insert_attempt} voice_attempt={voice_attempt} model={model} max_tokens={max_tokens} timeout={VOICE_REPAIR_TIMEOUT_SECONDS}s",
        flush=True,
    )
    response = chat_completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You perform final literary acceptance repair on a long chapter. "
                    "Preserve canon and length while fixing voice, wit, tonal modulation, and braid balance. "
                    "Output markdown only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.62,
        max_tokens=max_tokens,
        extra_body={"reasoning_effort": "low"},
        timeout_seconds=VOICE_REPAIR_TIMEOUT_SECONDS,
        max_attempts=2,
        retry_backoff_seconds=20,
    )
    text = normalize_chapter_text(
        extract_text(response),
        chapter_number=chapter_number,
        chapter_title=chapter_title,
    )
    stage_output_path(raw_dir, slug, stage_index, kind=f"voice-repair-{insert_attempt}-{voice_attempt}").write_text(
        text,
        encoding="utf-8",
    )
    return text


def main() -> None:
    args = parse_args()
    meta = working_meta(args.chapter)
    if meta.book_number != args.book:
        raise RuntimeError(f"Chapter {args.chapter:02d} does not belong to book {args.book}")

    manifest_row = load_manifest_row(args.chapter)
    matrix_row = load_matrix_row(args.chapter)
    target_row = load_target_row(args.chapter)

    working_path = REPO_ROOT / meta.working_file
    dossier_path = REPO_ROOT / manifest_row["dossier_file"]
    raw_dir = RAW_ROOT / f"book_{args.book}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    slug = chapter_slug(args.chapter, meta.chapter_title)
    raw_path = raw_dir / f"{slug}.raw.md"
    if args.force:
        for stale_path in raw_dir.glob(f"{slug}*.md"):
            stale_path.unlink()

    current_text = normalize_chapter_text(
        working_path.read_text(encoding="utf-8"),
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
    )
    dossier_text = dossier_path.read_text(encoding="utf-8")
    dossier_context = build_dossier_context(dossier_text)
    current_words = word_count(current_text)
    default_minimum_words = max(int(target_row["macro_target_low"] * 0.8), current_words * 2)
    minimum_words = args.minimum_words if args.minimum_words is not None else default_minimum_words
    if minimum_words <= current_words:
        raise RuntimeError(
            f"--minimum-words must be greater than current chapter length: {minimum_words} <= {current_words}"
        )
    print(
        f"[chapter {args.chapter:02d}] current_words={current_words} minimum_words={minimum_words} default_minimum_words={default_minimum_words}",
        flush=True,
    )

    draft_model, draft_route_notes = resolve_draft_model(
        book_number=args.book,
        matrix_row=matrix_row,
        override=args.draft_model,
    )
    control_model, control_route_notes = resolve_control_model(
        matrix_row=matrix_row,
        override=args.control_model,
    )
    route_notes = draft_route_notes + control_route_notes
    print(f"[chapter {args.chapter:02d}] matrix_draft_model={matrix_row.get('draft_model')}", flush=True)
    print(f"[chapter {args.chapter:02d}] effective_draft_model={draft_model}", flush=True)
    print(f"[chapter {args.chapter:02d}] matrix_control_model={matrix_control_model(matrix_row)}", flush=True)
    print(f"[chapter {args.chapter:02d}] effective_control_model={control_model}", flush=True)
    for note in route_notes:
        print(f"[chapter {args.chapter:02d}] route_note={note}", flush=True)
    if args.print_route:
        return

    stage_targets = build_stage_targets(current_words=current_words, minimum_words=minimum_words)
    draft = current_text
    previous_words = current_words
    for stage_index, stage_low in enumerate(stage_targets, start=1):
        final_stage = stage_index == len(stage_targets)
        stage_high = min(target_row["macro_target_low"], stage_low + 1200)
        print(
            f"[chapter {args.chapter:02d}] stage={stage_index}/{len(stage_targets)} target={stage_low}-{stage_high} previous_words={previous_words}",
            flush=True,
        )
        insert_first_stage = stage_index >= INSERT_FIRST_STAGE_START
        if insert_first_stage:
            candidate = draft
            print(
                f"[chapter {args.chapter:02d}] stage={stage_index} insert_first_skipped_full_stage accepted_words={previous_words}",
                flush=True,
            )
        else:
            candidate = run_stage(
                model=draft_model,
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                dossier_context=dossier_context,
                matrix_row=matrix_row,
                target_row=target_row,
                current_draft=draft,
                stage_index=stage_index,
                stage_count=len(stage_targets),
                stage_low=stage_low,
                stage_high=stage_high,
                raw_dir=raw_dir,
                slug=slug,
            )
            print(
                f"[chapter {args.chapter:02d}] stage={stage_index} draft_words={word_count(candidate)}",
                flush=True,
            )
        try:
            if insert_first_stage:
                insert_floor = (
                    minimum_words
                    if final_stage
                    else stage_required_floor(
                        previous_words=previous_words,
                        stage_floor=stage_low,
                        stage_index=stage_index,
                    )
                )
                if previous_words < insert_floor:
                    raise RuntimeError(f"Insert-first stage growth required: {previous_words} < {insert_floor}")
            validate_candidate_progress(
                candidate,
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                current_words=current_words,
                previous_words=previous_words,
                stage_floor=stage_low,
                stage_index=stage_index,
                final_stage=final_stage,
                minimum_words=minimum_words,
            )
            style_gate = run_style_gate(
                model=control_model,
                chapter_number=args.chapter,
                chapter_title=meta.chapter_title,
                candidate_text=candidate,
                raw_dir=raw_dir,
                slug=slug,
                stage_index=stage_index,
            )
            print(
                f"[chapter {args.chapter:02d}] stage={stage_index} gate_pass scores={style_gate.get('scores', {})}",
                flush=True,
            )
            validate_style_gate(style_gate)
        except RuntimeError as exc:
            print(
                f"[chapter {args.chapter:02d}] stage={stage_index} repair_reason={exc}",
                flush=True,
            )
            failed_candidate = "" if insert_first_stage else candidate
            repair_notes = str(exc)
            failed_candidate_words = previous_words if insert_first_stage else word_count(failed_candidate)
            if failed_candidate and has_hard_validation_failure(failed_candidate, chapter_number=args.chapter):
                failed_candidate = ""
                failed_candidate_words = previous_words
                repair_notes = f"{repair_notes} | failed candidate rejected before repair prompt"
                print(
                    f"[chapter {args.chapter:02d}] stage={stage_index} failed_candidate_hard_failure_omitted_from_repair",
                    flush=True,
                )
            required_min_words = (
                minimum_words
                if final_stage
                else stage_required_floor(
                    previous_words=previous_words,
                    stage_floor=stage_low,
                    stage_index=stage_index,
                )
            )
            initial_partial_growth = failed_candidate_words > previous_words and "below minimum" in repair_notes.lower()
            repair_attempt_count = (
                0
                if initial_partial_growth or insert_first_stage
                else full_repair_attempt_limit(
                    stage_index=stage_index,
                    stage_count=len(stage_targets),
                    accepted_words=previous_words,
                    reason=repair_notes,
                )
            )
            if initial_partial_growth:
                print(
                    f"[chapter {args.chapter:02d}] stage={stage_index} initial_partial_growth_escalate_to_insert words={failed_candidate_words}",
                    flush=True,
                )
            elif repair_attempt_count == 0:
                skip_reason = "insert_first_stage" if insert_first_stage else "late_stage_insert_fallback"
                print(
                    f"[chapter {args.chapter:02d}] stage={stage_index} full_repair_skipped={skip_reason}",
                    flush=True,
                )
            repaired = False
            if failed_candidate_words > previous_words and not has_hard_validation_failure(
                failed_candidate,
                chapter_number=args.chapter,
            ):
                best_candidate = failed_candidate
                best_candidate_words = failed_candidate_words
            else:
                best_candidate = draft
                best_candidate_words = previous_words
            last_repair_words: int | None = None
            for repair_attempt in range(1, repair_attempt_count + 1):
                try:
                    candidate = run_stage_repair(
                        model=draft_model,
                        chapter_number=args.chapter,
                        chapter_title=meta.chapter_title,
                        accepted_draft=draft,
                        failed_candidate=failed_candidate,
                        stage_index=stage_index,
                        stage_low=stage_low,
                        stage_high=stage_high,
                        accepted_words=previous_words,
                        required_min_words=required_min_words,
                        repair_attempt=repair_attempt,
                        focus_notes=repair_notes,
                        raw_dir=raw_dir,
                        slug=slug,
                    )
                except RuntimeError as repair_call_exc:
                    repair_notes = f"{repair_notes} | repair attempt {repair_attempt} call failed: {repair_call_exc}"
                    print(
                        f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} call_failed_escalate_to_insert={repair_call_exc}",
                        flush=True,
                    )
                    break
                repair_words = word_count(candidate)
                print(
                    f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} repair_words={repair_words}",
                    flush=True,
                )
                if repair_words > best_candidate_words and not has_hard_validation_failure(
                    candidate,
                    chapter_number=args.chapter,
                ):
                    best_candidate = candidate
                    best_candidate_words = repair_words
                try:
                    validate_candidate_progress(
                        candidate,
                        chapter_number=args.chapter,
                        chapter_title=meta.chapter_title,
                        current_words=current_words,
                        previous_words=previous_words,
                        stage_floor=stage_low,
                        stage_index=stage_index,
                        final_stage=final_stage,
                        minimum_words=minimum_words,
                    )
                    style_gate = run_style_gate(
                        model=control_model,
                        chapter_number=args.chapter,
                        chapter_title=meta.chapter_title,
                        candidate_text=candidate,
                        raw_dir=raw_dir,
                        slug=slug,
                        stage_index=stage_index,
                    )
                    print(
                        f"[chapter {args.chapter:02d}] stage={stage_index} gate_post_repair scores={style_gate.get('scores', {})}",
                        flush=True,
                    )
                    validate_style_gate(style_gate)
                    repaired = True
                    break
                except RuntimeError as repair_exc:
                    repair_notes = f"{repair_notes} | repair attempt {repair_attempt}: {repair_exc}"
                    print(
                        f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} failed={repair_exc}",
                        flush=True,
                    )
                    repair_failure = str(repair_exc)
                    if is_hard_failure_reason(repair_failure):
                        failed_candidate = ""
                        candidate = draft
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} hard_failure_reverted_to_last_clean",
                            flush=True,
                        )
                        break
                    failed_candidate = candidate
                    if any(marker in repair_failure.lower() for marker in STYLE_FAILURE_MARKERS):
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} style_failure_escalate_to_insert",
                            flush=True,
                        )
                        break
                    if repair_words <= previous_words:
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} non_additive_repair_escalate_to_insert",
                            flush=True,
                        )
                        break
                    if "below minimum pass floor" in repair_failure and repair_words > previous_words:
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} partial_growth_escalate_to_insert",
                            flush=True,
                        )
                        break
                    if last_repair_words == repair_words:
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} repair_attempt={repair_attempt} duplicate_repair_words_escalate_to_insert",
                            flush=True,
                        )
                        break
                    last_repair_words = repair_words
            if not repaired:
                candidate = best_candidate
                insert_notes = sanitize_failure_note(repair_notes, chapter_number=args.chapter)
                duplicate_insert_failures = 0
                for insert_attempt in range(1, INSERT_FALLBACK_ATTEMPTS + 1):
                    required_new_words = max(required_min_words - word_count(candidate), 300)
                    requested_new_words = min(required_new_words, MAX_INSERT_REQUEST_WORDS)
                    if duplicate_insert_failures >= DUPLICATE_INSERT_FALLBACK_AFTER:
                        requested_new_words = min(requested_new_words, POST_HARD_FAILURE_MAX_INSERT_WORDS)
                    insert_model = (
                        control_model
                        if duplicate_insert_failures >= DUPLICATE_INSERT_FALLBACK_AFTER
                        else draft_model
                    )
                    print(
                        f"[chapter {args.chapter:02d}] stage={stage_index} insert_fallback attempt={insert_attempt} required_new_words={required_new_words} requested_new_words={requested_new_words} model={insert_model}",
                        flush=True,
                    )
                    candidate_before_insert = candidate
                    try:
                        candidate = run_insert_repair(
                            model=insert_model,
                            chapter_number=args.chapter,
                            chapter_title=meta.chapter_title,
                            accepted_draft=candidate_before_insert,
                            failed_candidate="" if duplicate_insert_failures >= DUPLICATE_INSERT_FALLBACK_AFTER else failed_candidate,
                            required_new_words=requested_new_words,
                            focus_notes=insert_notes,
                            raw_dir=raw_dir,
                            slug=slug,
                            stage_index=stage_index,
                            insert_attempt=insert_attempt,
                        )
                    except RuntimeError as insert_call_exc:
                        if "duplicate material" in str(insert_call_exc).lower():
                            duplicate_insert_failures += 1
                        insert_notes = (
                            f"{insert_notes} | insert attempt {insert_attempt} call failed: "
                            f"{sanitize_failure_note(str(insert_call_exc), chapter_number=args.chapter)}"
                        )
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} insert_attempt={insert_attempt} call_failed={insert_call_exc}",
                            flush=True,
                        )
                        continue
                    print(
                        f"[chapter {args.chapter:02d}] stage={stage_index} insert_attempt={insert_attempt} insert_merged_words={word_count(candidate)}",
                        flush=True,
                    )
                    try:
                        validate_candidate_progress(
                            candidate,
                            chapter_number=args.chapter,
                            chapter_title=meta.chapter_title,
                            current_words=current_words,
                            previous_words=previous_words,
                            stage_floor=stage_low,
                            stage_index=stage_index,
                            final_stage=final_stage,
                            minimum_words=minimum_words,
                        )
                        style_gate = run_style_gate(
                            model=control_model,
                            chapter_number=args.chapter,
                            chapter_title=meta.chapter_title,
                            candidate_text=candidate,
                            raw_dir=raw_dir,
                            slug=slug,
                            stage_index=stage_index,
                        )
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} gate_post_insert scores={style_gate.get('scores', {})}",
                            flush=True,
                        )
                        validate_style_gate(style_gate)
                        break
                    except RuntimeError as insert_exc:
                        insert_failure = str(insert_exc)
                        hard_insert_failure = is_hard_failure_reason(insert_failure)
                        failed_candidate = "" if hard_insert_failure else candidate
                        if hard_insert_failure:
                            contaminated_words = word_count(candidate)
                            candidate = candidate_before_insert
                            insert_notes = (
                                f"{insert_notes} | insert attempt {insert_attempt}: hard validation failure "
                                f"| contaminated candidate rejected at {contaminated_words} words "
                                f"| next insert must avoid explicit scaffold, unsupported names, and setting drift"
                            )
                        else:
                            insert_notes = (
                                f"{insert_notes} | insert attempt {insert_attempt}: "
                                f"{sanitize_failure_note(insert_failure, chapter_number=args.chapter)}"
                            )
                        print(
                            f"[chapter {args.chapter:02d}] stage={stage_index} insert_attempt={insert_attempt} failed={insert_failure}",
                            flush=True,
                        )
                        if hard_insert_failure:
                            duplicate_insert_failures = max(
                                duplicate_insert_failures,
                                DUPLICATE_INSERT_FALLBACK_AFTER,
                            )
                            print(
                                f"[chapter {args.chapter:02d}] stage={stage_index} insert_attempt={insert_attempt} hard_failure_reverted_to_last_clean_switch_to_control clean_words={word_count(candidate)}",
                                flush=True,
                            )
                            continue
                        candidate_reached_minimum = word_count(candidate) >= minimum_words
                        if candidate_reached_minimum and is_style_failure(insert_failure):
                            voice_repaired = False
                            for voice_attempt in range(1, VOICE_REPAIR_ATTEMPTS + 1):
                                voice_candidate = candidate
                                try:
                                    voice_candidate = run_voice_repair(
                                        model=control_model,
                                        chapter_number=args.chapter,
                                        chapter_title=meta.chapter_title,
                                        candidate_text=candidate,
                                        minimum_words=minimum_words,
                                        gate_notes=insert_notes,
                                        raw_dir=raw_dir,
                                        slug=slug,
                                        stage_index=stage_index,
                                        insert_attempt=insert_attempt,
                                        voice_attempt=voice_attempt,
                                    )
                                    print(
                                        f"[chapter {args.chapter:02d}] stage={stage_index} voice_repair_attempt={voice_attempt} words={word_count(voice_candidate)}",
                                        flush=True,
                                    )
                                    validate_candidate_progress(
                                        voice_candidate,
                                        chapter_number=args.chapter,
                                        chapter_title=meta.chapter_title,
                                        current_words=current_words,
                                        previous_words=previous_words,
                                        stage_floor=stage_low,
                                        stage_index=stage_index,
                                        final_stage=final_stage or candidate_reached_minimum,
                                        minimum_words=minimum_words,
                                    )
                                    style_gate = run_style_gate(
                                        model=control_model,
                                        chapter_number=args.chapter,
                                        chapter_title=meta.chapter_title,
                                        candidate_text=voice_candidate,
                                        raw_dir=raw_dir,
                                        slug=slug,
                                        stage_index=stage_index,
                                    )
                                    print(
                                        f"[chapter {args.chapter:02d}] stage={stage_index} gate_post_voice_repair scores={style_gate.get('scores', {})}",
                                        flush=True,
                                    )
                                    validate_style_gate(style_gate)
                                    candidate = voice_candidate
                                    voice_repaired = True
                                    break
                                except RuntimeError as voice_exc:
                                    failed_candidate = voice_candidate
                                    insert_notes = (
                                        f"{insert_notes} | voice repair attempt {voice_attempt}: "
                                        f"{sanitize_failure_note(str(voice_exc), chapter_number=args.chapter)}"
                                    )
                                    print(
                                        f"[chapter {args.chapter:02d}] stage={stage_index} voice_repair_attempt={voice_attempt} failed={voice_exc}",
                                        flush=True,
                                    )
                            if voice_repaired:
                                break
                else:
                    raise RuntimeError(
                        f"Stage {stage_index} insert fallback failed after {INSERT_FALLBACK_ATTEMPTS} attempts: {insert_notes}"
                    )
        draft = candidate
        previous_words = word_count(draft)

    text = draft
    raw_path.write_text(text, encoding="utf-8")
    validate_chapter(
        text,
        chapter_number=args.chapter,
        chapter_title=meta.chapter_title,
        current_words=current_words,
        minimum_words=minimum_words,
    )

    working_path.write_text(text, encoding="utf-8")
    print(f"Wrote {working_path}")
    print(f"Wrote {raw_path}")
    print(f"before_words={current_words}")
    print(f"after_words={word_count(text)}")
    print(f"minimum_words={minimum_words}")


if __name__ == "__main__":
    main()
