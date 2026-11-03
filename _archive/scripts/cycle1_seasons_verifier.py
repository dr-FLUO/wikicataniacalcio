import os
import re
import json
import yaml

SEASONS_DIR = "content/02-cronistoria/stagioni"
WIKI_SEASONS_DIR = "data/wikimedia_catania_db/seasons"

def clean_wiki_markup(text):
    if not text:
        return ""
    # Remove templates like {{Bandiera|...}}
    text = re.sub(r'\{\{.*?\}\}', '', text)
    # Remove html tags like <br />
    text = re.sub(r'<.*?>', ' ', text)
    # Clean wikilinks [[Target|Label]] -> Label or [[Target]] -> Target
    def replace_wikilink(m):
        content = m.group(1)
        if '|' in content:
            return content.split('|')[1].strip()
        return content.strip()
    text = re.sub(r'\[\[(.*?)\]\]', replace_wikilink, text)
    return ' '.join(text.split()).strip()

def extract_people_from_wikitext(text):
    if not text:
        return []
    # Find all [[Target|Label]] or [[Target]]
    results = []
    # Match patterns like [[Name (disambig)|Name]] or [[Name]]
    links = re.findall(r'\[\[(.*?)\]\]', text)
    for link in links:
        if '|' in link:
            target, label = link.split('|', 1)
        else:
            target, label = link, link
        # Filter out flags, categories, division links
        if any(skip in target.lower() for skip in ['bandiera', 'categoria', 'divisione', 'serie', 'campionato', 'coppa']):
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')
        results.append((slug, label.strip()))
    return results

def slugify(text):
    text = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return text

def audit_and_fix_seasons():
    report = {
        "total_seasons": 0,
        "coaches_fixed": 0,
        "math_checked": 0,
        "math_discrepancies": [],
        "links_fixed": 0
    }

    season_files = sorted([f for f in os.listdir(SEASONS_DIR) if f.endswith(".md") and f != "index.md"])
    report["total_seasons"] = len(season_files)

    for sf in season_files:
        season_label = sf.replace(".md", "")
        filepath = os.path.join(SEASONS_DIR, sf)
        wiki_json_path = os.path.join(WIKI_SEASONS_DIR, f"{season_label}.json")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm_text = parts[1]
        body = parts[2]
        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"Error parsing YAML in {sf}: {e}")
            continue

        changed = False

        # 1. Check and fix coach_refs
        # Check if wiki json exists
        wiki_data = None
        if os.path.exists(wiki_json_path):
            try:
                with open(wiki_json_path, "r", encoding="utf-8") as wf:
                    wiki_data = json.load(wf)
            except Exception:
                pass

        # Check existing coach_refs
        current_coaches = fm.get("coach_refs", [])
        if not isinstance(current_coaches, list):
            current_coaches = [current_coaches] if current_coaches else []

        fixed_coaches = []
        for cr in current_coaches:
            cr_str = str(cr)
            # Check for bad concatenation like "poi-dal-" or "e-poi"
            if any(bad in cr_str.lower() for bad in ["poi-dal", "poi dal", "subentrato", "<br"]):
                # Extract coaches from wiki data if available, else clean the string
                if wiki_data and "infobox" in wiki_data and ("allenatore1" in wiki_data["infobox"] or "allenatore" in wiki_data["infobox"]):
                    raw_all = wiki_data["infobox"].get("allenatore1") or wiki_data["infobox"].get("allenatore", "")
                    all_people = extract_people_from_wikitext(raw_all)
                    if all_people:
                        for c_slug, c_name in all_people:
                            coach_link = f"[[03-tesserati/allenatori/{c_slug}|{c_name}]]"
                            if coach_link not in fixed_coaches:
                                fixed_coaches.append(coach_link)
                                report["coaches_fixed"] += 1
                        continue
                # Fallback: clean the string
                clean_name = clean_wiki_markup(cr_str)
                clean_slug = slugify(clean_name)
                fixed_coaches.append(f"[[03-tesserati/allenatori/{clean_slug}|{clean_name}]]")
                report["coaches_fixed"] += 1
            else:
                # Ensure path is updated to 03-tesserati/allenatori/
                clean_cr = re.sub(r'\[\[(?:tesserati/allenatori/|allenatori/)?([^|\]]+)(\|[^\]]+)?\]\]',
                                  lambda m: f"[[03-tesserati/allenatori/{slugify(m.group(1).split('/')[-1])}{m.group(2) if m.group(2) else '|' + m.group(1)}]]",
                                  cr_str)
                fixed_coaches.append(clean_cr)

        if fixed_coaches != current_coaches:
            fm["coach_refs"] = fixed_coaches
            changed = True

        # 2. Fix prev_season and next_season
        if "prev_season" in fm and fm["prev_season"]:
            ps = str(fm["prev_season"])
            # standardize to 02-cronistoria/stagioni/YYYY-YYYY
            m = re.search(r'(\d{4}-\d{4})', ps)
            if m:
                target_ps = f"[[02-cronistoria/stagioni/{m.group(1)}|{m.group(1)}]]"
                if ps != target_ps:
                    fm["prev_season"] = target_ps
                    changed = True

        if "next_season" in fm and fm["next_season"]:
            ns = str(fm["next_season"])
            m = re.search(r'(\d{4}-\d{4})', ns)
            if m:
                target_ns = f"[[02-cronistoria/stagioni/{m.group(1)}|{m.group(1)}]]"
                if ns != target_ns:
                    fm["next_season"] = target_ns
                    changed = True

        # 3. Check and fix president_ref
        if "president_ref" in fm and fm["president_ref"]:
            pres = str(fm["president_ref"])
            clean_pres = re.sub(r'\[\[(?:societa/presidenti/|presidenti/)?([^|\]]+)(\|[^\]]+)?\]\]',
                                lambda m: f"[[01-societa/presidenti/{slugify(m.group(1).split('/')[-1])}{m.group(2) if m.group(2) else '|' + m.group(1)}]]",
                                pres)
            if clean_pres != pres:
                fm["president_ref"] = clean_pres
                changed = True

        # 4. Check Algebraic Math
        matches = fm.get("matches_played", 0)
        wins = fm.get("wins", 0)
        draws = fm.get("draws", 0)
        losses = fm.get("losses", 0)
        gf = fm.get("goals_for", 0)
        ga = fm.get("goals_against", 0)
        pts = fm.get("points_final", 0)
        regime = fm.get("points_per_win_regime", 2 if int(season_label[:4]) < 1994 else 3)
        pen = fm.get("points_penalty", 0)

        report["math_checked"] += 1
        calc_matches = wins + draws + losses
        if matches > 0 and calc_matches > 0 and matches != calc_matches:
            report["math_discrepancies"].append({
                "season": season_label,
                "recorded_matches": matches,
                "sum_wdl": calc_matches,
                "details": f"W:{wins} D:{draws} L:{losses}"
            })

        # Save back if changed
        if changed:
            report["links_fixed"] += 1
            # Dump YAML
            new_fm_str = yaml.dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
            new_content = f"---\n{new_fm_str}---\n{body}"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

    print("=== REPORT CICLO 1: CRONISTORIA & STAGIONI ===")
    print(f"Stagioni totali analizzate: {report['total_seasons']}")
    print(f"Allenatori bonificati/separati: {report['coaches_fixed']}")
    print(f"File con collegamenti/metadati aggiornati: {report['links_fixed']}")
    print(f"Quadratura matematica verificata su: {report['math_checked']} stagioni")
    print(f"Discrepanze matematiche rilevate: {len(report['math_discrepancies'])}")
    if report["math_discrepancies"]:
        for d in report["math_discrepancies"][:10]:
            print(f"  - {d['season']}: partite={d['recorded_matches']} vs W+D+L={d['sum_wdl']} ({d['details']})")

if __name__ == "__main__":
    audit_and_fix_seasons()
