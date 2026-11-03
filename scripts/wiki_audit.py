#!/usr/bin/env python3
"""
wiki_audit.py — Master Audit Runner for Wiki Catania Calcio (Beta 1.0).

Executes `wiki_validator`, `wiki_players`, and `wiki_seasons` to provide a unified
health check of the repository, graph links, player deduplication, and seasonal standings.
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from wiki_validator import validate_vault, CONTENT_DIR
from wiki_players import PlayerRegistry, TESSERATI_DIR
from wiki_seasons import verify_seasons, STAGIONI_DIR


def main() -> int:
    print("=" * 72)
    print("WIKI CATANIA CALCIO — FULL-STACK & DATA AUDIT RUNNER")
    print("=" * 72)

    val_res = validate_vault(CONTENT_DIR)
    print(f"[1/3] Vault & Graph Validation ({val_res['total_files']} files):")
    print(f"      - Broken [[wikilinks]]:         {len(val_res['broken_wikilinks'])}")
    print(f"      - Corrupted URLs:               {len(val_res['corrupted_urls'])}")
    print(f"      - Nested [[wikilinks]]:         {len(val_res['nested_wikilinks'])}")
    print(f"      - Missing alt attributes:       {len(val_res['missing_alt_images'])}")

    reg = PlayerRegistry(TESSERATI_DIR)
    print(f"[2/3] Player & Staff Registry ({len(set(reg.by_alias_or_slug.values()))} cards):")
    print(f"      - Transfermarkt IDs indexed:    {len(reg.by_tm_id)}")
    print(f"      - CalcioCatania IDs indexed:    {len(reg.by_cc_id)}")
    print(f"      - Total aliases registered:     {len(reg.by_alias_or_slug)}")

    seas_res = verify_seasons(STAGIONI_DIR)
    print(f"[3/3] Seasonal Standings Verification:")
    print(f"      - Valid YAML identities:        {len(seas_res['valid_yaml_identities'])}")
    print(f"      - YAML formula errors:          {len(seas_res['yaml_algebraic_errors'])}")
    print(f"      - Cup/Playoff mixed in League:  {len(seas_res['cup_or_playoff_mixed_in_standings'])}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
