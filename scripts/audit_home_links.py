import re
import os

with open('quartz/components/MagazineHome.tsx', encoding='utf-8') as f:
    text = f.read()

hrefs = re.findall(r'href:\s*["\']([^"\']+)["\']', text)
hrefs += re.findall(r'<a\s+href=["\']([^"\'#]+)["\']', text)

broken = []
for h in hrefs:
    if h.startswith('http'):
        continue
    clean = h.lstrip('./').rstrip('/')
    c1 = os.path.join('content', clean + '.md')
    c2 = os.path.join('content', clean, 'index.md')
    c3 = os.path.join('content', clean)
    if not (os.path.exists(c1) or os.path.exists(c2) or os.path.exists(c3)):
        broken.append(h)

print(f"Total checked: {len(hrefs)}")
print(f"Broken unique: {len(set(broken))}")
for b in sorted(set(broken)):
    print(" ->", b)
