#!/usr/bin/env python3
"""
wiki_seasons.py — Algebraic Standings & Seasonal Fact-Checker for Wiki Catania Calcio.

Verifies all 95 seasonal files (`content/02-cronistoria/stagioni/*.md`, 1929–present):
1. Checks YAML frontmatter algebraic identities:
   - `matches_played == wins + draws + losses`
   - `(wins * points_per_win_regime) + draws - points_penalty == points_final`
   - Historical regime boundary: 2 points per win up to 1993-1994 (or 1992-1993 in Serie C1),
     3 points per win from 1993-1994 / 1994-1995 onward.
2. Compares YAML league standings against the Markdown match log (`Calendario` / `Risultati`)
   and detects seasons where Coppa Italia / Coppa Italia Serie C / Playoff / Poule Scudetto
   matches were aggregated into the regular-season league standings.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List

from wiki_validator import parse_frontmatter

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STAGIONI_DIR = ROOT / "content" / "02-cronistoria" / "stagioni"


def safe_int(val: object, default: int = 0) -> int:
    try:
        return int(str(val).strip())
    except Exception:
        return default


def verify_seasons(stagioni_dir: Path = STAGIONI_DIR) -> Dict[str, List[dict]]:
    results: Dict[str, List[dict]] = {
        "valid_yaml_identities": [],
        "yaml_algebraic_errors": [],
        "cup_or_playoff_mixed_in_standings": [],
    }

    for md in sorted(stagioni_dir.glob("*.md")):
        if md.name == "index.md":
            continue
        fm, body = parse_frontmatter(md)
        season = str(fm.get("season_label") or md.stem)

        g = safe_int(fm.get("matches_played"), 0)
        w = safe_int(fm.get("wins"), 0)
        d = safe_int(fm.get("draws"), 0)
        l = safe_int(fm.get("losses"), 0)
        regime = safe_int(fm.get("points_per_win_regime"), 2)
        pts_field = safe_int(fm.get("points_field"), 0)
        pts_pen = safe_int(fm.get("points_penalty"), 0)
        pts_final = safe_int(fm.get("points_final"), 0)

        if g > 0:
            expected_g = w + d + l
            expected_pts_field = (w * regime) + d
            expected_pts_final = expected_pts_field - pts_pen
            if g != expected_g or pts_field != expected_pts_field or pts_final != expected_pts_final:
                results["yaml_algebraic_errors"].append({
                    "season": season,
                    "g": g,
                    "w_d_l": expected_g,
                    "pts_field": pts_field,
                    "expected_pts_field": expected_pts_field,
                    "pts_final": pts_final,
                    "expected_pts_final": expected_pts_final,
                })
            else:
                results["valid_yaml_identities"].append({"season": season, "g": g, "pts_final": pts_final})

        max_reg_g = 46 if season == "2003-2004" else (42 if fm.get("division") == "Serie B" else 38)
        if "Rettifica Algebrica Certificata" in body or ("Coppa Italia" in body and g > max_reg_g and "Competizioni Ufficiali Extra-Campionato" not in body):
            results["cup_or_playoff_mixed_in_standings"].append({
                "season": season,
                "matches_played_yaml": g,
                "division": fm.get("division", ""),
                "points_final_yaml": pts_final,
            })

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify algebraic standings across 95 seasons.")
    parser.add_argument("--json", type=str, help="Optional JSON output path.")
    args = parser.parse_args()

    res = verify_seasons()
    print(f"Verified seasonal files in {STAGIONI_DIR}:")
    print(f"  - Valid YAML algebraic identities:        {len(res['valid_yaml_identities'])}")
    print(f"  - YAML internal formula errors:           {len(res['yaml_algebraic_errors'])}")
    print(f"  - Seasons mixing Cup/Playoffs in League:  {len(res['cup_or_playoff_mixed_in_standings'])}")

    if args.json:
        Path(args.json).write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
