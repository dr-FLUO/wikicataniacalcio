import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("data/wikimedia_catania_db/eventi_storici/scandalo_scaramella.json", encoding="utf-8") as f:
    sc = json.load(f)
print("=== SCANDALO SCARAMELLA ===")
print("External links:", sc.get("external_links"))
print("Images:", sc.get("images"))
print("Wikitext length:", sc.get("wikitext_length"))
print("Wikitext:\n", sc.get("wikitext")[:1500])

with open("data/wikimedia_catania_db/eventi_storici/cinquanta_volti_per_il_cibali_hall_of_fame.json", encoding="utf-8") as f:
    cv = json.load(f)
print("\n=== CINQUANTA VOLTI ===")
print("External links:", cv.get("external_links"))
print("Images:", cv.get("images"))
print("Wikitext length:", cv.get("wikitext_length"))
print("Wikitext:\n", cv.get("wikitext")[:1500])
