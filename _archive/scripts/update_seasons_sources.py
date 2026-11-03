# -*- coding: utf-8 -*-
import os
import re

modern_years = range(2011, 2026)

for yr in modern_years:
    path = f'content/02-cronistoria/stagioni/{yr}-{yr+1}.md'
    if not os.path.exists(path):
        print(f'File not found: {path}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Regex replacement for YAML sources entry
    # Match any YAML entry with 'Tutto il Catania minuto per minuto' and GEO Edizioni
    yaml_pattern = re.compile(
        r'-\s*author:\s*Antonio Buemi[^\n]*\n(?:\s+Solarino[^\n]*\n)?'
        r'\s*title:\s*Tutto il Catania minuto per minuto[^\n]*\n'
        r'\s*publisher:\s*GEO Edizioni[^\n]*\n'
        r'\s*year:\s*2010\n'
        r'\s*reference:[^\n]*',
        re.MULTILINE
    )

    new_yaml = (
        '- author: Roberto Quartarone, Alessandro Russo, Filippo Solarino, Antonio Buemi, Carlo Fontanelli\n'
        '  title: Tutto il Catania minuto per minuto — Portale e Archivio Storico Online\n'
        '  publisher: tuttoilcataniaminutoperminuto.it\n'
        '  year: 2026\n'
        '  url: https://www.tuttoilcataniaminutoperminuto.it/\n'
        '  reference: Tabellini, cronache e statistiche stagionali'
    )

    text, n1 = yaml_pattern.subn(new_yaml, text)

    # Regex replacement for markdown body bibliography entry
    body_pattern = re.compile(
        r'\d+\.\s*\*\*Antonio Buemi[^\*]+\*\*,\s*\*Tutto il Catania minuto per minuto[^\*]+\*,\s*GEO Edizioni[^\n]+',
        re.MULTILINE
    )

    new_body = (
        '1. **Roberto Quartarone, Alessandro Russo, Filippo Solarino, Antonio Buemi, Carlo Fontanelli**, '
        '*Tutto il Catania minuto per minuto*, archivio e documentazione online su '
        '[tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/).'
    )

    text, n2 = body_pattern.subn(new_body, text)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f'{yr}-{yr+1}.md: YAML replaced={n1}, body replaced={n2}')
