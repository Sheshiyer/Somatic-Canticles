#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="/Volumes/madara/2026/Somatic-Canticles/somatic-canticles/generated"
TARGET_DIR="$(cd "$(dirname "$0")/.." && pwd)/src/images"

mkdir -p "$TARGET_DIR"/{arcana,anatomy,covers,logos,brand-kit}

# Clean only generated webp targets (keeps README/manifest files intact)
find "$TARGET_DIR"/arcana "$TARGET_DIR"/anatomy "$TARGET_DIR"/covers "$TARGET_DIR"/logos "$TARGET_DIR"/brand-kit -type f -name '*.webp' -delete

while IFS= read -r f; do
  base="$(basename "$f")"

  if [[ "$base" =~ ^[0-9]{2}-.*\.webp$ ]]; then
    cp "$f" "$TARGET_DIR/arcana/$base"
  elif [[ "$base" == anatomy-*.webp ]]; then
    cp "$f" "$TARGET_DIR/anatomy/$base"
  elif [[ "$base" == book-cover-*.webp ]]; then
    cp "$f" "$TARGET_DIR/covers/$base"
  elif [[ "$base" == logo-*.webp ]]; then
    cp "$f" "$TARGET_DIR/logos/$base"
  elif [[ "$base" == brand-kit-*.webp ]]; then
    cp "$f" "$TARGET_DIR/brand-kit/$base"
  fi
done < <(find "$SOURCE_DIR" -maxdepth 1 -type f -name '*.webp' | sort)

TARGET_DIR="$TARGET_DIR" python3 - <<'PY'
import json, os, glob
base=os.environ['TARGET_DIR']
cats=['arcana','anatomy','covers','logos','brand-kit']
manifest={
  'source':'/Volumes/madara/2026/Somatic-Canticles/somatic-canticles/generated',
  'target':base,
  'format':'webp',
  'categories':{},
  'counts':{},
  'total':0,
}
for c in cats:
  files=sorted([os.path.basename(p) for p in glob.glob(os.path.join(base,c,'*.webp'))])
  manifest['categories'][c]=files
  manifest['counts'][c]=len(files)
  manifest['total']+=len(files)
out=os.path.join(base,'media-manifest.json')
with open(out,'w') as f:
  json.dump(manifest,f,indent=2)
print('Updated',out)
print('Total assets:',manifest['total'])
PY

echo "Sync complete: $TARGET_DIR"
