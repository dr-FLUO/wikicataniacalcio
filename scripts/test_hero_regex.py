import re

with open('content/03-tesserati/calciatori/archivio/a-c/adamo-puccini.md', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div class="nfc-player-hero-card">[\s\S]*?</table>\s*</div>', text)
print("Matched exactly table inside hero card:", bool(m))
if m:
    print(m.group(0)[:150])
    print("...")
    print(m.group(0)[-100:])
