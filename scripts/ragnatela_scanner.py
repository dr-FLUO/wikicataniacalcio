import os
import re
import json
import argparse
from collections import defaultdict
import yaml

CONTENT_DIR = "content"
CANONICAL_ENTITIES_PATH = "data/canonical_entities.json"
BACKLOG_OUTPUT_PATH = "backlog_priorita.json"

WIKILINK_RE = re.compile(r"\[\[([^\]\\|]+)(?:\\?\|([^\]]+))?\]\]")

def load_canonical_entities():
    if os.path.exists(CANONICAL_ENTITIES_PATH):
        try:
            with open(CANONICAL_ENTITIES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def scan_vault():
    vault_files = {} # slug -> filepath
    all_md_files = []
    
    for root, _, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, CONTENT_DIR).replace(os.sep, "/")
                slug = os.path.splitext(rel_path)[0]
                vault_files[slug] = full_path
                all_md_files.append((slug, full_path))

    # Read frontmatter to discover all aliases
    alias_map = {} # alias -> slug
    for slug, full_path in all_md_files:
        try:
            with open(full_path, "r", encoding="utf-8-sig") as fp:
                content = fp.read()
            match = re.search(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
            if match:
                fm = yaml.safe_load(match.group(1))
                if isinstance(fm, dict):
                    aliases = fm.get("aliases", [])
                    if isinstance(aliases, list):
                        for a in aliases:
                            if isinstance(a, str):
                                clean_a = a.strip().lstrip("/").replace(".md", "")
                                alias_map[clean_a] = slug
                                vault_files[clean_a] = full_path
        except Exception:
            pass
                
    outgoing_links = defaultdict(set) # slug -> set of target slugs
    incoming_links = defaultdict(set) # slug -> set of source slugs
    red_links = defaultdict(list)     # target slug -> list of (source slug, line_num)
    table_pipe_errors = []            # list of (file, line_num, line)
    
    for slug, full_path in all_md_files:
        with open(full_path, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
            
        in_frontmatter = False
        body_lines = []
        
        for idx, line in enumerate(lines):
            if idx == 0 and line.strip() == "---":
                in_frontmatter = True
                continue
            if in_frontmatter:
                if line.strip() == "---":
                    in_frontmatter = False
                continue
            else:
                body_lines.append((idx + 1, line))
                
        # Scan body lines for wikilinks & GFM table pipes
        for line_num, line in body_lines:
            stripped = line.strip()
            
            # Check GFM table pipe unescaped
            if stripped.startswith("|") and stripped.endswith("|"):
                unescaped = re.findall(r"\[\[[^\]]*(?<!\\)\|[^\]]*\]\]", stripped)
                if unescaped:
                    table_pipe_errors.append((full_path, line_num, stripped, unescaped))
                    
            # Find wikilinks
            for match in WIKILINK_RE.finditer(line):
                target = match.group(1).strip()
                # Clean leading slash, trailing backslash, or relative prefix
                target_clean = target.rstrip("\\").lstrip("/").replace(".md", "")
                
                # Check anchor
                if "#" in target_clean:
                    target_clean = target_clean.split("#")[0]
                    
                if not target_clean:
                    continue
                    
                outgoing_links[slug].add(target_clean)
                
                if target_clean in vault_files:
                    resolved_slug = alias_map.get(target_clean, target_clean)
                    incoming_links[resolved_slug].add(slug)
                else:
                    # Check if target is a simple file basename
                    base_matches = [s for s in vault_files if s.endswith("/" + target_clean) or s == target_clean]
                    if base_matches:
                        resolved_slug = alias_map.get(base_matches[0], base_matches[0])
                        incoming_links[resolved_slug].add(slug)
                    else:
                        red_links[target_clean].append((slug, line_num))
                        
    return vault_files, outgoing_links, incoming_links, red_links, table_pipe_errors

def fix_table_pipes():
    fixed = 0
    for root, _, files in os.walk(CONTENT_DIR):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                with open(full_path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    
                lines = content.splitlines()
                modified = False
                new_lines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith("|") and stripped.endswith("|"):
                        new_line = re.sub(r"\[\[([^\]|]+)(?<!\\)\|([^\]]+)\]\]", r"[[\1\\|\2]]", line)
                        if new_line != line:
                            modified = True
                            line = new_line
                    new_lines.append(line)
                    
                if modified:
                    with open(full_path, "w", encoding="utf-8") as fp:
                        fp.write("\n".join(new_lines) + ("\n" if content.endswith("\n") else ""))
                    fixed += 1
    return fixed

def main():
    parser = argparse.ArgumentParser(description="Scanner Ragnatela per audit dei collegamenti del vault")
    parser.add_argument("--top", type=int, default=50, help="Numero di entita prioritarie nel backlog")
    parser.add_argument("--fix-pipes", action="store_true", help="Corregge automaticamente i pipe non sottoposti a escape nelle tabelle")
    args = parser.parse_args()
    
    if args.fix_pipes:
        fixed = fix_table_pipes()
        print(f"[OK] Corretti i pipe non sottoposti a escape in {fixed} file.")
        
    vault_files, outgoing_links, incoming_links, red_links, table_pipe_errors = scan_vault()
    
    canonical_entities = load_canonical_entities()
    
    # Priority score for red links: frequency * entity priority
    scored_red_links = []
    for target, occurrences in red_links.items():
        freq = len(occurrences)
        # Determine category / weight from target slug or canonical registry
        weight = 1.0
        if target in canonical_entities:
            weight = 2.5
        elif "societa/" in target or "stagioni/" in target:
            weight = 2.0
        elif "tesserati/" in target or "calciatori/" in target or "allenatori/" in target:
            weight = 1.5
        elif "partite/" in target:
            weight = 1.2
            
        priority_score = round(freq * weight, 2)
        sources = list(set([src for src, _ in occurrences]))
        
        scored_red_links.append({
            "target_slug": target,
            "priority_score": priority_score,
            "incoming_references_count": freq,
            "weight_multiplier": weight,
            "source_pages": sources[:10],
            "total_referencing_pages": len(sources)
        })
        
    scored_red_links.sort(key=lambda x: (x["priority_score"], x["incoming_references_count"]), reverse=True)
    top_backlog = scored_red_links[:args.top]
    
    backlog_data = {
        "metadata": {
            "total_vault_files": len(vault_files),
            "total_unique_red_links": len(red_links),
            "table_pipe_errors_count": len(table_pipe_errors),
            "top_requested": args.top
        },
        "prioritized_backlog": top_backlog
    }
    
    with open(BACKLOG_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(backlog_data, f, indent=2, ensure_ascii=False)
        
    print("=======================================================")
    print("   RAGNATELA SCANNER REPORT - WIKI CALCIO CATANIA     ")
    print("=======================================================")
    print(f"File Markdown totali nel vault: {len(vault_files)}")
    print(f"Collegamenti rossi unici (pagine mancanti): {len(red_links)}")
    print(f"Errori di pipe non sottoposti a escape nelle tabelle: {len(table_pipe_errors)}")
    print()
    print(f"[OK] Backlog prioritario generato con successo: {BACKLOG_OUTPUT_PATH}")
    if top_backlog:
        print(f"  - Top 5 pagine mancanti pi referenziate:")
        for item in top_backlog[:5]:
            print(f"    * [[{item['target_slug']}]] (citato {item['incoming_references_count']} volte)")
    else:
        print("  - Zero collegamenti rossi!")
        
    if table_pipe_errors:
        print()
        print(f"[ATTENZIONE] Rilevati {len(table_pipe_errors)} errori di pipe nelle tabelle. Esegui con --fix-pipes per risolverli.")
    else:
        print()
        print("[OK] Nessun errore di pipe non sottoposto a escape nelle tabelle.")

if __name__ == "__main__":
    main()
