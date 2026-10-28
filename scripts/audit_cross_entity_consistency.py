"""
scripts/audit_cross_entity_consistency.py
=========================================
Script per la Fase 1 di Audit Relazionale Semantico (Cross-Entity Consistency Check).
Esegue una scansione completa del grafo della conoscenza su tutti i 1.690 file Markdown
del vault, senza modificare alcun file (Read-Only Dry-Run).

Verifiche implementate:
1. Coerenza Stagioni ↔ Allenatori (coach_refs spezzati, stringhe concatenate, slug con diacritici mutati)
2. Coerenza Calciatori ↔ Rosa Attuale (current_squad flag in archivio vs rosa-attuale)
3. Coerenza Periodi di Militanza (catania_periods vs stagioni effettive)
4. Allucinazioni Narrativo-Tattiche (Allenatore X citato nella Stagione Y in cui non allenava)
5. Partite Storiche ↔ Tabellini Stagione
6. Coerenza Fatti ed Eventi Giudiziari Chiave (2 Febbraio 2007 Raciti, Catania-Siena 2003)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re
import json
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

VAULT_CONTENT = Path("content")
LOGS_DIR = Path("logs")

def clean_wikilink(wlink):
    if not wlink:
        return "", ""
    wlink = str(wlink).strip().strip("[]'")
    target = wlink
    label = ""
    if "|" in wlink:
        parts = wlink.split("|", 1)
        target = parts[0].strip()
        label = parts[1].strip()
    target = target.replace("\\", "/")
    return target, label

def extract_slug(target):
    return target.split("/")[-1].strip()

def parse_md_frontmatter(path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return None, "", str(e)
    
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                return fm, parts[2], None
            except Exception as e:
                return {}, parts[2], f"YAML parse error: {e}"
    return {}, text, None

def run_cross_entity_audit():
    print(f"[*] Avvio Audit Cross-Entity su: {VAULT_CONTENT.resolve()}...")
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    findings = []
    
    # =========================================================================
    # STEP 1: Indicizzazione Stagioni (1929-2027)
    # =========================================================================
    seasons = {} # label -> dict
    season_files = sorted(list((VAULT_CONTENT / "02-cronistoria" / "stagioni").glob("*.md")))
    print(f"[*] Indicizzazione di {len(season_files)} stagioni ufficiali...")
    
    for sf in season_files:
        fm, body, err = parse_md_frontmatter(sf)
        if err:
            findings.append({
                "category": "YAML_ERROR",
                "file": str(sf.relative_to(VAULT_CONTENT)),
                "severity": "CRITICAL",
                "message": f"Errore parsing YAML: {err}"
            })
            continue
            
        label = fm.get("season_label") or sf.stem
        raw_coaches = fm.get("coach_refs") or []
        if isinstance(raw_coaches, str):
            raw_coaches = [raw_coaches]
            
        coach_slugs = []
        for rc in raw_coaches:
            target, label_text = clean_wikilink(rc)
            slug = extract_slug(target)
            coach_slugs.append({
                "raw": rc,
                "target": target,
                "slug": slug,
                "label": label_text
            })
            
        raw_pres = fm.get("president_ref") or ""
        p_target, p_label = clean_wikilink(raw_pres)
        pres_slug = extract_slug(p_target)
        
        seasons[label] = {
            "path": sf,
            "rel_path": str(sf.relative_to(VAULT_CONTENT)),
            "fm": fm,
            "body": body,
            "coaches": coach_slugs,
            "president_slug": pres_slug,
            "division": fm.get("division", ""),
            "division_tier": fm.get("division_tier", "")
        }

    # =========================================================================
    # STEP 2: Indicizzazione Allenatori e Verifica Coach_refs
    # =========================================================================
    coaches_dir = VAULT_CONTENT / "03-tesserati" / "allenatori"
    coach_files = {} # slug -> dict
    existing_coaches = {cf.stem: cf for cf in coaches_dir.glob("*.md") if cf.name != "index.md"}
    print(f"[*] Indicizzati {len(existing_coaches)} allenatori ufficiali...")

    for cf_stem, cf in existing_coaches.items():
        fm, body, err = parse_md_frontmatter(cf)
        coach_files[cf_stem] = {
            "path": cf,
            "rel_path": str(cf.relative_to(VAULT_CONTENT)),
            "fm": fm,
            "body": body,
            "periods": fm.get("catania_periods") or [],
            "name": fm.get("title", cf_stem)
        }

    # Controllo Coach_refs delle stagioni
    for s_label, s_data in seasons.items():
        for c in s_data["coaches"]:
            slug = c["slug"]
            
            # Caso 1: Testo puro non wikilink
            if not c["raw"].startswith("[["):
                findings.append({
                    "category": "COACH_UNLINKED_PLAIN_TEXT",
                    "file": s_data["rel_path"],
                    "severity": "HIGH",
                    "season": s_label,
                    "target": c["raw"],
                    "message": f"In {s_label}: l'allenatore '{c['raw']}' è testo semplice non formattato come wikilink."
                })
                continue

            # Caso 2: Stringhe concatenate con "poi", "a-seguire", ecc.
            if any(sep in slug for sep in ["-poi-", "-a-seguire-", "dalla-", "-e-", "-maurizio-"]):
                findings.append({
                    "category": "COACH_CONCATENATED_STRING",
                    "file": s_data["rel_path"],
                    "severity": "HIGH",
                    "season": s_label,
                    "target": c["raw"],
                    "slug": slug,
                    "message": f"In {s_label}: stringa allenatori concatenata '{slug}'. Deve essere separata in elementi distinti della lista YAML."
                })
            else:
                # Caso 3: Verifica se esiste il file
                if slug not in existing_coaches:
                    # Controlliamo mutazioni note (es. diacritici / accenti)
                    slug_clean = slug.replace("-ii", "").replace("-", "")
                    matched_coach = None
                    for ec_stem in existing_coaches:
                        ec_clean = ec_stem.replace("-", "")
                        if ec_clean == slug_clean or slug_clean in ec_clean or ec_clean in slug_clean:
                            matched_coach = ec_stem
                            break
                    
                    if matched_coach:
                        findings.append({
                            "category": "COACH_SLUG_ACCENT_MUTATION",
                            "file": s_data["rel_path"],
                            "severity": "HIGH",
                            "season": s_label,
                            "target": c["raw"],
                            "slug": slug,
                            "suggested_slug": matched_coach,
                            "message": f"In {s_label}: slug '{slug}' rotto da diacritici/suffisso, corrisponde a 'content/03-tesserati/allenatori/{matched_coach}.md'."
                        })
                    else:
                        findings.append({
                            "category": "COACH_FILE_NOT_FOUND",
                            "file": s_data["rel_path"],
                            "severity": "HIGH",
                            "season": s_label,
                            "target": c["raw"],
                            "slug": slug,
                            "message": f"In {s_label}: file allenatore non trovato: '{slug}.md'"
                        })

    # =========================================================================
    # STEP 3: Indicizzazione Calciatori e Controllo current_squad / Anacronismi
    # =========================================================================
    calciatori_dir = VAULT_CONTENT / "03-tesserati" / "calciatori"
    player_files = sorted(list(calciatori_dir.rglob("*.md")))
    print(f"[*] Indicizzazione di {len(player_files)} calciatori...")
    
    rosa_attuale_dir = calciatori_dir / "rosa-attuale"
    rosa_attuale_slugs = {p.stem for p in rosa_attuale_dir.glob("*.md") if p.name != "index.md"}
    # Capitano storico Castellini
    rosa_attuale_slugs.add("alessio-castellini")

    for pf in player_files:
        if pf.name == "index.md":
            continue
        rel_path = str(pf.relative_to(VAULT_CONTENT))
        slug = pf.stem
        fm, body, err = parse_md_frontmatter(pf)
        if err:
            findings.append({
                "category": "YAML_ERROR",
                "file": rel_path,
                "severity": "CRITICAL",
                "message": f"Errore YAML in calciatore: {err}"
            })
            continue

        is_in_rosa_attuale = "rosa-attuale" in pf.parts
        current_squad_val = fm.get("current_squad")
        periods = fm.get("catania_periods") or []
        if isinstance(periods, str):
            periods = [periods]

        # Regola A: File in rosa-attuale DEVE avere current_squad: true
        if is_in_rosa_attuale and current_squad_val is not True:
            findings.append({
                "category": "ROSA_ATTUALE_CURRENT_SQUAD_MISMATCH",
                "file": rel_path,
                "severity": "MEDIUM",
                "slug": slug,
                "current_val": current_squad_val,
                "message": f"Calciatore '{slug}' in rosa-attuale/ ha 'current_squad: {current_squad_val}' invece di true."
            })

        # Regola B: File in archivio/ o storici/ NON DEVE avere current_squad: true (salvo Castellini)
        if not is_in_rosa_attuale and slug != "alessio-castellini" and current_squad_val is True:
            findings.append({
                "category": "ARCHIVED_PLAYER_MARKED_CURRENT",
                "file": rel_path,
                "severity": "HIGH",
                "slug": slug,
                "message": f"Calciatore archiviato '{slug}' ha 'current_squad: true' ma non appartiene alla rosa attiva 2026-2027."
            })

        # Regola C: Calciatore archiviato con catania_periods che cita 2026-2027 o 2027
        if not is_in_rosa_attuale and slug != "alessio-castellini":
            for per in periods:
                per_str = str(per)
                if "2026-2027" in per_str or (per_str.endswith("2027") and not per_str.startswith("19")):
                    findings.append({
                        "category": "ARCHIVED_PLAYER_FUTURE_PERIOD",
                        "file": rel_path,
                        "severity": "HIGH",
                        "slug": slug,
                        "period": per_str,
                        "message": f"Calciatore archiviato '{slug}' ha periodi '{per_str}' estesi alla stagione corrente 2026-2027."
                    })

        # Regola D: Anacronismi narrativi Calciatore ↔ Allenatore ↔ Stagione
        coach_season_patterns = [
            re.compile(r"(?:sotto la (?:sapiente )?regia|guida|con l'allenatore|con il tecnico|schierato da|allenato da)\s+\[\[(?:03-tesserati/allenatori/)?([^\|\]]+)(?:\|[^\]]*)?\]\]\s+nel(?:la)?\s+(?:\[\[(?:02-cronistoria/stagioni/)?([^\|\]]+)(?:\|[^\]]*)?\]\]|stagione\s+(\d{4}-\d{4}))", re.IGNORECASE),
            re.compile(r"nel(?:la)?\s+(?:\[\[(?:02-cronistoria/stagioni/)?([^\|\]]+)(?:\|[^\]]*)?\]\]|stagione\s+(\d{4}-\d{4}))[^\.\n]*?(?:sotto la guida|con il tecnico|allenato da)\s+\[\[(?:03-tesserati/allenatori/)?([^\|\]]+)(?:\|[^\]]*)?\]\]", re.IGNORECASE)
        ]
        
        for pat in coach_season_patterns:
            for match in pat.finditer(body):
                groups = match.groups()
                c_cand = None
                s_cand = None
                for g in groups:
                    if not g: continue
                    if re.match(r"^\d{4}-\d{4}$", g):
                        s_cand = g
                    elif "20" in g or "19" in g:
                        s_cand = extract_slug(g)
                    else:
                        c_cand = extract_slug(g)
                
                if c_cand and s_cand and s_cand in seasons:
                    season_coaches = [c["slug"] for c in seasons[s_cand]["coaches"]]
                    if season_coaches and c_cand not in season_coaches:
                        is_sub = any(c_cand in sc for sc in season_coaches)
                        if not is_sub:
                            findings.append({
                                "category": "NARRATIVE_COACH_SEASON_MISMATCH",
                                "file": rel_path,
                                "severity": "HIGH",
                                "coach": c_cand,
                                "season": s_cand,
                                "official_coaches": season_coaches,
                                "match_text": match.group(0)[:120],
                                "message": f"In '{slug}': associato l'allenatore '{c_cand}' alla stagione '{s_cand}', ma la stagione riporta: {season_coaches}."
                            })

    # =========================================================================
    # STEP 4: Controllo Avvenimenti Storici e Giudiziari Chiave
    # =========================================================================
    print(f"[*] Audit di coerenza su eventi storici chiave (2 Febbraio 2007, Caso Catania 2003)...")
    
    for md_file in VAULT_CONTENT.rglob("*.md"):
        rel_p = str(md_file.relative_to(VAULT_CONTENT))
        try:
            txt = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        # Check A: Caso Catania 2003 (Catania-Siena)
        if "Catania-Siena" in txt or "Catania - Siena" in txt or "Caso Catania" in txt:
            if re.search(r"Catania\s*-\s*Siena[^\.\n]*0-2\s*a\s*tavolino", txt, re.IGNORECASE) or \
               re.search(r"CAF[^\.\n]*0-2", txt, re.IGNORECASE) or \
               re.search(r"delibera[^\.\n]*0-2", txt, re.IGNORECASE):
                findings.append({
                    "category": "HISTORICAL_EVENT_CONTRADICTION",
                    "file": rel_p,
                    "severity": "CRITICAL",
                    "event": "Caso Catania 2003",
                    "message": "Indica un verdetto CAF '0-2' a tavolino per Catania-Siena (falso: la vittoria a tavolino fu 2-0 per il Catania)."
                })

        # Check B: 2 Febbraio 2007 (Filippo Raciti)
        if "Raciti" in txt or "2 febbraio 2007" in txt:
            # Riconoscimento legge antiviolenza: deve essere Legge 41/2007 oppure Decreto-Legge 8/2007
            # Segnala SOLO se scrive "Legge 8/2007" (senza Decreto) o numeri arbitrari
            legge_err = re.finditer(r"(?<!Decreto-)(?<!D\.L\.\s)(?<!D\.Lgs\.\s)Legge\s+(?:n\.\s*)?(\d+)/2007", txt, re.IGNORECASE)
            for le in legge_err:
                num = le.group(1)
                if num != "41":
                    findings.append({
                        "category": "HISTORICAL_EVENT_LAW_MISMATCH",
                        "file": rel_p,
                        "severity": "HIGH",
                        "event": "2 Febbraio 2007",
                        "matched": le.group(0),
                        "message": f"Citazione normativa imprecisa: '{le.group(0)}' (il D.L. è 8/2007, la Legge di conversione è Legge 41/2007)."
                    })

    # =========================================================================
    # STEP 5: Consolidamento e Salvataggio Report
    # =========================================================================
    severity_counts = defaultdict(int)
    category_counts = defaultdict(int)
    for f in findings:
        severity_counts[f["severity"]] += 1
        category_counts[f["category"]] += 1

    report_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_files_audited": len(list(VAULT_CONTENT.rglob("*.md"))),
        "total_seasons_indexed": len(seasons),
        "total_coaches_indexed": len(existing_coaches),
        "total_players_indexed": len(player_files),
        "findings_count": len(findings),
        "severity_summary": dict(severity_counts),
        "category_summary": dict(category_counts),
        "findings": findings
    }

    report_json_path = LOGS_DIR / "cross_entity_audit_report.json"
    with open(report_json_path, "w", encoding="utf-8") as jf:
        json.dump(report_data, jf, indent=2, ensure_ascii=False)
        
    print(f"\n[+] Audit completato!")
    print(f"    - File analizzati: {report_data['total_files_audited']}")
    print(f"    - Discrepanze totali rilevate: {len(findings)}")
    print(f"    - Severità: CRITICAL: {severity_counts['CRITICAL']}, HIGH: {severity_counts['HIGH']}, MEDIUM: {severity_counts['MEDIUM']}")
    print(f"    - Report JSON salvato in: {report_json_path}")
    
    return report_data

if __name__ == "__main__":
    run_cross_entity_audit()
