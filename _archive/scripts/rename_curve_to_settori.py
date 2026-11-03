import os
import re
import yaml

# 1. Update all files in content/06-tifoseria-e-cultura/settori
settori_dir = 'content/06-tifoseria-e-cultura/settori'
for root, dirs, files in os.walk(settori_dir):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                content = fp.read()
            
            # Replace curve with settori in slug
            content = content.replace('slug: "06-tifoseria-e-cultura/curve/', 'slug: "06-tifoseria-e-cultura/settori/')
            content = content.replace("slug: '06-tifoseria-e-cultura/curve/", "slug: '06-tifoseria-e-cultura/settori/")
            content = content.replace('slug: 06-tifoseria-e-cultura/curve/', 'slug: 06-tifoseria-e-cultura/settori/')

            # Calculate relative path from content for alias
            rel_path = os.path.relpath(p, 'content').replace('\\', '/')
            old_rel_path = rel_path.replace('06-tifoseria-e-cultura/settori', '06-tifoseria-e-cultura/curve')
            old_alias_no_ext = old_rel_path.replace('.md', '').replace('/index', '')

            # Add old alias if not present
            if content.startswith('---'):
                parts = content.split('---', 2)
                fm_raw = parts[1]
                body = parts[2]
                
                # Update title of index.md
                if f == 'index.md' and root == settori_dir:
                    fm_raw = re.sub(r'title:\s*"[^"]*"', 'title: "I Settori del Massimino: Curva Nord, Curva Sud e Tribuna B"', fm_raw)
                    body = re.sub(r'^#\s+[^\n]+', '# I Settori del Massimino: Curva Nord, Curva Sud e Tribuna B', body, count=1, flags=re.MULTILINE)

                if old_alias_no_ext not in fm_raw:
                    if 'aliases:' in fm_raw:
                        fm_raw = fm_raw.replace('aliases:', f'aliases:\n  - "{old_alias_no_ext}"\n  - "{old_rel_path.replace(".md", "")}"')
                    else:
                        fm_raw += f'\naliases:\n  - "{old_alias_no_ext}"\n  - "{old_rel_path.replace(".md", "")}"\n'

                content = f"---{fm_raw}---{body}"

            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(content)

print("Updated settori directory files.")

# 2. Update all references in content/
changed_files = 0
for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            if '06-tifoseria-e-cultura/curve' in c or 'tifoseria/curve' in c:
                new_c = c.replace('06-tifoseria-e-cultura/curve', '06-tifoseria-e-cultura/settori')
                new_c = new_c.replace('tifoseria/curve', 'tifoseria/settori')
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(new_c)
                changed_files += 1

print(f"Updated references in {changed_files} content markdown files.")

# 3. Update quartz/util/editorialFolders.ts
ed_path = 'quartz/util/editorialFolders.ts'
with open(ed_path, 'r', encoding='utf-8') as fp:
    ed = fp.read()

old_curve_block = '''  "06-tifoseria-e-cultura/curve": {
    title: "Le Curve del Massimino (Curva Nord & Curva Sud)",
    desc: "I due poli del tifo organizzato etneo: le origini, le filosofie di curva, gli striscioni storici e il legame viscerale con i quartieri di Catania.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/curve/curva-nord": {
    title: "Curva Nord: Movimento, Gruppi & Coreografie",
    desc: "La storia della Curva Nord: dalle prime sigle a Mecha Katane e A Sostegno di una Fede, con le coreografie monumentali che hanno riempito lo stadio.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/curve/curva-sud": {
    title: "Curva Sud: Falange d'Assalto & Irriducibili 1991",
    desc: "Le radici storiche del tifo popolare: la Falange fondata nel 1979 da Ciccio Famoso, gli Irriducibili e l'identità del Castello Ursino e di San Cristoforo.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },'''

new_settori_block = '''  "06-tifoseria-e-cultura/settori": {
    title: "I Settori del Massimino (Nord, Sud & Tribuna B)",
    desc: "I tre poli del tifo organizzato etneo: le origini, le filosofie di gradinata, gli striscioni storici e il legame viscerale con i quartieri di Catania.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/settori/curva-nord": {
    title: "Curva Nord: Movimento, Gruppi & Coreografie",
    desc: "La storia della Curva Nord: dalle prime sigle a Mecha Katane e A Sostegno di una Fede, con le coreografie monumentali che hanno riempito lo stadio.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/settori/curva-sud": {
    title: "Curva Sud: Falange d'Assalto & Irriducibili 1991",
    desc: "Le radici storiche del tifo popolare: la Falange fondata nel 1979 da Ciccio Famoso, gli Irriducibili e l'identità del Castello Ursino e di San Cristoforo.",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },
  "06-tifoseria-e-cultura/settori/tribuna-b": {
    title: "Tribuna B (Gradinata): MCK & Tradizione Popolare",
    desc: "Il terzo polo autonomo di gradinata: dal Gruppo Tattaresu all'A.N.R. e all'Ultras Mecha Klan Catania (MCK).",
    rubric: "RUBRICA 06 · TIFOSERIA",
  },'''

if old_curve_block in ed:
    ed = ed.replace(old_curve_block, new_settori_block)
    with open(ed_path, 'w', encoding='utf-8') as fp:
        fp.write(ed)
    print("editorialFolders.ts updated successfully!")
else:
    print("editorialFolders old_curve_block not directly matched, trying regex replace")
    ed = ed.replace('06-tifoseria-e-cultura/curve', '06-tifoseria-e-cultura/settori')
    with open(ed_path, 'w', encoding='utf-8') as fp:
        fp.write(ed)
    print("editorialFolders.ts regex-replaced.")

# 4. Update MagazineHome.tsx
mh_path = 'quartz/components/MagazineHome.tsx'
with open(mh_path, 'r', encoding='utf-8') as fp:
    mh = fp.read()
if '06-tifoseria-e-cultura/curve' in mh:
    mh = mh.replace('06-tifoseria-e-cultura/curve', '06-tifoseria-e-cultura/settori')
    with open(mh_path, 'w', encoding='utf-8') as fp:
        fp.write(mh)
    print("MagazineHome.tsx updated!")
