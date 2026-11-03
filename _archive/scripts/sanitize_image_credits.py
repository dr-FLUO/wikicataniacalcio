import re
from pathlib import Path
import yaml

content = Path("content")
failed_files = []

for p in sorted(content.rglob("*.md")):
    raw = p.read_text(encoding="utf-8")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", raw, re.DOTALL)
    if not m:
        continue
    fm_raw, body = m.group(1), m.group(2)
    try:
        yaml.safe_load(fm_raw)
    except Exception:
        failed_files.append((p, fm_raw, body))

print(f"Found {len(failed_files)} files to sanitize.")

for p, fm_raw, body in failed_files:
    # 1. Clean orphan continuation lines inside image_credits
    lines = fm_raw.splitlines()
    new_lines = []
    in_credits = False
    
    for line in lines:
        stripped = line.strip()
        if stripped == "image_credits:":
            in_credits = True
            new_lines.append(line)
            continue
            
        if in_credits and re.match(r"^[a-zA-Z_0-9-]+:", line) and not stripped.startswith("image_"):
            in_credits = False
            
        if in_credits:
            # If line is indented but does not contain a colon ':' and is not a list item '- '
            if not stripped.startswith("- ") and ":" not in stripped:
                # This is a stray continuation line like '    2011' or '    Catania'
                continue
            # If line has duplicate author_or_archive or license_type or year
            # We will clean keys
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    # Try parsing
    candidate_fm = "\n".join(new_lines)
    try:
        yaml.safe_load(candidate_fm)
        p.write_text(f"---\n{candidate_fm.strip()}\n---\n{body.lstrip()}", encoding="utf-8")
        print(f"[REPAIRED PASS 1] {p.name}")
        continue
    except Exception:
        pass
        
    # Pass 2: Deduplicate mapping keys inside each image_credits block
    pass2_lines = []
    in_credits = False
    current_item_keys = set()
    
    for line in new_lines:
        stripped = line.strip()
        if stripped == "image_credits:":
            in_credits = True
            pass2_lines.append(line)
            continue
        if in_credits and re.match(r"^[a-zA-Z_0-9-]+:", line):
            in_credits = False
            
        if in_credits:
            if stripped.startswith("- "):
                current_item_keys = set()
                # extract key if present
                k = stripped[2:].split(":")[0].strip()
                current_item_keys.add(k)
                pass2_lines.append(line)
                continue
            elif ":" in stripped:
                k = stripped.split(":", 1)[0].strip()
                if k in current_item_keys:
                    # Duplicate key in same item! Skip
                    continue
                current_item_keys.add(k)
                # Ensure value is cleanly quoted
                v = stripped.split(":", 1)[1].strip()
                clean_v = v.strip("'\"").replace('"', "'")
                indent = len(line) - len(line.lstrip())
                if k in ("alt_text", "license_type", "author_or_archive", "image_path"):
                    pass2_lines.append(f"{' ' * indent}{k}: \"{clean_v}\"")
                else:
                    pass2_lines.append(line)
                continue
        pass2_lines.append(line)
        
    candidate_fm2 = "\n".join(pass2_lines)
    try:
        yaml.safe_load(candidate_fm2)
        p.write_text(f"---\n{candidate_fm2.strip()}\n---\n{body.lstrip()}", encoding="utf-8")
        print(f"[REPAIRED PASS 2] {p.name}")
    except Exception as e:
        print(f"[STILL FAILING] {p.name} -> {e}")
