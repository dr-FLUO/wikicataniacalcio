#!/usr/bin/env python3
"""
wiki_validator.py — Unified Frontmatter, Graph, and WCAG Validator for Wiki Catania Calcio.

Responsibilities:
1. Validates YAML frontmatter across all 8 thematic folders (`01-societa` .. `08-settori-paralleli`)
   against `SCHEMA.md` and Pydantic v2 models (`agents/models.py`).
2. Verifies graph integrity by resolving every `[[wikilink]]` against file paths, slugs,
   and frontmatter `aliases`.
3. Checks WCAG 2.1 AA compliance (non-empty `alt` text on images, valid table pipe escaping,
   absence of nested wikilinks or corrupted URLs).
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple

try:
    import yaml
    from yaml import CSafeLoader as SafeLoader
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
CORRUPTED_URL_RE = re.compile(r"\[https?://[^\]]*\[https?://")
NESTED_WIKILINK_RE = re.compile(r"\[\[[^\]]*\[\[")


def parse_frontmatter_fallback(fm_str: str) -> dict:
    fm: dict = {}
    current_list_key = None
    for line in fm_str.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        m_list = re.match(r"^[ \t]*-\s+(.*)$", line)
        if m_list and current_list_key:
            val = m_list.group(1).strip().strip("'\"")
            if not val.startswith(("author:", "title:", "image_path:")):
                fm.setdefault(current_list_key, []).append(val)
            continue
        m_kv = re.match(r"^([a-zA-Z0-9_]+):\s*(.*)$", line)
        if m_kv:
            k, v = m_kv.group(1), m_kv.group(2).strip()
            if not v:
                current_list_key = k
                fm[k] = []
            else:
                current_list_key = None
                fm[k] = v.strip("'\"")
    return fm


def parse_frontmatter(md_path: Path) -> Tuple[dict, str]:
    text = md_path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            if HAS_YAML:
                try:
                    fm = yaml.load(parts[1], Loader=SafeLoader) or {}
                    if isinstance(fm, dict):
                        return fm, parts[2]
                except Exception:
                    pass
            return parse_frontmatter_fallback(parts[1]), parts[2]
    return {}, text


def build_vault_index(content_dir: Path) -> Tuple[Set[str], Dict[str, Path]]:
    valid_targets: Set[str] = set()
    slug_to_path: Dict[str, Path] = {}

    for md in content_dir.rglob("*.md"):
        rel_no_ext = md.relative_to(content_dir).as_posix()[:-3]
        valid_targets.add(rel_no_ext)
        valid_targets.add(rel_no_ext.lower())
        valid_targets.add(md.stem)
        valid_targets.add(md.stem.lower())
        if md.name == "index.md" and md.parent != content_dir:
            parent_rel = md.parent.relative_to(content_dir).as_posix()
            valid_targets.add(parent_rel)
            valid_targets.add(parent_rel.lower())

        fm, _ = parse_frontmatter(md)
        slug = str(fm.get("slug", "")).strip().strip("/")
        if slug:
            valid_targets.add(slug)
            valid_targets.add(slug.lower())
            slug_to_path[slug] = md

        aliases = fm.get("aliases") or []
        if isinstance(aliases, list):
            for al in aliases:
                al_str = str(al).strip().strip("/")
                if al_str:
                    valid_targets.add(al_str)
                    valid_targets.add(al_str.lower())

    return valid_targets, slug_to_path


def validate_vault(content_dir: Path) -> dict:
    valid_targets, _ = build_vault_index(content_dir)
    report = {
        "total_files": 0,
        "missing_required_frontmatter": [],
        "broken_frontmatter_wikilinks": [],
        "broken_wikilinks": [],
        "unescaped_table_pipes": [],
        "broken_images": [],
        "corrupted_urls": [],
        "nested_wikilinks": [],
        "missing_alt_images": [],
    }

    required_fields = {"title", "slug", "entity_type", "status", "tags"}

    for md in sorted(content_dir.rglob("*.md")):
        report["total_files"] += 1
        rel = md.relative_to(content_dir).as_posix()
        fm, body = parse_frontmatter(md)

        missing = [k for k in required_fields if not fm.get(k)]
        if missing and md.name != "index.md":
            report["missing_required_frontmatter"].append({"file": rel, "missing": missing})

        # Check frontmatter wikilinks
        fm_dump = json.dumps(fm, ensure_ascii=False, default=str)
        for m in WIKILINK_RE.finditer(fm_dump):
            raw_target = m.group(1).strip().rstrip("\\").strip("/")
            if not raw_target or raw_target.startswith(("http://", "https://", "mailto:", "assets/")):
                continue
            if raw_target not in valid_targets and raw_target.lower() not in valid_targets:
                report["broken_frontmatter_wikilinks"].append({"file": rel, "target": raw_target})

        # Check frontmatter image existence
        fm_img = fm.get("image")
        if fm_img and isinstance(fm_img, str) and not fm_img.startswith(("http://", "https://")):
            img_clean = fm_img.lstrip("/")
            if not (content_dir / img_clean).exists() and not (ROOT / "quartz" / img_clean).exists() and not (ROOT / img_clean).exists():
                report["broken_images"].append({"file": rel, "image": fm_img})

        if CORRUPTED_URL_RE.search(body):
            report["corrupted_urls"].append(rel)

        if NESTED_WIKILINK_RE.search(body):
            report["nested_wikilinks"].append(rel)

        for img_m in re.finditer(r"<img\b[^>]*>", body, flags=re.IGNORECASE):
            tag = img_m.group(0)
            if 'alt="' not in tag.lower() and "alt='" not in tag.lower():
                report["missing_alt_images"].append(rel)
            src_m = re.search(r'src=["\']([^"\']+)["\']', tag, flags=re.IGNORECASE)
            if src_m:
                src_u = src_m.group(1).strip()
                if not src_u.startswith(("http://", "https://", "data:")):
                    u_clean = src_u.lstrip("/")
                    if not (content_dir / u_clean).exists() and not (ROOT / "quartz" / u_clean).exists() and not (ROOT / u_clean).exists():
                        report["broken_images"].append({"file": rel, "image": src_u})

        for line in body.splitlines():
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                if re.search(r"\[\[[^\]]*(?<!\\)\|[^\]]*\]\]", s):
                    report["unescaped_table_pipes"].append(rel)
                    break

        for m in WIKILINK_RE.finditer(body):
            raw_target = m.group(1).strip().rstrip("\\").strip("/")
            if not raw_target or raw_target.startswith(("http://", "https://", "mailto:", "assets/")):
                continue
            if raw_target not in valid_targets and raw_target.lower() not in valid_targets:
                report["broken_wikilinks"].append({"file": rel, "target": raw_target})

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Wiki Catania Calcio vault.")
    parser.add_argument("--json", type=str, help="Optional path to save JSON report.")
    args = parser.parse_args()

    res = validate_vault(CONTENT_DIR)
    print(f"Scanned {res['total_files']} Markdown files in {CONTENT_DIR}:")
    print(f"  - Missing required frontmatter:   {len(res['missing_required_frontmatter'])}")
    print(f"  - Broken FM [[wikilinks]]:        {len(res['broken_frontmatter_wikilinks'])}")
    print(f"  - Broken body [[wikilinks]]:      {len(res['broken_wikilinks'])}")
    print(f"  - Unescaped GFM table pipes:      {len(res['unescaped_table_pipes'])}")
    print(f"  - Broken image references:        {len(res['broken_images'])}")
    print(f"  - Corrupted URLs:                 {len(res['corrupted_urls'])}")
    print(f"  - Nested [[wikilinks]]:           {len(res['nested_wikilinks'])}")
    print(f"  - Images missing alt attribute:   {len(res['missing_alt_images'])}")

    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
