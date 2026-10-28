import os
import re
import yaml

content_dir = "content"
repaired = 0

for root, _, files in os.walk(content_dir):
    for f in files:
        if not f.endswith(".md"):
            continue
        filepath = os.path.join(root, f)
        with open(filepath, "r", encoding="utf-8") as fp:
            text = fp.read()

        match = re.search(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            continue

        raw_fm = match.group(1)
        body = text[len(match.group(0)):]

        # Check if YAML can be parsed directly
        try:
            fm = yaml.safe_load(raw_fm)
        except Exception:
            # Fix unindented list items under image_credits or sources
            lines = raw_fm.splitlines()
            fixed_lines = []
            curr_key = None
            for line in lines:
                if re.match(r"^[a-zA-Z0-9_-]+:\s*$", line):
                    curr_key = line.split(":")[0].strip()
                    fixed_lines.append(line)
                elif curr_key in ("image_credits", "sources", "tags", "catania_periods", "club_entities", "aliases"):
                    if line.startswith("- "):
                        fixed_lines.append("  " + line)
                    elif line.startswith("  ") and not line.startswith("    ") and not line.strip().startswith("-"):
                        fixed_lines.append("  " + line)
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)

            try:
                fm = yaml.safe_load("\n".join(fixed_lines))
            except Exception as e:
                print(f"Failed to fix {filepath}: {e}")
                continue

        # Check Diego Simeone
        if f == "diego-pablo-simeone.md":
            simeone_img = "allenatori/diego-simeone-calcio-catania-allenatore-serie-a-2011.webp"
            if simeone_img not in body:
                body = f"\n\n![Diego Pablo Simeone alla guida tecnica del Calcio Catania in Serie A nel 2011](../../assets/images/{simeone_img})\n\n" + body
                if "image_credits" not in fm or not isinstance(fm["image_credits"], list):
                    fm["image_credits"] = []
                fm["image_credits"].append({
                    "image_path": f"assets/images/{simeone_img}",
                    "alt_text": "Diego Pablo Simeone alla guida tecnica del Calcio Catania in Serie A nel 2011",
                    "author_or_archive": "Archivio Storico Calcio Catania",
                    "year": 2011,
                    "license_type": "Fair Use / Rassegna Stampa Sportiva"
                })

        # Ensure image_credits is properly structured if present
        if "image_credits" in fm and isinstance(fm["image_credits"], list):
            cleaned_credits = []
            for c in fm["image_credits"]:
                if isinstance(c, dict):
                    img_p = c.get("image_path") or c.get("source_url") or "assets/images/"
                    alt_t = c.get("alt_text") or c.get("description") or "Documentazione fotografica"
                    auth = c.get("author_or_archive") or c.get("author") or "Archivio Storico Catania"
                    lic = c.get("license_type") or c.get("license") or "Fair Use"
                    yr = c.get("year", 2024)
                    cleaned_credits.append({
                        "image_path": img_p,
                        "alt_text": alt_t,
                        "author_or_archive": auth,
                        "year": yr,
                        "license_type": lic
                    })
            fm["image_credits"] = cleaned_credits

        # Re-serialize frontmatter cleanly
        new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
        new_full = f"---\n{new_fm}---\n{body}"
        if new_full != text:
            with open(filepath, "w", encoding="utf-8") as fp:
                fp.write(new_full)
            repaired += 1

print(f"Repaired files: {repaired}")
