import re
import yaml

files = [
    ("content/02-cronistoria/stagioni/1990-1991.md", "1990-1991"),
    ("content/02-cronistoria/stagioni/1992-1993.md", "1992-1993"),
    ("content/02-cronistoria/stagioni/1999-2000.md", "1999-2000")
]

for p, yr in files:
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    idx_heading = text.find("\n# ")
    if idx_heading == -1:
        idx_heading = text.find("\n![")

    # Frontmatter is between the start and idx_heading
    block = text[:idx_heading].strip()
    # It starts with --- and should end with ---
    # Strip opening --- and closing ---
    assert block.startswith("---")
    block = block[3:].strip()
    if block.endswith("---"):
        block = block[:-3].strip()
        
    # Remove any stray inner '---'
    block = re.sub(r"\n---\n", "\n", block)
    
    # Fix broken tags and middle
    bad_pattern = re.compile(r"tags:.*?gir\.-b\s*\n\s*-\s*stagione-[0-9-]+\s*\n", re.DOTALL)
    replacement = f"""tags:
  - serie-c1
  - gir-b
  - stagione-{yr}
aliases:
  - stagioni/{yr}
"""
    block = bad_pattern.sub(replacement, block)
    
    block = re.sub(
        r"- author:\s*Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo\s+Solarino",
        '- author: "Antonio Buemi, Carlo Fontanelli, Roberto Quartarone, Alessandro Russo, Filippo Solarino"',
        block
    )

    try:
        fm = yaml.safe_load(block)
        new_fm = yaml.dump(fm, allow_unicode=True, sort_keys=False)
        body = text[idx_heading:].lstrip("\r\n")
        new_text = f"---\n{new_fm}---\n\n{body}"
        with open(p, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"Fixed {p}")
    except Exception as e:
        print(f"Error parsing {p}: {e}")
