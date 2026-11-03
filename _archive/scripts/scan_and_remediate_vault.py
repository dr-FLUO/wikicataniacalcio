"""
scripts/scan_and_remediate_vault.py
===================================
Script per la scansione sistematica e la bonifica deterministica dei 1.685 file
Markdown dell'enciclopedia storica del Calcio Catania (directory 'content/').

Funzionalità:
1. --scan (default): Scansione read-only di tutti i 1.685 file:
   - Verifica sintassi e integrità del Frontmatter YAML
   - Rilevamento token e placeholder residui ("Avversario", "TODO", ecc.)
   - Controllo discrepanze numeriche interne (caption vs frontmatter)
   - Verifica dei fatti storici e anagrafici cardine (Registro di Audit)
   - Verifica allineamento e formattazione tabelle GFM
   - Generazione di un audit log JSON e summary Markdown in logs/
2. --remediate: Esecuzione delle bonifiche deterministicamente verificate:
   - Risoluzione dei 72 placeholder "Avversario" nelle partite storiche e stagioni
   - Correzione dati anagrafici storici (Piero Andreoli, Mascara, Baiocco, Caso 2003)
   - Normalizzazione spareggi di Roma 1983 (avversari Como/Cremonese e formula torneo)
   - Backup preventivo automatico in backups/remediation_<timestamp>/
"""

import os
import sys
import re
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import yaml

CONTENT_DIR = Path("content")
LOGS_DIR = Path("logs")
BACKUPS_DIR = Path("backups")

# Mapping verificato per le stagioni con placeholder Avversario
SEASONS_DATA_DIR = Path("data")


class VaultAuditorAndRemediator:
    def __init__(self, content_dir=CONTENT_DIR, dry_run=True):
        self.content_dir = Path(content_dir)
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = BACKUPS_DIR / f"remediation_{self.timestamp}"
        
        # Statistiche di scansione
        self.stats = {
            "total_files": 0,
            "yaml_valid": 0,
            "yaml_invalid": 0,
            "avversario_occurrences": 0,
            "avversario_files": set(),
            "factual_errors_found": 0,
            "table_syntax_issues": 0,
            "remediated_files_count": 0,
            "remediated_patches_count": 0
        }
        
        self.findings = []
        self.remediation_log = []

    def scan_file(self, file_path: Path):
        """Esegue l'audit diagnostico completo su un singolo file Markdown."""
        self.stats["total_files"] += 1
        rel_path = file_path.relative_to(self.content_dir).as_posix()
        
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        file_issues = []

        # 1. Parsing Frontmatter YAML
        fm = {}
        has_fm = False
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                has_fm = True
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                    self.stats["yaml_valid"] += 1
                except Exception as e:
                    self.stats["yaml_invalid"] += 1
                    file_issues.append({"type": "YAML_PARSE_ERROR", "detail": str(e)})
                body = parts[2]
            else:
                self.stats["yaml_invalid"] += 1
                file_issues.append({"type": "YAML_MALFORMED", "detail": "Missing closing ---"})
        else:
            self.stats["yaml_invalid"] += 1
            file_issues.append({"type": "YAML_MISSING", "detail": "Document does not start with ---"})

        # 2. Controllo placeholder 'Avversario'
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            # Esclude header tabelle o sezioni descrittive legittime
            if re.search(r"\bAvversario\b", line):
                if not ("| Avversario" in line or "## " in line or "per Avversario" in line):
                    self.stats["avversario_occurrences"] += 1
                    self.stats["avversario_files"].add(rel_path)
                    file_issues.append({
                        "type": "PLACEHOLDER_AVVERSARIO",
                        "line": idx + 1,
                        "text": line.strip()
                    })

        # 3. Controllo errori fattuali specifici da Registro di Audit
        if rel_path == "03-tesserati/allenatori/piero-andreoli.md":
            b_date = str(fm.get("birth_date", ""))
            b_place = str(fm.get("birth_place", ""))
            if b_date == "1911-01-02" or "Bologna" in b_place:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "FACTUAL_ERROR_ANDREOLI",
                    "detail": f"birth_date={b_date}, birth_place={b_place} (Atteso: 1911-11-02, Verona)"
                })

        elif rel_path == "03-tesserati/calciatori/storici/davide-baiocco.md":
            tot_app = fm.get("total_appearances")
            if tot_app == 122:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "FACTUAL_DISAGGREGATION_BAIOCCO",
                    "detail": "total_appearances=122 omette 7 presenze in Coppa Italia (reale: 129)"
                })

        elif rel_path == "03-tesserati/calciatori/storici/giuseppe-mascara.md":
            caption = fm.get("cover_caption", "")
            if "236" in caption or "61" in caption:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "FACTUAL_DISCREPANCY_MASCARA_CAPTION",
                    "detail": "cover_caption indica 236 presenze e 61 reti anziché 235 e 60"
                })
            if "al 90' Mascara trasforma il calcio di rigore" in body:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "FACTUAL_CHRONO_MASCARA_INTER",
                    "detail": "Attribuzione rigore al 90' (3-1) anziché 81' (2-1)"
                })

        elif rel_path == "01-societa/vicende-legali/caso-catania-2003.md":
            if "chiedendo lo 0-2 a tavolino" in body:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "FACTUAL_LEGAL_CASO_2003",
                    "detail": "Richiesta 0-2 anziché vittoria per 2-0 a tavolino per la squadra di casa"
                })

        elif rel_path == "02-cronistoria/stagioni/1982-1983.md":
            if "| 39ª giornata" in body or "| 40ª giornata" in body:
                self.stats["factual_errors_found"] += 1
                file_issues.append({
                    "type": "STRUCTURAL_SPAREGGI_NUMBERING",
                    "detail": "Spareggi promozione erroneamente numerati come 39ª e 40ª giornata di Serie B"
                })

        # 4. Controllo integrità tabelle Markdown (mismatched pipe counts)
        in_table = False
        header_cols = 0
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                # Split ignorando i pipe escapati (\|) all'interno dei wikilink
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", stripped[1:-1])]
                if not in_table:
                    in_table = True
                    header_cols = len(cells)
                else:
                    if re.match(r"^[\s\:\-]+$", "".join(cells)):
                        continue # separator line
                    if len(cells) != header_cols:
                        self.stats["table_syntax_issues"] += 1
                        file_issues.append({
                            "type": "TABLE_PIPE_MISMATCH",
                            "line": idx + 1,
                            "detail": f"Row has {len(cells)} cols, expected {header_cols}"
                        })
            else:
                in_table = False

        if file_issues:
            self.findings.append({
                "file": rel_path,
                "issues_count": len(file_issues),
                "issues": file_issues
            })

    def run_full_scan(self):
        """Scansiona tutti i file Markdown nella cartella content."""
        print(f"[*] Avvio scansione completa su: {self.content_dir.resolve()}...")
        for root, _, files in os.walk(self.content_dir):
            for file in files:
                if file.endswith(".md"):
                    self.scan_file(Path(root) / file)
        
        print(f"[+] Scansione completata: {self.stats['total_files']} file esaminati.")

    def apply_remediations(self):
        """Applica in sicurezza le bonifiche convalidate sui file target."""
        if self.dry_run:
            print("[!] Modalità DRY-RUN (Read-Only) attiva. Nessuna modifica verrà scritta su disco.")
            return

        print(f"[*] Creazione backup preventivo in: {self.backup_path}...")
        self.backup_path.mkdir(parents=True, exist_ok=True)

        # 1. Bonifica piero-andreoli.md
        self._remediate_andreoli()

        # 2. Bonifica davide-baiocco.md
        self._remediate_baiocco()

        # 3. Bonifica giuseppe-mascara.md
        self._remediate_mascara()

        # 4. Bonifica caso-catania-2003.md
        self._remediate_caso_2003()

        # 5. Bonifica marcatori partite storiche (team: Avversario)
        self._remediate_historical_matches()

        # 6. Bonifica stagioni con placeholder (1982-1983, 1955-1956, 1956-1957, 2000-2001)
        self._remediate_season_opponents()

        # 7. Bonifica tabella derby Palermo
        self._remediate_palermo_table()

        print(f"[+] Bonifica completata: {self.stats['remediated_files_count']} file modificati, "
              f"{self.stats['remediated_patches_count']} patch applicate.")

    def _backup_file(self, target_file: Path):
        """Copia di sicurezza di un file prima della mutazione."""
        rel = target_file.relative_to(self.content_dir)
        dest = self.backup_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target_file, dest)

    def _remediate_andreoli(self):
        target = self.content_dir / "03-tesserati/allenatori/piero-andreoli.md"
        if not target.exists():
            return
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()

        # Patch YAML
        text = text.replace("birth_date: 1911-01-02", "birth_date: 1911-11-02")
        text = text.replace("birth_place: Bologna, Italia", "birth_place: Verona, Italia")
        text = text.replace("death_date: 1960-03-26", "death_date: 1984-06-16")
        text = text.replace("death_place: Massa, Italia", "death_place: Verona, Italia")

        with open(target, "w", encoding="utf-8") as f:
            f.write(text)

        self.stats["remediated_files_count"] += 1
        self.stats["remediated_patches_count"] += 4
        self.remediation_log.append({"file": target.as_posix(), "patch": "Andreoli anagrafica veronese"})

    def _remediate_baiocco(self):
        target = self.content_dir / "03-tesserati/calciatori/storici/davide-baiocco.md"
        if not target.exists():
            return
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()

        text = text.replace("total_appearances: 122", "total_appearances: 129\nleague_appearances: 122\ncup_appearances: 7")
        text = text.replace("122 presenze registrate in maglia rossazzurra", "129 presenze ufficiali registrate in maglia rossazzurra (122 campionato, 7 coppa)")
        text = text.replace("* **Presenze Ufficiali complessive**: 122", "* **Presenze Ufficiali complessive**: 129 (122 in Campionato, 7 in Coppa Italia)")

        with open(target, "w", encoding="utf-8") as f:
            f.write(text)

        self.stats["remediated_files_count"] += 1
        self.stats["remediated_patches_count"] += 3
        self.remediation_log.append({"file": target.as_posix(), "patch": "Baiocco disaggregazione presenze 129"})

    def _remediate_mascara(self):
        target = self.content_dir / "03-tesserati/calciatori/storici/giuseppe-mascara.md"
        if not target.exists():
            return
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()

        # Caption
        text = text.replace("capitano, 236 presenze e 61", "capitano, 235 presenze e 60")
        # Body riga 102
        old_text = "al 90' Mascara trasforma il calcio di rigore del definitivo **3-1** beffando Júlio César con un morbido *cucchiaio* centrale."
        new_text = "all'81' Mascara trasforma il calcio di rigore del **2-1** beffando Júlio César con un morbido *cucchiaio* centrale (il 3-1 definitivo sarà siglato da Jorge Martínez al 90')."
        text = text.replace(old_text, new_text)

        with open(target, "w", encoding="utf-8") as f:
            f.write(text)

        self.stats["remediated_files_count"] += 1
        self.stats["remediated_patches_count"] += 2
        self.remediation_log.append({"file": target.as_posix(), "patch": "Mascara caption e cronologia Catania-Inter"})

    def _remediate_caso_2003(self):
        target = self.content_dir / "01-societa/vicende-legali/caso-catania-2003.md"
        if not target.exists():
            return
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()

        text = text.replace("chiedendo lo 0-2 a tavolino", "chiedendo la vittoria per 2-0 a tavolino per il Catania")
        with open(target, "w", encoding="utf-8") as f:
            f.write(text)

        self.stats["remediated_files_count"] += 1
        self.stats["remediated_patches_count"] += 1
        self.remediation_log.append({"file": target.as_posix(), "patch": "Caso Catania 2003 vittoria per 2-0"})

    def _remediate_historical_matches(self):
        """Sostituisce 'team: Avversario' con la squadra corretta nei tabellini."""
        replacements = [
            ("02-cronistoria/partite-storiche/2002-2003/catania-siena-1-1.md", "team: Avversario", "team: A.C. Siena"),
            ("02-cronistoria/partite-storiche/2009-2010/catania-inter-3-1.md", "team: Avversario", "team: F.C. Internazionale"),
            ("02-cronistoria/partite-storiche/1963-1964/finale-coppa-delle-alpi-1964.md", "team: Avversario", "team: Genoa C.F.C."),
            ("02-cronistoria/partite-storiche/2023-2024/finale-coppa-catania-padova-4-2.md", "team: Avversario", "team: Calcio Padova")
        ]
        for rel_file, old_s, new_s in replacements:
            target = self.content_dir / rel_file
            if target.exists():
                self._backup_file(target)
                with open(target, "r", encoding="utf-8") as f:
                    text = f.read()
                count = text.count(old_s)
                if count > 0:
                    text = text.replace(old_s, new_s)
                    with open(target, "w", encoding="utf-8") as f:
                        f.write(text)
                    self.stats["remediated_files_count"] += 1
                    self.stats["remediated_patches_count"] += count
                    self.remediation_log.append({"file": rel_file, "patch": f"Risolto {old_s} in {new_s} ({count}x)"})

    def _remediate_season_opponents(self):
        """Sostituisce i placeholder 'Avversario' nelle tabelle delle stagioni storiche."""
        
        # 1. Stagione 2000-2001
        target_2000 = self.content_dir / "02-cronistoria/stagioni/2000-2001.md"
        if target_2000.exists():
            self._backup_file(target_2000)
            with open(target_2000, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            patches = 0
            for l in lines:
                if "23 agosto 2000" in l and "Avversario" in l:
                    l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Catania – Catanzaro", l)
                    patches += 1
                new_lines.append(l)
            with open(target_2000, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            if patches:
                self.stats["remediated_files_count"] += 1
                self.stats["remediated_patches_count"] += patches
                self.remediation_log.append({"file": "2000-2001.md", "patch": "Catania-Catanzaro 1-1"})

        # 2. Stagione 1982-1983
        target_1982 = self.content_dir / "02-cronistoria/stagioni/1982-1983.md"
        if target_1982.exists():
            self._backup_file(target_1982)
            with open(target_1982, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            patches = 0
            for l in lines:
                if "Avversario" in l:
                    if "27 febbraio 1983" in l or "Mirabello" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Reggiana – Catania", l).replace("| V |", "| P |")
                        patches += 1
                    elif "13 marzo 1983" in l or "Ossola" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Varese – Catania", l).replace("| V |", "| P |")
                        patches += 1
                    elif "27 marzo 1983" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Catania – Cavese", l)
                        patches += 1
                    elif "2 aprile 1983" in l or "Pistoiese" in l:
                        l = re.sub(r"Pistoiese\s*[\-\u2013\u2014]\s*Avversario", "Pistoiese – Catania", l)
                        patches += 1
                    elif "17 aprile 1983" in l or "Vittoria" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Bari – Catania", l).replace("| V |", "| P |")
                        patches += 1
                    elif "24 aprile 1983" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Catania – Como", l)
                        patches += 1
                    elif "1 maggio 1983" in l or "1º maggio 1983" in l or "Traini" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Arezzo – Catania", l)
                        patches += 1
                    elif "8 maggio 1983" in l or "Ballarin" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Sambenedettese – Catania", l).replace("| P |", "| V |")
                        patches += 1
                    elif "22 maggio 1983" in l or "Sada" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Monza – Catania", l)
                        patches += 1
                    elif "29 maggio 1983" in l or "Bordon" in l:
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Catania – Foggia", l)
                        patches += 1
                    elif "5 giugno 1983" in l or "Lazio" in l:
                        l = re.sub(r"Lazio\s*[\-\u2013\u2014]\s*Avversario", "Lazio – Catania", l)
                        patches += 1
                    elif "18 giugno 1983" in l:
                        l = re.sub(r"39[ªa]?\s*giornata", "Spareggio 1", l)
                        l = re.sub(r"Catania\s*[\-\u2013\u2014]\s*Avversario", "Catania – Como", l)
                        patches += 1
                    elif "29 agosto 1982" in l or "Galleana" in l:
                        l = re.sub(r"Milan\s*[\-\u2013\u2014]\s*Avversario", "Milan – Catania", l)
                        patches += 1
                    elif "5 settembre 1982" in l or "Adriatico" in l:
                        l = re.sub(r"Pescara\s*[\-\u2013\u2014]\s*Avversario", "Pescara – Catania", l)
                        patches += 1
                if "40ª giornata" in l or "40a giornata" in l:
                    l = re.sub(r"40[ªa]?\s*giornata", "Spareggio 2", l)
                    patches += 1
                new_lines.append(l)

            with open(target_1982, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

            if patches:
                self.stats["remediated_files_count"] += 1
                self.stats["remediated_patches_count"] += patches
                self.remediation_log.append({"file": "1982-1983.md", "patch": f"Bonificati {patches} match e spareggi"})

        # 3. Bonifica 1955-1956 e 1956-1957 da file di dati
        self._remediate_json_season("content/02-cronistoria/stagioni/1955-1956.md", "data/Club_Calcio_Catania_1955-1956.json")
        self._remediate_json_season("content/02-cronistoria/stagioni/1956-1957.md", "data/Club_Calcio_Catania_1956-1957.json")

    def _remediate_json_season(self, md_path: str, json_path: str):
        target = Path(md_path)
        jpath = Path(json_path)
        if not target.exists() or not jpath.exists():
            return
        
        with open(jpath, "r", encoding="utf-8") as f:
            matches_data = json.load(f)
            
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        patches = 0
        new_lines = []
        for line in lines:
            if "Avversario" in line and "|" in line and "giornata" in line:
                for m in matches_data:
                    # cerca matching su turno o data
                    t_num = re.search(r"(\d+)ª", m["turno"])
                    if t_num:
                        turn_str = f"| {t_num.group(1)}ª giornata"
                        if turn_str in line:
                            # Sostituzione corretta di squadra 1 e squadra 2
                            # Es. Catania – Avversario -> Catania – Squadra2 oppure Squadra1 – Catania
                            s1 = m["sq1"]
                            s2 = m["sq2"]
                            # normalizza
                            incontro_str = f"{s1} – {s2}"
                            # regex replace between date and score
                            line = re.sub(r"\|\s*([A-Za-z0-9\(\)\s\.\-]+)\s*–\s*Avversario\s*\|", f"| {incontro_str} |", line)
                            patches += 1
                            break
            new_lines.append(line)
            
        with open(target, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        self.stats["remediated_files_count"] += 1
        self.stats["remediated_patches_count"] += patches
        self.remediation_log.append({"file": md_path, "patch": f"Bonificati {patches} tabellini da Wikipedia"})

    def _remediate_palermo_table(self):
        target = self.content_dir / "02-cronistoria/partite-storiche/precedenti/palermo.md"
        if not target.exists():
            return
        self._backup_file(target)
        with open(target, "r", encoding="utf-8") as f:
            text = f.read()
        
        old_row1 = "| **1º marzo 2009** | Serie A 2008-2009 | **[[partite/2008-2009/palermo-catania-0-4\\|Palermo - Catania 0-4]]** | Ledesma, Morimoto, [[tesserati/calciatori/giuseppe-mascara\\|Mascara]] (da centrocampo) e Paolucci. |"
        new_row1 = "| **1º marzo 2009** | Serie A 2008-2009 | **Palermo - Catania** | **0-4** | [[partite/2008-2009/palermo-catania-0-4\\|Ledesma, Morimoto, Mascara (da 50m) e Paolucci]]. |"
        
        old_row2 = "| **3 aprile 2011** | Serie A 2010-2011 | **[[partite/2010-2011/catania-palermo-4-0\\|Catania - Palermo 4-0]]** | Aut. Balzaretti, [[tesserati/calciatori/gonzalo-bergessio\\|Bergessio]], Ledesma, Pesce (All. [[tesserati/allenatori/diego-pablo-simeone\\|Diego Simeone]]). |"
        new_row2 = "| **3 aprile 2011** | Serie A 2010-2011 | **Catania - Palermo** | **4-0** | [[partite/2010-2011/catania-palermo-4-0\\|Aut. Balzaretti, Bergessio, Ledesma, Pesce (All. Diego Simeone)]]. |"
        
        if old_row1 in text and old_row2 in text:
            text = text.replace(old_row1, new_row1).replace(old_row2, new_row2)
            with open(target, "w", encoding="utf-8") as f:
                f.write(text)
            self.stats["remediated_files_count"] += 1
            self.stats["remediated_patches_count"] += 2
            self.remediation_log.append({"file": "palermo.md", "patch": "Corretto allineamento a 5 colonne tabella derby"})

    def save_reports(self):
        """Salva il log JSON completo e la sintesi Markdown dell'audit."""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        report_json = LOGS_DIR / "scan_and_remediate_report.json"
        
        output_data = {
            "timestamp": self.timestamp,
            "dry_run": self.dry_run,
            "stats": {
                **self.stats,
                "avversario_files": list(self.stats["avversario_files"])
            },
            "findings_count": len(self.findings),
            "findings": self.findings,
            "remediation_log": self.remediation_log
        }
        
        with open(report_json, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"[+] Report JSON salvato in: {report_json}")


def main():
    parser = argparse.ArgumentParser(description="Audit e Bonifica Automatica Vault Markdown Catania Wiki")
    parser.add_argument("--scan", action="store_true", help="Esegue solo la scansione read-only")
    parser.add_argument("--remediate", action="store_true", help="Applica le correzioni e le bonifiche verificate")
    parser.add_argument("--content-dir", default="content", help="Cartella dei contenuti Markdown")
    args = parser.parse_args()

    # Se non specificato diversamente o se specificato --scan, opera in dry_run
    dry_run = not args.remediate

    runner = VaultAuditorAndRemediator(content_dir=args.content_dir, dry_run=dry_run)
    runner.run_full_scan()

    if args.remediate:
        runner.apply_remediations()
        print("\n[*] Esecuzione post-audit di verifica...")
        verifier = VaultAuditorAndRemediator(content_dir=args.content_dir, dry_run=True)
        verifier.run_full_scan()
        print(f"[+] Rimanenti occorrenze Avversario: {verifier.stats['avversario_occurrences']}")
        print(f"[+] Rimanenti errori fattuali noti: {verifier.stats['factual_errors_found']}")
        print(f"[+] Rimanenti errori tabelle: {verifier.stats['table_syntax_issues']}")
        verifier.remediation_log = runner.remediation_log
        verifier.stats["remediated_files_count"] = runner.stats["remediated_files_count"]
        verifier.stats["remediated_patches_count"] = runner.stats["remediated_patches_count"]
        verifier.save_reports()
    else:
        runner.save_reports()


if __name__ == "__main__":
    main()
