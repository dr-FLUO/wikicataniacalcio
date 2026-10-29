import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, re
from pathlib import Path
from collections import defaultdict

ROOT = Path('content')

files_info = []
for p in ROOT.rglob('*.md'):
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    try:
        content = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    lines = content.splitlines()
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
    words = len(body.split())
    files_info.append({
        'path': rel,
        'lines': len(lines),
        'words': words,
        'stem': p.stem,
        'parent': str(p.parent.relative_to(ROOT)).replace('\\', '/')
    })

folder_groups = defaultdict(list)
for fi in files_info:
    folder_groups[fi['parent']].append(fi)

print('=== THEMATIC FOLDERS AUDIT (NON-CALCIATORI / NON-PARTITE / NON-STAGIONI) ===')
for folder, f_list in sorted(folder_groups.items()):
    if any(folder.startswith(x) for x in ['02-cronistoria/stagioni', '02-cronistoria/partite-storiche/tabellini', '03-tesserati/calciatori/archivio']):
        continue
    print(f"\n[Folder: {folder}] ({len(f_list)} files):")
    for f in sorted(f_list, key=lambda x: x['words']):
        print(f"   {f['stem'][:35]:35} | {f['lines']:4} righe | {f['words']:5} parole | {f['path']}")
