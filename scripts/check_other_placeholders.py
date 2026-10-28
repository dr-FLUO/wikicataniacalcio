import os
from PIL import Image, ImageStat

candidates = []

for root, dirs, files in os.walk('content/assets/img'):
    for f in files:
        path = os.path.join(root, f)
        if f.lower().endswith(('.webp', '.jpg', '.png', '.jpeg')):
            try:
                with Image.open(path) as img:
                    stat = ImageStat.Stat(img.convert('RGB'))
                    # standard deviation of colors in real photos is high; in smooth 2-color gradient it's low or very specific
                    # Or check unique colors:
                    w, h = img.size
                    px = img.convert('RGB').load()
                    c1 = px[0, 0]
                    # if c1 == (79, 17, 35) or low variance or specific sponsors/maglie
                    if c1 == (79, 17, 35):
                        candidates.append((path, "exact_gradient", img.size))
                    elif 'maglie-e-simboli' in path:
                        # check if sponsor or maglia is placeholder
                        pass
            except Exception as e:
                pass

print(f"Total exact gradient placeholders: {len(candidates)}")
# Let's check maglie-e-simboli files
for root, dirs, files in os.walk('content/assets/img/maglie-e-simboli'):
    for f in files:
        p = os.path.join(root, f)
        with Image.open(p) as img:
            px = img.convert('RGB').load()
            print(f"maglie: {f} -> size {img.size}, px[0,0]={px[0,0]}")
