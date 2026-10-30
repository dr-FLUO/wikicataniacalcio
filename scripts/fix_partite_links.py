import os
import re
import yaml

CONTENT_DIR = "content"
ps_dir = os.path.join(CONTENT_DIR, "02-cronistoria", "partite-storiche")

# 1. Aggiungi alias a tutti i file in partite-storiche
for root, _, files in os.walk(ps_dir):
    for f in files:
        if not f.endswith(".md"): continue
        path = os.path.join(root, f)
        rel_slug = os.path.relpath(path, CONTENT_DIR).replace(os.sep, "/")[:-3]
        
        with open(path, "r", encoding="utf-8-sig") as fp:
            content = fp.read()
            
        m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)$', content, re.DOTALL)
        if not m: continue
        fm_raw, body = m.group(1), m.group(2)
        fm = yaml.safe_load(fm_raw) or {}
        
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str): aliases = [aliases]
        
        # Genera alias standard:
        # es: rel_slug = 02-cronistoria/partite-storiche/1960-1961/catania-inter-2-0
        # alias: partite/1960-1961/catania-inter-2-0
        # alias: partite-storiche/1960-1961/catania-inter-2-0
        # alias: 1960-1961/catania-inter-2-0
        # alias: catania-inter-2-0
        sub_part = rel_slug.replace("02-cronistoria/partite-storiche/", "")
        candidate_aliases = [
            f"partite/{sub_part}",
            f"partite-storiche/{sub_part}",
            sub_part,
            f[:-3]
        ]
        
        changed = False
        for ca in candidate_aliases:
            if ca not in aliases and ca != rel_slug:
                aliases.append(ca)
                changed = True
                
        if changed:
            fm["aliases"] = aliases
            new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
            with open(path, "w", encoding="utf-8") as fp:
                fp.write(f"---\n{new_fm}---\n{body}")
            print(f"[OK] Added aliases for {f}")

# 2. Aggiorna content/02-cronistoria/partite-storiche/index.md con i link canonici corretti
index_path = os.path.join(ps_dir, "index.md")
with open(index_path, "r", encoding="utf-8-sig") as fp:
    idx_content = fp.read()

# Rimpiazza i vecchi prefissi con i percorsi canonici
replacements = [
    (r'\[\[partite/1960-1961/catania-inter-2-0', r'[[02-cronistoria/partite-storiche/1960-1961/catania-inter-2-0'),
    (r'\[\[partite/1982-1983/spareggio-catania-como-1-0', r'[[02-cronistoria/partite-storiche/1982-1983/spareggio-catania-como-1-0'),
    (r'\[\[partite/1982-1983/spareggio-catania-cremonese-0-0', r'[[02-cronistoria/partite-storiche/1982-1983/spareggio-catania-cremonese-0-0'),
    (r'\[\[partite/2002-2003/catania-siena-1-1', r'[[02-cronistoria/partite-storiche/2002-2003/catania-siena-1-1'),
    (r'\[\[partite/2005-2006/catania-albinoleffe-2-1', r'[[02-cronistoria/partite-storiche/2005-2006/catania-albinoleffe-2-1'),
    (r'\[\[partite/2008-2009/palermo-catania-0-4', r'[[02-cronistoria/partite-storiche/2008-2009/palermo-catania-0-4'),
    (r'\[\[partite/2009-2010/catania-inter-3-1', r'[[02-cronistoria/partite-storiche/2009-2010/catania-inter-3-1'),
    (r'\[\[partite/2010-2011/catania-palermo-4-0', r'[[02-cronistoria/partite-storiche/2010-2011/catania-palermo-4-0'),
    (r'\[\[partite/2023-2024/padova-catania-2-1', r'[[02-cronistoria/partite-storiche/2023-2024/padova-catania-2-1'),
    (r'\[\[partite/2023-2024/finale-coppa-catania-padova-4-2', r'[[02-cronistoria/partite-storiche/2023-2024/finale-coppa-catania-padova-4-2'),
    (r'\[\[partite/precedenti/palermo', r'[[02-cronistoria/partite-storiche/precedenti/palermo'),
    (r'\[\[partite/precedenti/inter', r'[[02-cronistoria/partite-storiche/precedenti/inter'),
    (r'\[\[partite/precedenti/salernitana', r'[[02-cronistoria/partite-storiche/precedenti/salernitana'),
    (r'\[\[partite/precedenti/casarano', r'[[02-cronistoria/partite-storiche/precedenti/casarano'),
    (r'\[\[partite/precedenti/atalanta-u23', r'[[02-cronistoria/partite-storiche/precedenti/atalanta-u23'),
    (r'\[\[stagioni/([0-9]{4}-[0-9]{4})', r'[[02-cronistoria/stagioni/\1'),
    (r'\[\[tesserati/allenatori/([a-z-]+)', r'[[03-tesserati/allenatori/\1'),
    (r'\[\[tesserati/calciatori/giuseppe-mascara', r'[[03-tesserati/calciatori/storici/giuseppe-mascara'),
    (r'\[\[tesserati/calciatori/gonzalo-bergessio', r'[[03-tesserati/calciatori/archivio/g-l/gonzalo-bergessio'),
    (r'\[\[tifoseria/eventi/esodo-roma-1983', r'[[06-tifoseria-e-cultura/eventi-e-giustizia/esodo-roma-1983'),
    (r'\[\[vicende-legali/caso-catania-2003', r'[[01-societa/vicende-legali/caso-catania-2003'),
]

for pat, repl in replacements:
    idx_content = re.sub(pat, repl, idx_content)

with open(index_path, "w", encoding="utf-8") as fp:
    fp.write(idx_content)

print("[OK] Updated partite-storiche/index.md with verified canonical links")
