import re
from pathlib import Path

content_dir = Path('content')
cover_images = []
inline_images = []

for md in content_dir.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    for m in re.finditer(r'cover_image:\s*["\']?([^"\']+)["\']?', text):
        cover_images.append((md.name, m.group(1).strip()))
    for m in re.finditer(r'!\[.*?\]\((.*?)\)', text):
        inline_images.append((md.name, m.group(1).strip()))

print(f"Total cover_image references: {len(cover_images)}")
print("Sample cover_image references:")
for f, img in cover_images[:10]:
    print(f"  {f}: {img}")

print(f"\nTotal inline image references: {len(inline_images)}")
print("Sample inline image references:")
for f, img in inline_images[:10]:
    print(f"  {f}: {img}")
