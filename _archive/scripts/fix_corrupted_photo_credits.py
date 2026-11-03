import glob, re

files = glob.glob('content/03-tesserati/calciatori/**/*.md', recursive=True)
files = [f.replace('\\', '/') for f in files if not f.endswith('index.md') and not f.endswith('contributo-nazionali.md')]

fixed = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    if 'nfc-player-photo-credit' in c and 'Fonti e Bibliografia' in c:
        # Check if Fonti e Bibliografia is inside nfc-player-photo-credit
        m = re.search(r'<div class="nfc-player-photo-credit">[\s\S]*?## Fonti e Bibliografia[\s\S]*?</div>', c)
        if m:
            clean_div = '<div class="nfc-player-photo-credit">[[07-media-e-comunicazione/testate/calciocatania-com|Archivio Storico CalcioCatania.com]]</div>'
            c = c[:m.start()] + clean_div + c[m.end():]
            fixed += 1
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(c)

print(f"Fixed {fixed} files with corrupted photo credit block.")
