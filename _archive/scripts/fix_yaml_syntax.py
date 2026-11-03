import glob
import re
import sys
import yaml

sys.stdout.reconfigure(encoding='utf-8')

count = 0
for path in glob.glob("content/**/*.md", recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix unquoted multiline author in sources
    new_content = re.sub(
        r"- author:\s*Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo\s+Solarino",
        '- author: "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino"',
        content
    )

    # Also fix indentation if list item starts at column 0 in frontmatter
    match = re.search(r"^---\n(.*?)\n---\n", new_content, re.DOTALL)
    if match:
        fm_raw = match.group(1)
        body = new_content[len(match.group(0)):]
        lines = fm_raw.splitlines()
        fixed_lines = []
        in_list_key = None
        for line in lines:
            if re.match(r"^[a-zA-Z0-9_-]+:\s*$", line):
                in_list_key = line.split(":")[0].strip()
                fixed_lines.append(line)
            elif in_list_key in ("image_credits", "sources", "catania_periods", "tags", "club_entities", "aliases"):
                if line.startswith("- "):
                    fixed_lines.append("  " + line)
                elif line.startswith("  ") and not line.startswith("    ") and not line.strip().startswith("-"):
                    fixed_lines.append("  " + line)
                else:
                    fixed_lines.append(line)
            else:
                if not line.startswith(" ") and ":" in line:
                    in_list_key = None
                fixed_lines.append(line)
        
        try:
            parsed = yaml.safe_load("\n".join(fixed_lines))
            new_fm = yaml.dump(parsed, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{new_fm}---\n{body}"
        except Exception:
            pass

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        count += 1

print(f"Total files fixed: {count}")
