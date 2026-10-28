path = 'content/07-media-e-comunicazione/index.md'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace(r"d\'autore", "d'autore")
with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print("Done")
