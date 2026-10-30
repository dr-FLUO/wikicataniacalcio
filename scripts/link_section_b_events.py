import os
import re

CONTENT_DIR = "content"

# Definizione delle regole di linking
# target: path relativo senza .md
# pattern: espressione regolare per trovare il testo
# repl_func: funzione che restituisce la stringa di rimpiazzo
RULES = [
    {
        "name": "Caso Scaramella",
        "target": "01-societa/vicende-legali/caso-scaramella-1955",
        "self_file": "caso-scaramella-1955.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)\b([Ii]l\s+)?Caso\s+Scaramella(?:\s+\(1955\))?\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[\101-societa/vicende-legali/caso-scaramella-1955\\|Caso Scaramella (1955)]]",
        "normal_repl": r"[[\101-societa/vicende-legali/caso-scaramella-1955|Caso Scaramella (1955)]]"
    },
    {
        "name": "Caso Martinelli",
        "target": "01-societa/vicende-legali/caso-martinelli-2003",
        "self_file": "caso-martinelli-2003.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)\b([Ii]l\s+)?Caso\s+Martinelli\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[\101-societa/vicende-legali/caso-martinelli-2003\\|Caso Martinelli]]",
        "normal_repl": r"[[\101-societa/vicende-legali/caso-martinelli-2003|Caso Martinelli]]"
    },
    {
        "name": "Caso Catania 2003",
        "target": "01-societa/vicende-legali/caso-catania-2003",
        "self_file": "caso-catania-2003.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)\b([Ii]l\s+)?[Cc]aso\s+Catania\s+(?:del\s+)?2003\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[\101-societa/vicende-legali/caso-catania-2003\\|Caso Catania (2003)]]",
        "normal_repl": r"[[\101-societa/vicende-legali/caso-catania-2003|Caso Catania (2003)]]"
    },
    {
        "name": "Spareggi di Roma 1983",
        "target": "02-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983",
        "self_file": "spareggi-roma-1983.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)\b([Gg]li\s+)?[Ss]pareggi\s+di\s+Roma(?:\s+(?:del\s+)?1983)?\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[\102-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983\\|Spareggi di Roma (1983)]]",
        "normal_repl": r"[[\102-cronistoria/partite-storiche/1982-1983/spareggi-roma-1983|Spareggi di Roma (1983)]]"
    },
    {
        "name": "Clamoroso al Cibali",
        "target": "07-media-e-comunicazione/firme-e-voci/clamoroso-al-cibali",
        "self_file": "clamoroso-al-cibali.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)(?:[«"“])?[Cc]lamoroso\s+al\s+Cibali(?:!|[»"”]|!\s*[»"”])?\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[07-media-e-comunicazione/firme-e-voci/clamoroso-al-cibali\\|«Clamoroso al Cibali!»]]",
        "normal_repl": r"[[07-media-e-comunicazione/firme-e-voci/clamoroso-al-cibali|«Clamoroso al Cibali!»]]"
    },
    {
        "name": "Caso Tacopina",
        "target": "01-societa/vicende-legali/trattativa-sigi-tacopina-2021",
        "self_file": "trattativa-sigi-tacopina-2021.md",
        "pattern": re.compile(r'(?<!\[\[)(?<!/)\b([Ii]l\s+)?[Cc]aso\s+Tacopina\b(?!\]\])', re.I),
        "pipe_table_repl": r"[[\101-societa/vicende-legali/trattativa-sigi-tacopina-2021\\|Caso Tacopina (2021)]]",
        "normal_repl": r"[[\101-societa/vicende-legali/trattativa-sigi-tacopina-2021|Caso Tacopina (2021)]]"
    }
]

total_files_modified = 0
total_replacements = 0

for root, _, files in os.walk(CONTENT_DIR):
    for f in files:
        if not f.endswith(".md"):
            continue
        filepath = os.path.join(root, f)
        
        with open(filepath, "r", encoding="utf-8-sig") as fp:
            content = fp.read()
            
        m = re.match(r'^(---\r?\n.*?\r?\n---\r?\n)(.*)$', content, re.DOTALL)
        if m:
            frontmatter = m.group(1)
            body = m.group(2)
        else:
            frontmatter = ""
            body = content
            
        lines = body.splitlines(keepends=True)
        modified_lines = []
        file_changed = False
        replacements_in_file = 0
        
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                modified_lines.append(line)
                continue
                
            if in_code_block:
                modified_lines.append(line)
                continue
                
            is_table_row = stripped.startswith("|") and stripped.endswith("|")
            
            new_line = line
            for rule in RULES:
                # Non linkare all'interno del file stesso
                if f == rule["self_file"]:
                    continue
                    
                repl = rule["pipe_table_repl"] if is_table_row else rule["normal_repl"]
                # Sostituisci solo se c'è un match
                if rule["pattern"].search(new_line):
                    # Pulizia da prefisso di capture group se c'era
                    def make_replacement(match, is_table=is_table_row, target=rule["target"], name=rule["name"]):
                        art = match.group(1) if match.lastindex and match.group(1) else ""
                        pipe = "\\|" if is_table else "|"
                        label = match.group(0).strip("«»\"“”! ")
                        return f"{art}[[{target}{pipe}{label}]]"
                    
                    subbed, count = rule["pattern"].subn(make_replacement, new_line)
                    if count > 0:
                        new_line = subbed
                        replacements_in_file += count
                        file_changed = True
                        
            modified_lines.append(new_line)
            
        if file_changed:
            new_content = frontmatter + "".join(modified_lines)
            with open(filepath, "w", encoding="utf-8") as fp:
                fp.write(new_content)
            total_files_modified += 1
            total_replacements += replacements_in_file
            print(f"[OK] {f}: {replacements_in_file} link inseriti")

print(f"\n=======================================================")
print(f"COLLEGAMENTI COMPLETATI:")
print(f"File modificati: {total_files_modified}")
print(f"Totale wikilink inseriti: {total_replacements}")
print(f"=======================================================")
