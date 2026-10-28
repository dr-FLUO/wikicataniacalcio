with open("content/01-societa/vicende-legali/caso-scaramella-1955.md", "r", encoding="utf-8") as f:
    text = f.read()

wiki_source = """sources:
- author: "Wikipedia Italia"
  title: "Voce Enciclopedica Ufficiale — Scandalo Scaramella"
  publisher: "Wikimedia Foundation"
  year: 2026
  url: "https://it.wikipedia.org/wiki/Scandalo_Scaramella"
  reference: "Dossier storico illecito sportivo 1955\""""

text = text.replace("sources:", wiki_source, 1)

old_aliases = "aliases:\n- vicende-legali/caso-scaramella-1955"
new_aliases = """aliases:
- vicende-legali/caso-scaramella-1955
- vicende-legali/scandalo-scaramella-1955
- scandalo-scaramella-1955
- scandalo-scaramella"""

text = text.replace(old_aliases, new_aliases, 1)

with open("content/01-societa/vicende-legali/caso-scaramella-1955.md", "w", encoding="utf-8") as f:
    f.write(text)

print("[OK] caso-scaramella-1955.md updated successfully")
