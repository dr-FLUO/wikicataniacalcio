import re
from pathlib import Path
import yaml

content = Path("content")
fixed_count = 0

for p in content.rglob("*.md"):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
    if not m:
        continue
    
    fm, body = m.group(1), m.group(2)
    orig_fm = fm
    
    # Check if there is image_credits section
    if "image_credits:" in fm:
        lines = fm.splitlines()
        new_lines = []
        i = 0
        in_credits = False
        aliases_to_add = []
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if stripped == "image_credits:":
                in_credits = True
                new_lines.append(line)
                i += 1
                continue
                
            if in_credits and re.match(r"^[a-zA-Z_]+:", line):
                in_credits = False
                
            if in_credits:
                # Catch mistakenly placed alias under image_credits
                if re.match(r"^-\s+(tesserati/|societa/|stagioni/|partite/|tifoseria/)", stripped):
                    alias_val = stripped.lstrip("- ").strip()
                    aliases_to_add.append(alias_val)
                    i += 1
                    continue
                    
                # Fix alt_text
                if stripped.startswith("alt_text:"):
                    # Extract raw text after alt_text:
                    val = stripped[len("alt_text:"):].strip()
                    # Strip leading/trailing quote marks of any kind
                    clean_val = val.strip("'\"")
                    # Replace internal double quotes with single quotes so double quoting is clean
                    clean_val = clean_val.replace('"', "'")
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(f"{' ' * indent}alt_text: \"{clean_val}\"")
                    i += 1
                    continue
                    
                # Fix license_type and skip duplicate subsequent license_type lines
                if stripped.startswith("license_type:"):
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(f"{' ' * indent}license_type: \"Pubblico Dominio (Scadenza termini d'autore)\"")
                    i += 1
                    # Skip duplicate license_type
                    while i < len(lines) and lines[i].strip().startswith("license_type:"):
                        i += 1
                    continue
                    
                # Fix author_or_archive
                if stripped.startswith("author_or_archive:"):
                    val = stripped[len("author_or_archive:"):].strip().strip("'\"")
                    clean_val = val.replace('"', "'")
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(f"{' ' * indent}author_or_archive: \"{clean_val}\"")
                    i += 1
                    continue

                # Fix image_path
                if stripped.startswith("image_path:"):
                    val = stripped[len("image_path:"):].strip().strip("'\"")
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(f"{' ' * indent}image_path: \"{val}\"")
                    i += 1
                    continue
                    
            new_lines.append(line)
            i += 1
            
        # If any aliases were moved
        if aliases_to_add:
            # Check if aliases section exists
            fm_temp = "\n".join(new_lines)
            if "aliases:" in fm_temp:
                for al in aliases_to_add:
                    if al not in fm_temp:
                        new_lines.append(f"- {al}")
            else:
                new_lines.append("aliases:")
                for al in aliases_to_add:
                    new_lines.append(f"- {al}")
                    
        fm = "\n".join(new_lines)
        
    if fm != orig_fm:
        try:
            yaml.safe_load(fm)
            p.write_text(f"---\n{fm.strip()}\n---\n{body.lstrip()}", encoding="utf-8")
            fixed_count += 1
        except Exception as e:
            print(f"Still invalid: {p} -> {e}")

print(f"Fixed {fixed_count} files successfully!")
