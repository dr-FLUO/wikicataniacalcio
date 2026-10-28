import json

with open("data/wikimedia_catania_db/commons_images.json", "r", encoding="utf-8") as f:
    imgs = json.load(f)

print(f"Total Commons images collected: {len(imgs)}")
for im in imgs[:15]:
    title = im.get("file_title")
    lic = im.get("license")
    url = im.get("url")
    author = im.get("author", "")[:30]
    print(f" - {title} [{lic} | {author}] -> {url}")
