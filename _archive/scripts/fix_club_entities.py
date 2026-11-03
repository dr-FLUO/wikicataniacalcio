# -*- coding: utf-8 -*-
import os
import re

seasons = sorted([f for f in os.listdir('content/02-cronistoria/stagioni') if f.endswith('.md')])
fixed_count = 0

for s in seasons:
    p = os.path.join('content/02-cronistoria/stagioni', s)
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text

    # Pattern for broken club_entity spanning one or two lines
    text = re.sub(
        r"club_entity:\s*'\[\[societa/1967-calcio-catania-spa-massimino\]\]\s*\|Calcio Catania S\.p\.A\.[^']*'",
        "club_entity: '[[societa/1967-calcio-catania-spa-massimino|Calcio Catania S.p.A. (Era Massimino)]]'",
        text,
        flags=re.DOTALL
    )
    text = re.sub(
        r"club_entity:\s*'\[\[societa/2004-era-pulvirenti\]\]\s*\|Calcio Catania S\.p\.A\.[^']*'",
        "club_entity: '[[societa/2004-era-pulvirenti|Calcio Catania S.p.A. (Era Pulvirenti)]]'",
        text,
        flags=re.DOTALL
    )
    text = re.sub(
        r"club_entity:\s*'\[\[societa/2020-sigi-e-fallimento\]\]\s*\|Calcio Catania S\.p\.A\.[^']*'",
        "club_entity: '[[societa/2020-sigi-e-fallimento|Calcio Catania S.p.A. (Gestione SIGI)]]'",
        text,
        flags=re.DOTALL
    )

    if text != orig:
        fixed_count += 1
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)

print(f'Fixed club_entity in {fixed_count} files.')
