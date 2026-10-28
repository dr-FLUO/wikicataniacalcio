import os
from PIL import Image

placeholders = []
all_files = []

for root, dirs, files in os.walk('content/assets/img'):
    for f in files:
        path = os.path.join(root, f)
        all_files.append(path)
        if f.lower().endswith(('.webp', '.jpg', '.png', '.jpeg')):
            try:
                with Image.open(path) as img:
                    px = img.convert('RGB').load()
                    c1 = px[0, 0]
                    # Check for placeholder pattern: top-left (79, 17, 35) or similar known gradient
                    if c1 == (79, 17, 35):
                        placeholders.append((path, img.size))
            except Exception as e:
                print(f"Error reading {path}: {e}")

print(f"Total files in content/assets/img: {len(all_files)}")
print(f"Total placeholders found: {len(placeholders)}")
for p, sz in placeholders:
    print(f"{sz} -> {p}")
