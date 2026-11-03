from pathlib import Path

content = Path("content")
fixed = 0

for p in content.rglob("*.md"):
    txt = p.read_text(encoding="utf-8")
    new_txt = txt
    
    # Replace single quote wrapped license_type
    new_txt = new_txt.replace("license_type: 'Pubblico Dominio (Scadenza termini d'autore)'", 'license_type: "Pubblico Dominio (Scadenza termini d\'autore)"')
    new_txt = new_txt.replace("license_type: 'Pubblico Dominio (Scadenza termini d''autore)'", 'license_type: "Pubblico Dominio (Scadenza termini d\'autore)"')
    new_txt = new_txt.replace("license_type: 'Marchio Storico ad uso descrittivo enciclopedico (Art. 21 CPI)'", 'license_type: "Marchio Storico ad uso descrittivo enciclopedico (Art. 21 CPI)"')
    new_txt = new_txt.replace("license_type: 'Creative Commons CC BY-SA 4.0'", 'license_type: "Creative Commons CC BY-SA 4.0"')
    new_txt = new_txt.replace("license_type: 'Creative Commons CC BY 4.0'", 'license_type: "Creative Commons CC BY 4.0"')
    
    # Also check alt_text single quote issues: d'autore or d'Arco
    lines = new_txt.splitlines()
    rebuilt = []
    changed_lines = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("alt_text:") and stripped.endswith("'") and stripped.count("'") > 2:
            val = stripped[len("alt_text:"):].strip().strip("'\"").replace('"', "'")
            indent = len(line) - len(line.lstrip())
            rebuilt.append(f"{' ' * indent}alt_text: \"{val}\"")
            changed_lines = True
        elif stripped.startswith("license_type:") and "d'autore" in stripped:
            indent = len(line) - len(line.lstrip())
            rebuilt.append(f"{' ' * indent}license_type: \"Pubblico Dominio (Scadenza termini d'autore)\"")
            changed_lines = True
        else:
            rebuilt.append(line)
            
    if changed_lines:
        new_txt = "\n".join(rebuilt)
        
    if new_txt != txt:
        p.write_text(new_txt, encoding="utf-8")
        fixed += 1

print(f"Fixed {fixed} files with license_type/alt_text quote syntax!")
