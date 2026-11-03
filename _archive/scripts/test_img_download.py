import urllib.request
import urllib.parse
from pathlib import Path

target = Path("data/wikimedia_catania_db/images/test")
target.mkdir(parents=True, exist_ok=True)

test_url = "https://upload.wikimedia.org/wikipedia/commons/8/8f/1935-03-31_Viareggio_Catania_1-0.jpg"
req = urllib.request.Request(test_url, headers={"User-Agent": "WikiCalcioCataniaBot/1.0 (info@wikicalciocatania.org; Image Harvester)"})

with urllib.request.urlopen(req) as resp:
    data = resp.read()

out_file = target / "1935-03-31_Viareggio_Catania_1-0.jpg"
out_file.write_bytes(data)
print(f"Downloaded successfully: {out_file.name} ({len(data)} bytes)")
