import os
import glob
import re

def fix_storici():
    p = 'content/03-tesserati/calciatori/storici/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    files = sorted(glob.glob('content/03-tesserati/calciatori/storici/*.md'))
    missing = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        if slug not in c:
            with open(f, 'r', encoding='utf-8') as sf:
                txt = sf.read()
            m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', txt)
            title = m.group(1).split('—')[0].split('–')[0].strip() if m else slug.replace('-', ' ').title()
            missing.append((slug, title))
    if missing:
        txt_add = "\n\n### Altri Protagonisti e Calciatori Storici\n"
        for slug, title in missing:
            txt_add += f"- [[03-tesserati/calciatori/storici/{slug}|{title}]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', txt_add + '\n## Collegamenti Correlati')
        else:
            c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added {len(missing)} to storici index.")

def fix_centri_sportivi():
    p = 'content/04-strutture/centri-sportivi/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'torre-del-grifo' not in c:
        txt_add = "\n\n- [[04-strutture/centri-sportivi/torre-del-grifo|Torre del Grifo Village — Il Centro Sportivo Polifunzionale]]\n"
        c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Added torre-del-grifo to centri-sportivi index.")

def fix_eventi_giustizia():
    p = 'content/06-tifoseria-e-cultura/eventi-e-giustizia/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    files = sorted(glob.glob('content/06-tifoseria-e-cultura/eventi-e-giustizia/*.md'))
    missing = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        if slug not in c:
            with open(f, 'r', encoding='utf-8') as ef:
                txt = ef.read()
            m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', txt)
            title = m.group(1).split('—')[0].split('–')[0].strip() if m else slug.replace('-', ' ').title()
            missing.append((slug, title))
    if missing:
        txt_add = "\n\n### Altri Dossier Storici e Giudiziari\n"
        for slug, title in missing:
            txt_add += f"- [[06-tifoseria-e-cultura/eventi-e-giustizia/{slug}|{title}]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', txt_add + '\n## Collegamenti Correlati')
        else:
            c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added {len(missing)} to eventi-e-giustizia index.")

def fix_rivalita():
    p = 'content/06-tifoseria-e-cultura/relazioni/rivalita/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'derby-di-sicilia' not in c:
        txt_add = "\n\n- [[06-tifoseria-e-cultura/relazioni/rivalita/derby-di-sicilia|Il Derby di Sicilia — La Storica Rivalità con il Palermo]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', txt_add + '\n## Collegamenti Correlati')
        else:
            c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Added derby-di-sicilia to rivalita index.")

def fix_curva_nord():
    p = 'content/06-tifoseria-e-cultura/settori/curva-nord/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'festa-curva-nord-famiglie-bambini-2026' not in c:
        txt_add = "\n\n- [[06-tifoseria-e-cultura/settori/curva-nord/festa-curva-nord-famiglie-bambini-2026|Festa Curva Nord Famiglie e Bambini (2026)]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', txt_add + '\n## Collegamenti Correlati')
        else:
            c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Added festa-curva-nord to curva-nord index.")

def fix_stagione_2026():
    p = 'content/02-cronistoria/stagioni/index.md'
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if '2026-2027.md' not in c and '02-cronistoria/stagioni/2026-2027' not in c:
        txt_add = "\n- [[02-cronistoria/stagioni/2026-2027|Stagione 2026-2027 — Il Catania nel Campionato di Serie C]]\n"
        c += txt_add
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Added 2026-2027 to stagioni index.")

fix_storici()
fix_centri_sportivi()
fix_eventi_giustizia()
fix_rivalita()
fix_curva_nord()
fix_stagione_2026()
print("All remaining indexes fixed.")
