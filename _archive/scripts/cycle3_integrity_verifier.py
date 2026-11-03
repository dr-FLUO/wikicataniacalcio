import os
import glob
import re
import yaml

CONTENT_DIR = "content"

def run_cycle3():
    print("=== AVVIO CICLO 3: INTEGRITÀ STRUTTURALE & RAGNATELA WIKILINK ===")
    
    files = glob.glob(f"{CONTENT_DIR}/**/*.md", recursive=True)
    report = {
        "total_files": len(files),
        "valid_yaml": 0,
        "invalid_yaml": 0,
        "total_wikilinks": 0,
        "resolved_wikilinks": 0,
        "fixed_wikilinks": 0,
        "unresolved_wikilinks": set()
    }

    # Step 1: Build the global registry of all valid slugs and aliases
    slug_registry = set()
    alias_registry = set()

    for fpath in files:
        rel = os.path.relpath(fpath, CONTENT_DIR)
        calc_slug = os.path.splitext(rel)[0].replace("\\", "/").rstrip("/")
        slug_registry.add(calc_slug)
        slug_registry.add(calc_slug.lower())

        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()

        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                report["valid_yaml"] += 1
                slug = fm.get("slug")
                if slug:
                    s_clean = str(slug).strip().rstrip("/")
                    slug_registry.add(s_clean)
                    slug_registry.add(s_clean.lower())
                
                aliases = fm.get("aliases", [])
                if isinstance(aliases, list):
                    for a in aliases:
                        a_clean = str(a).strip().rstrip("/")
                        alias_registry.add(a_clean)
                        alias_registry.add(a_clean.lower())
            except Exception as e:
                report["invalid_yaml"] += 1
                print(f"YAML Syntax Error in {fpath}: {e}")

    # All known valid destinations
    all_valid_targets = slug_registry | alias_registry
    print(f"Registrati {len(slug_registry)} slug validi e {len(alias_registry)} alias di compatibilità.")

    # Step 2: Scan and repair all wikilinks in all markdown files
    wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()

        changed = False

        def fix_link(match):
            nonlocal changed
            report["total_wikilinks"] += 1
            raw_target = match.group(1).strip()
            label = match.group(2)
            
            # Clean target
            clean_target = raw_target.lstrip("/").replace("\\", "/")
            
            # If target has anchor, split it
            anchor = ""
            if "#" in clean_target:
                clean_target, anchor = clean_target.split("#", 1)
                anchor = f"#{anchor}"
            
            # Strip trailing slash from wikilink target
            stripped_target = clean_target.rstrip("/")
            norm_target = stripped_target.lower()

            if norm_target in all_valid_targets:
                report["resolved_wikilinks"] += 1
                # If it had a trailing slash in markdown, clean it
                if clean_target != stripped_target:
                    changed = True
                    report["fixed_wikilinks"] += 1
                    disp_label = label if label else stripped_target.split("/")[-1]
                    return f"[[{stripped_target}{anchor}|{disp_label}]]"
                return match.group(0)

            # Heuristics for legacy paths
            repaired_target = None
            if norm_target.startswith("tesserati/"):
                candidate = f"03-{stripped_target}"
                if candidate.lower() in all_valid_targets:
                    repaired_target = candidate
            elif norm_target.startswith("societa/"):
                candidate = f"01-{stripped_target}"
                if candidate.lower() in all_valid_targets:
                    repaired_target = candidate
            elif norm_target.startswith("stagioni/"):
                candidate = f"02-cronistoria/{stripped_target}"
                if candidate.lower() in all_valid_targets:
                    repaired_target = candidate
            elif norm_target.startswith("stadio/"):
                candidate = f"04-strutture/stadio-massimino/{stripped_target.split('/')[-1]}"
                if candidate.lower() in all_valid_targets:
                    repaired_target = candidate
            else:
                # Check basename in aliases or slugs
                base = stripped_target.split("/")[-1]
                if base.lower() in all_valid_targets:
                    repaired_target = base

            if repaired_target:
                changed = True
                report["fixed_wikilinks"] += 1
                disp_label = label if label else stripped_target.split("/")[-1]
                return f"[[{repaired_target}{anchor}|{disp_label}]]"
            else:
                report["unresolved_wikilinks"].add(raw_target)
                return match.group(0)

        new_content = wikilink_pattern.sub(fix_link, content)

        if changed:
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(new_content)

    print("=== REPORT CICLO 3 (AGGIORNATO): INTEGRITÀ STRUTTURALE & WIKILINKS ===")
    print(f"File totali analizzati: {report['total_files']}")
    print(f"File con YAML valido: {report['valid_yaml']} (Errori di sintassi: {report['invalid_yaml']})")
    print(f"Wikilink totali scansionati: {report['total_wikilinks']}")
    print(f"Wikilink verificati con successo: {report['resolved_wikilinks']}")
    print(f"Wikilink bonificati (slash finale o percorsi legacy corretti): {report['fixed_wikilinks']}")
    print(f"Link orfani residui: {len(report['unresolved_wikilinks'])}")
    if report["unresolved_wikilinks"]:
        print("Campione link non risolti:")
        for u in list(report["unresolved_wikilinks"])[:15]:
            print(f"  - {u}")

if __name__ == "__main__":
    run_cycle3()
