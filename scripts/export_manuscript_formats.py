#!/usr/bin/env python3
"""Generate distributable manuscript exports from the normalized Somatic Canticles omnibus."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


TITLE = "Somatic Canticles"
AUTHOR = "Shesh Iyer"
LANG = "en-US"
RIGHTS = "Copyright © 2026 Shesh Iyer. All rights reserved."


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=repo_root / "02_MANUSCRIPTS" / "COMPILED" / "Somatic_Canticles_Trilogy_Omnibus_CLEAN.md",
        help="Normalized omnibus markdown file to export.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=repo_root / "02_MANUSCRIPTS" / "EXPORTS",
        help="Directory where generated export artifacts will be written.",
    )
    return parser.parse_args()


def require_command(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required command not found: {name}")
    return path


def command_works(name: str, args: list[str] | None = None) -> bool:
    path = shutil.which(name)
    if not path:
        return False
    command = [path, *(args or ["--version"])]
    completed = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_pandoc(pandoc: str, source: Path, destination: Path, extra_args: list[str]) -> None:
    command = [
        pandoc,
        str(source),
        "--standalone",
        "--toc",
        "--toc-depth=3",
        "--metadata",
        f"title={TITLE}",
        "--metadata",
        f"author={AUTHOR}",
        "--metadata",
        f"lang={LANG}",
        "--metadata",
        f"rights={RIGHTS}",
        "-o",
        str(destination),
        *extra_args,
    ]
    subprocess.run(command, check=True)


def first_available_pdf_engine() -> str | None:
    for candidate in ("tectonic", "xelatex", "pdflatex"):
        if command_works(candidate):
            return candidate
    return None


def pdf_skip_reason() -> str:
    if shutil.which("weasyprint"):
        if command_works("weasyprint"):
            return "A PDF helper is present (`weasyprint`), but no supported pandoc PDF engine (`tectonic`, `xelatex`, or `pdflatex`) is installed."
        return "WeasyPrint is installed but not usable in this environment."
    if shutil.which("wkhtmltopdf"):
        if command_works("wkhtmltopdf"):
            return "wkhtmltopdf is available, but this exporter is currently configured for `tectonic`, `xelatex`, or `pdflatex`."
        return "wkhtmltopdf is installed but not usable in this environment."
    return "No supported PDF engine found. Install `tectonic`, `xelatex`, or `pdflatex`."


def build_manifest(source: Path, output_dir: Path, generated: dict[str, dict[str, object]], pdf_status: dict[str, object]) -> dict[str, object]:
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": str(source),
        "source_sha256": sha256(source),
        "output_dir": str(output_dir),
        "artifacts": generated,
        "pdf_status": pdf_status,
    }


def artifact_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_readme(output_dir: Path, generated: dict[str, dict[str, object]], pdf_status: dict[str, object]) -> None:
    lines = [
        "# Somatic Canticles Export Package",
        "",
        f"Source omnibus: `../COMPILED/Somatic_Canticles_Trilogy_Omnibus_CLEAN.md`",
        "",
        "Generated artifacts:",
    ]
    for label in ("html", "epub"):
        artifact = generated.get(label)
        if artifact:
            lines.append(f"- `{Path(str(artifact['path'])).name}`")
    if pdf_status["state"] == "generated":
        lines.append(f"- `{Path(str(pdf_status['path'])).name}`")
    else:
        lines.append(f"- PDF not generated: {pdf_status['reason']}")
    lines.append("")
    lines.append("See `export-manifest.json` for sizes, input hash, and generation metadata.")
    (output_dir / "README.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    args = parse_args()
    source = args.input.resolve()
    if not source.exists():
        raise SystemExit(f"Input omnibus not found: {source}")

    pandoc = require_command("pandoc")
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / f"{source.stem}.html"
    epub_path = output_dir / f"{source.stem}.epub"

    run_pandoc(pandoc, source, html_path, ["--from=gfm", "--to=html5"])
    run_pandoc(pandoc, source, epub_path, ["--from=gfm", "--to=epub3", "--split-level=1"])

    generated = {
        "html": artifact_record(html_path),
        "epub": artifact_record(epub_path),
    }

    pdf_engine = first_available_pdf_engine()
    pdf_status: dict[str, object]
    if pdf_engine:
        pdf_path = output_dir / f"{source.stem}.pdf"
        run_pandoc(
            pandoc,
            source,
            pdf_path,
            ["--from=gfm", "--to=pdf", f"--pdf-engine={pdf_engine}"],
        )
        pdf_status = {"state": "generated", "engine": pdf_engine, **artifact_record(pdf_path)}
    else:
        pdf_status = {"state": "skipped", "reason": pdf_skip_reason()}

    manifest = build_manifest(source, output_dir, generated, pdf_status)
    (output_dir / "export-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    write_readme(output_dir, generated, pdf_status)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
