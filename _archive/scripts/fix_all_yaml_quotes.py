import re
from pathlib import Path

content = Path("content")
count = 0

for p in content.rglob("*.md"):
    text = p.read_text(encoding="utf-8")
    orig = text
    
    # 1. Correggi license_type con apici singoli contenente d'autore
    text = re.sub(
        r"license_type:\s*['\"]Pubblico Dominio \(Scadenza termini d['\"]*autore\)['\"]",
        'license_type: "Pubblico Dominio (Scadenza termini d\'autore)"',
        text
    )
    
    # 2. Correggi alt_text con apici singoli contenente d'autore
    def fix_alt(m):
        val = m.group(1).replace('"', '')
        return f'alt_text: "{val}"'
        
    text = re.sub(r"alt_text:\s*'(.*?)'", fix_alt, text)
    
    if text != orig:
        p.write_text(text, encoding="utf-8")
        count += 1

print(f"Normalizzati apici in {count} file.")
