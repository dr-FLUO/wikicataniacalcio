import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, re
from pathlib import Path
from collections import defaultdict

ROOT = Path('content')

all_files = list(ROOT.rglob('*.md'))
corrupt_files = []
for f in all_files:
    if '\ufffd' in f.name or '' in f.name or '?' in f.name:
        corrupt_files.append(f)

print(f"File con caratteri corrotti nel nome: {len(corrupt_files)}")
for cf in corrupt_files:
    print(f"  - {cf.relative_to(ROOT)}")
