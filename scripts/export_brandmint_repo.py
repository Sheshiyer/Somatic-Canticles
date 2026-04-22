#!/usr/bin/env python3
"""Assemble a standalone GitHub-ready Brandmint package for Somatic Canticles."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable


REPO_SLUG = "somatic-canticles-brandmint-kit"
COMMIT_MESSAGE = "feat: initial Somatic Canticles Brandmint kit"
COPY_IGNORE_NAMES = {
    ".DS_Store",
    ".astro",
    ".vercel",
    "node_modules",
    ".brandmint",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp") / REPO_SLUG,
        help="Destination directory for the standalone repo package.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Remove the output directory first if it already exists.",
    )
    return parser.parse_args()


def ensure_clean_output(path: Path, force: bool) -> None:
    if not path.exists():
        return
    if not force:
        raise SystemExit(f"Output directory already exists: {path}. Use --force to replace it.")
    shutil.rmtree(path)


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=False,
        ignore=shutil.ignore_patterns(*sorted(COPY_IGNORE_NAMES)),
    )


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def load_manifest(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text())


def classify_asset_id(asset_id: str) -> str:
    if asset_id.startswith("ARCANA-"):
        return "arcana"
    if asset_id.startswith("ANATOMY-"):
        return "anatomy"
    if asset_id.startswith("COVER-"):
        return "covers"
    if asset_id.startswith("LOGO-"):
        return "logos"
    if asset_id == "2A":
        return "brand-kit"
    return "other"


def count_manifest_assets(assets: Iterable[Dict[str, object]]) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for asset in assets:
        counter[classify_asset_id(str(asset.get("id", "")))] += 1
    return dict(counter)


def count_site_assets(images_root: Path) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for path in images_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "README.md" or path.name == "media-manifest.json":
            continue
        family = path.parent.name
        counter[family] += 1
    return dict(counter)


def build_readme(product_name: str, manifest: Dict[str, object], manifest_counts: Dict[str, int]) -> str:
    estimated_cost = manifest.get("estimated_cost_usd", "unknown")
    total_assets = manifest.get("total_assets", "unknown")
    total_api_calls = manifest.get("total_api_calls", "unknown")
    count_lines = "\n".join(f"- {family}: {count}" for family, count in sorted(manifest_counts.items()))
    return f"""# {product_name} Brandmint Kit

This repository is a standalone Brandmint package for **{product_name}**.

It packages the current source-of-truth brand inputs, generated asset manifest, Astro wiki source, and built wiki output into a separate repo that can be published independently from the larger manuscript repository.

## Included

- `brandmint-input/`
- `brand-wiki-site/`
- `docs/BRANDMINT_WAVE_0_9_AUDIT.md`
- `export-manifest.json`
- `PUBLISHING.md`

## Current Asset Inventory

- total manifest assets: {total_assets}
- total estimated API cost: ${estimated_cost}
- total API calls: {total_api_calls}

Breakdown:

{count_lines}

## Build The Astro Site

```bash
cd brand-wiki-site
bun install
bun run build
```

## Publish To GitHub

Default suggested repo slug: `{REPO_SLUG}`

See [`PUBLISHING.md`](./PUBLISHING.md) for the exact local git + `gh` commands.
"""


def build_publishing_guide(output_dir: Path) -> str:
    return f"""# Publishing Guide

Safe default:

- repo name: `{REPO_SLUG}`
- visibility: `private`

From inside this exported directory:

```bash
cd {output_dir}
git init -b main
git add .
git commit -m "{COMMIT_MESSAGE}"
gh repo create Sheshiyer/{REPO_SLUG} --private --source=. --remote=origin --push
```

If you want the repo public, replace `--private` with `--public`.
"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent

    brandmint_input = repo_root / "brandmint-input"
    brand_wiki_site = repo_root / "brand-wiki-site"
    audit_doc = repo_root / "00_PLANNING_AND_ROADMAP" / "BRANDMINT_WAVE_0_9_AUDIT.md"
    product_md = brandmint_input / "product.md"
    manifest_path = brandmint_input / "somatic-canticles" / "generation-manifest.json"
    images_root = brand_wiki_site / "src" / "images"

    manifest = load_manifest(manifest_path)
    manifest_assets = manifest.get("assets", [])
    if not isinstance(manifest_assets, list):
        raise SystemExit(f"Unexpected manifest asset structure in {manifest_path}")

    product_name = "Somatic Canticles"
    for line in product_md.read_text().splitlines():
        if line.strip() and not line.startswith("#") and line.strip() != "Somatic Canticles":
            continue
        if line.strip() == "Somatic Canticles":
            product_name = line.strip()
            break

    manifest_counts = count_manifest_assets(manifest_assets)
    site_counts = count_site_assets(images_root)

    ensure_clean_output(args.output, args.force)
    args.output.mkdir(parents=True, exist_ok=True)

    copy_tree(brandmint_input, args.output / "brandmint-input")
    copy_tree(brand_wiki_site, args.output / "brand-wiki-site")
    copy_file(audit_doc, args.output / "docs" / audit_doc.name)

    write_text(args.output / "README.md", build_readme(product_name, manifest, manifest_counts))
    write_text(
        args.output / "PUBLISHING.md",
        build_publishing_guide(args.output),
    )
    write_text(
        args.output / ".gitignore",
        ".DS_Store\nnode_modules/\n.brandmint/\n.env\n.env.*\n",
    )

    export_manifest = {
        "product_name": product_name,
        "suggested_repo_slug": REPO_SLUG,
        "source_repo_root": str(repo_root),
        "included_paths": [
            "brandmint-input/",
            "brand-wiki-site/",
            "docs/BRANDMINT_WAVE_0_9_AUDIT.md",
            "README.md",
            "PUBLISHING.md",
            ".gitignore",
        ],
        "manifest_asset_counts": manifest_counts,
        "site_asset_counts": site_counts,
        "estimated_cost_usd": manifest.get("estimated_cost_usd"),
        "total_assets": manifest.get("total_assets"),
        "total_api_calls": manifest.get("total_api_calls"),
    }
    write_text(args.output / "export-manifest.json", json.dumps(export_manifest, indent=2) + "\n")

    print(f"Exported standalone repo package to: {args.output}")
    print(json.dumps(export_manifest, indent=2))


if __name__ == "__main__":
    main()
