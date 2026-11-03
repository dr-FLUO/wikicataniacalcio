import os
import glob
import re

def update_presidenti():
    p_index = 'content/01-societa/presidenti/index.md'
    with open(p_index, 'r', encoding='utf-8') as f:
        c = f.read()

    files = sorted(glob.glob('content/01-societa/presidenti/*.md'))
    missing = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        if slug not in c:
            # get title
            with open(f, 'r', encoding='utf-8') as pf:
                txt = pf.read()
            m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', txt)
            title = m.group(1).split('—')[0].split('–')[0].strip() if m else slug.replace('-', ' ').title()
            missing.append((slug, title))

    if missing:
        append_txt = "\n\n### Altri Presidenti e Commissari Straordinari nell'Archivio\n"
        for slug, title in missing:
            append_txt += f"- [[01-societa/presidenti/{slug}|{title}]]\n"
        
        # Insert before ## Collegamenti Correlati
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', append_txt + '\n## Collegamenti Correlati')
        else:
            c += append_txt
        with open(p_index, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated presidenti index with {len(missing)} entries.")

def update_allenatori():
    a_index = 'content/03-tesserati/allenatori/index.md'
    with open(a_index, 'r', encoding='utf-8') as f:
        c = f.read()

    files = sorted(glob.glob('content/03-tesserati/allenatori/*.md'))
    missing = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        if slug not in c:
            with open(f, 'r', encoding='utf-8') as af:
                txt = af.read()
            m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', txt)
            title = m.group(1).split('—')[0].split('–')[0].strip() if m else slug.replace('-', ' ').title()
            missing.append((slug, title))

    if missing:
        append_txt = "\n\n### Archivio Monografico Completo delle Guide Tecniche\n"
        append_txt += "Elenco di tutti gli allenatori con scheda monografica dedicata:\n\n"
        # format in 3 columns or bullet list
        for slug, title in missing:
            append_txt += f"- [[03-tesserati/allenatori/{slug}|{title}]]\n"
        
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', append_txt + '\n## Collegamenti Correlati')
        else:
            c += append_txt
        with open(a_index, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated allenatori index with {len(missing)} entries.")

def update_stagioni():
    s_index = 'content/02-cronistoria/stagioni/index.md'
    with open(s_index, 'r', encoding='utf-8') as f:
        c = f.read()

    if '2026-2027' not in c:
        # add 2026-2027 entry
        entry = "\n| [[02-cronistoria/stagioni/2026-2027|2026-2027]] | Serie C (Girone C) | In corso | Stagione sportiva del centenario e consolidamento |"
        # insert into table
        if '| [[02-cronistoria/stagioni/2025-2026' in c:
            c = c.replace('| [[02-cronistoria/stagioni/2025-2026', entry + '\n| [[02-cronistoria/stagioni/2025-2026')
        elif '## Cronologia' in c:
            c += f"\n- [[02-cronistoria/stagioni/2026-2027|Stagione 2026-2027]]\n"
        with open(s_index, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated stagioni index with 2026-2027.")

def update_cronistoria():
    c_index = 'content/02-cronistoria/index.md'
    with open(c_index, 'r', encoding='utf-8') as f:
        c = f.read()

    if 'coppa-italia-serie-c' not in c:
        entry = "- [[02-cronistoria/coppa-italia-serie-c|Coppa Italia Serie C — La Storia del Trofeo e il Trionfo del 2024]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', entry + '\n## Collegamenti Correlati')
        else:
            c += '\n' + entry
        with open(c_index, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated cronistoria index with coppa-italia-serie-c.")

def update_precedenti():
    p_index = 'content/02-cronistoria/partite-storiche/precedenti/index.md'
    with open(p_index, 'r', encoding='utf-8') as f:
        c = f.read()

    files = sorted(glob.glob('content/02-cronistoria/partite-storiche/precedenti/*.md'))
    missing = []
    for f in files:
        slug = os.path.splitext(os.path.basename(f))[0]
        if slug == 'index':
            continue
        if slug not in c:
            with open(f, 'r', encoding='utf-8') as pf:
                txt = pf.read()
            m = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', txt)
            title = m.group(1).split('—')[0].split('–')[0].strip() if m else slug.replace('-', ' ').title()
            missing.append((slug, title))

    if missing:
        append_txt = "\n\n### Altri Precedenti Ufficiali Registrati\n"
        for slug, title in missing:
            append_txt += f"- [[02-cronistoria/partite-storiche/precedenti/{slug}|{title}]]\n"
        if '## Collegamenti Correlati' in c:
            c = c.replace('## Collegamenti Correlati', append_txt + '\n## Collegamenti Correlati')
        else:
            c += append_txt
        with open(p_index, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated precedenti index with {len(missing)} entries.")

update_presidenti()
update_allenatori()
update_stagioni()
update_cronistoria()
update_precedenti()
print("All target indexes synced.")
