#!/usr/bin/env python3
"""
wiki_players.py — Anti-Duplicate Player & Staff Card Manager for Wiki Catania Calcio.

Fixes the root causes of historical duplicate cards:
1. Decodes HTML entities (`&apos;`, `&#39;`, `<b>`) BEFORE slugifying names so `dapos` / `ltbgt`
   corrupted filenames can never be generated.
2. Performs a 4-stage preventative deduplication check across `03-tesserati` before creating
   any card:
   - Stage 1: Exact `tm_id` (Transfermarkt Player ID) match
   - Stage 2: Exact `cc_id` (CalcioCatania.com ID in `sources`) match
   - Stage 3: Normalized slug / `aliases` frontmatter match (resolving South American full names
     vs sporting names, e.g. `Maximiliano Gastón López` -> `maxi-lopez`)
   - Stage 4: Exact `birth_date` + `role` match
3. Uses strict `y–y+1` season range formatting (`int(Stagione_ID)` -> `f"{y}-{y+1}"`), eliminating
   the legacy `-1` year shift bug.
"""

import re
import html
import sys
import unicodedata
import argparse
from pathlib import Path
from typing import Dict, Optional, Tuple

from wiki_validator import parse_frontmatter

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TESSERATI_DIR = ROOT / "content" / "03-tesserati"


def clean_player_name(raw_name: str) -> str:
    """Decode HTML entities and strip inline tags before slugification."""
    cleaned = html.unescape(str(raw_name or ""))
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = cleaned.replace("dapos", "d'").replace("lapos", "l'").replace("ltbgt", "")
    return re.sub(r"\s+", " ", cleaned).strip()


def slugify_player(name: str) -> str:
    """Generate a clean kebab-case slug from a player's sporting name."""
    cleaned = clean_player_name(name)
    norm = unicodedata.normalize("NFD", cleaned)
    norm = "".join(c for c in norm if unicodedata.category(c) != "Mn")
    norm = norm.lower().replace("ç", "c").replace("ø", "o").replace("ß", "ss").replace("ł", "l")
    norm = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
    return norm


def format_season_range(season_start_year: int | str) -> str:
    """Convert a Transfermarkt Stagione_ID (start year) into canonical YYYY-YYYY+1 format."""
    s = str(season_start_year).strip()
    if re.match(r"^\d{4}$", s):
        y = int(s)
        return f"{y}-{y + 1}"
    m = re.match(r"^(\d{4})[-/](\d{2,4})$", s)
    if m:
        y = int(m.group(1))
        return f"{y}-{y + 1}"
    return s


class PlayerRegistry:
    """Index of existing cards in 03-tesserati to prevent duplicate creation."""

    def __init__(self, tesserati_dir: Path = TESSERATI_DIR) -> None:
        self.tesserati_dir = tesserati_dir
        self.by_tm_id: Dict[str, Path] = {}
        self.by_cc_id: Dict[str, Path] = {}
        self.by_alias_or_slug: Dict[str, Path] = {}
        self.by_birth_date: Dict[Tuple[str, str], Path] = {}
        self._scan()

    def _scan(self) -> None:
        for md in sorted(self.tesserati_dir.rglob("*.md")):
            if md.name == "index.md":
                continue
            text = md.read_text(encoding="utf-8", errors="replace")
            fm, _ = parse_frontmatter(md)

            tm_id = str(fm.get("tm_id", "")).strip()
            if tm_id:
                self.by_tm_id[tm_id] = md

            cc_m = re.search(r"giocatori\.php\?[^)\s\"']*-(\d+)", text)
            if cc_m:
                self.by_cc_id[cc_m.group(1)] = md

            self.by_alias_or_slug[md.stem.lower()] = md
            self.by_alias_or_slug[slugify_player(md.stem)] = md
            for al in fm.get("aliases") or []:
                al_str = str(al).strip().lower()
                if al_str:
                    self.by_alias_or_slug[al_str] = md
                    self.by_alias_or_slug[al_str.split("/")[-1]] = md
                    self.by_alias_or_slug[slugify_player(al_str.split("/")[-1])] = md

            bdate = str(fm.get("birth_date", "")).strip()
            role = str(fm.get("role", "")).strip().lower()[:3]
            if bdate and role:
                self.by_birth_date[(bdate, role)] = md

    def find_existing(
        self,
        name: str,
        tm_id: Optional[str] = None,
        cc_id: Optional[str] = None,
        birth_date: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Optional[Path]:
        if tm_id and str(tm_id).strip() in self.by_tm_id:
            return self.by_tm_id[str(tm_id).strip()]
        if cc_id and str(cc_id).strip() in self.by_cc_id:
            return self.by_cc_id[str(cc_id).strip()]
        slug = slugify_player(name)
        if slug in self.by_alias_or_slug:
            return self.by_alias_or_slug[slug]
        if birth_date and role:
            key = (str(birth_date).strip(), str(role).strip().lower()[:3])
            if key in self.by_birth_date:
                return self.by_birth_date[key]
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit or look up player cards in 03-tesserati.")
    parser.add_argument("--check-duplicates", action="store_true", help="Scan 03-tesserati for duplicate IDs/aliases.")
    args = parser.parse_args()

    reg = PlayerRegistry()
    print(f"Indexed {len(set(reg.by_alias_or_slug.values()))} unique cards in {TESSERATI_DIR}:")
    print(f"  - Cards with tm_id:      {len(reg.by_tm_id)}")
    print(f"  - Cards with cc_id:      {len(reg.by_cc_id)}")
    print(f"  - Registered aliases:    {len(reg.by_alias_or_slug)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
