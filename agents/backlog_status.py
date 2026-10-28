from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


def check_backlog() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    reg_path = base_dir / "data" / "entity_registry.json"
    content_dir = base_dir / "content"

    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    entities: dict[str, dict] = reg["entities"]

    compiled_by_cat: dict[str, list[str]] = defaultdict(list)
    missing_by_cat: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for slug, meta in sorted(entities.items()):
        category = slug.split("/")[0]
        md_file = content_dir / f"{slug}.md"
        if md_file.exists():
            compiled_by_cat[category].append(slug)
        else:
            missing_by_cat[category].append((slug, meta["canonical_name"]))

    total = len(entities)
    done = sum(len(v) for v in compiled_by_cat.values())
    todo = sum(len(v) for v in missing_by_cat.values())

    print("=" * 72)
    print(f" STATO DEL VAULT WIKI ROSSAZZURRA: {done}/{total} nodi del registro compilati ({todo} in coda)")
    print("=" * 72)
    for cat in sorted(set(list(compiled_by_cat.keys()) + list(missing_by_cat.keys()))):
        c_list = compiled_by_cat[cat]
        m_list = missing_by_cat[cat]
        print(f"\n[{cat.upper()}] — Compilati: {len(c_list)} | Da generare: {len(m_list)}")
        for s in c_list:
            print(f"  [OK]   content/{s}.md")
        for s, name in m_list[:5]:
            print(f"  [TODO] content/{s}.md  ({name})")
        if len(m_list) > 5:
            print(f"  ... e altri {len(m_list) - 5} nodi in '{cat}/'")


if __name__ == "__main__":
    check_backlog()
