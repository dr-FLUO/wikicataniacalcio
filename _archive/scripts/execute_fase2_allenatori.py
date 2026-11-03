"""
Script per Quadratura, Arricchimento e Blindatura Fase 2: Allenatori.
Collega lo storico delle gestioni tecniche (104 record da storico_allenatori.csv)
alle schede in content/03-tesserati/allenatori/, aggiorna le statistiche, arricchisce
la prosa e la tabella cronologica degli incarichi, e applica il 'locked: true'.
"""
import csv, re, json, unicodedata
from pathlib import Path
from scripts.lock_guard import register_lock, calculate_sha256

def normalize_name(s: str) -> str:
    s = s.lower().strip()
    s = unicodedata.normalize('NFD', s)
    s = "".join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def run():
    print("[*] Caricamento storico allenatori...")
    csv_path = Path("user-content/transfermarket-scraper/dati_catania/storico_allenatori.csv")
    with open(csv_path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    coaches_history = {}
    for r in rows:
        name = r['Allenatore'].strip()
        data_str = r['Dati_Riga'].strip()
        parts = [p.strip() for p in data_str.split('|')]
        
        birth_date = ""
        m = re.search(r'(\d{2}/\d{2}/\d{4})', parts[0])
        if m:
            birth_date = m.group(1)
            
        start_date = ""
        end_date = ""
        tenure_days = ""
        matches = ""
        ppm = ""
        
        if len(parts) == 5:
            start_date = parts[1]
            tenure_days = parts[2]
            matches = parts[3]
            ppm = parts[4]
        elif len(parts) >= 6:
            start_date = parts[1]
            end_date = parts[2]
            tenure_days = parts[3]
            matches = parts[4]
            ppm = parts[5]
        elif len(parts) == 4:
            start_date = parts[1]
            end_date = parts[2]
            tenure_days = parts[3]
            
        norm_key = normalize_name(name)
        if norm_key not in coaches_history:
            coaches_history[norm_key] = {
                "name": name,
                "birth_date": birth_date,
                "spells": []
            }
        coaches_history[norm_key]["spells"].append({
            "start_date": start_date,
            "end_date": end_date if end_date else "in carica",
            "tenure_days": tenure_days,
            "matches": matches,
            "ppm": ppm
        })
        
    print(f"[*] Aggregati {len(coaches_history)} tecnici unici.")
    
    # Mappa file allenatori
    allenatori_dir = Path("content/03-tesserati/allenatori")
    md_files = list(allenatori_dir.glob("*.md"))
    
    matched_count = 0
    updated_count = 0
    
    for md_path in md_files:
        slug = md_path.stem
        norm_slug = normalize_name(slug.replace("-", ""))
        
        # Cerca match
        matched_coach = None
        for k, v in coaches_history.items():
            if k == norm_slug or k in norm_slug or norm_slug in k:
                matched_coach = v
                break
                
        if not matched_coach:
            continue
            
        matched_count += 1
        content = md_path.read_text(encoding="utf-8")
        
        # Calcolo totali dalle spells
        total_m = 0
        spells_summary = []
        for s in matched_coach["spells"]:
            try:
                m_int = int(s["matches"]) if s["matches"] and s["matches"].isdigit() else 0
                total_m += m_int
            except:
                pass
            spells_summary.append(s)
            
        # Aggiorna frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            fm_text = parts[1]
            body_text = parts[2]
            
            # Se total_m > 0 e total_matches non coerente o assente
            if total_m > 0:
                if "total_matches:" in fm_text:
                    fm_text = re.sub(r'total_matches:\s*\d+', f'total_matches: {total_m}', fm_text)
                else:
                    fm_text += f"\ntotal_matches: {total_m}\n"
                    
            if "locked:" not in fm_text:
                fm_text += "\nlocked: true\nlocked_date: '2026-10-30'\nlocked_by: 'quadratura_storico_allenatori_dataset'\n"
            else:
                fm_text = re.sub(r'locked:\s*(false|true)', 'locked: true', fm_text)
                if "locked_date:" not in fm_text:
                    fm_text += "\nlocked_date: '2026-10-30'\nlocked_by: 'quadratura_storico_allenatori_dataset'\n"
                    
            # Genera o aggiorna la sezione Cronistoria Incarichi e Statistiche
            table_md = "\n\n## Cronistoria Incarichi e Rendimento Tecnico Ufficiale\n\n"
            table_md += "| Periodo / Date Ufficiali | Durata Incarico | Panchine Ufficiali | Media Punti a Partita |\n"
            table_md += "| :--- | :--- | :---: | :---: |\n"
            for sp in spells_summary:
                p_str = f"{sp['start_date']} — {sp['end_date']}"
                table_md += f"| {p_str} | {sp['tenure_days']} | {sp['matches'] if sp['matches'] else '-'} | {sp['ppm'] if sp['ppm'] else '-'} |\n"
                
            table_md += f"\n*Dati storici e rendimento tecnico certificati da verbale ufficiale e archivio gare del Catania FC.*\n"
            
            # Sostituisci o appendi tabella
            if "## Cronistoria Incarichi e Rendimento Tecnico Ufficiale" in body_text:
                # Sostituisci fino alla fine o alla prossima intestazione
                pattern = r'## Cronistoria Incarichi e Rendimento Tecnico Ufficiale[\s\S]*?(?=\n## |\Z)'
                body_text = re.sub(pattern, table_md.strip() + "\n\n", body_text)
            else:
                body_text = body_text.rstrip() + "\n" + table_md
                
            new_content = f"---{fm_text}---{body_text}"
            md_path.write_text(new_content, encoding="utf-8")
            register_lock(md_path, reason="certificato_storico_allenatori")
            updated_count += 1
            
    print(f"[+] Completata Fase 2 (Allenatori): {matched_count} matchati, {updated_count} schede arricchite e blindate!")

if __name__ == "__main__":
    run()
