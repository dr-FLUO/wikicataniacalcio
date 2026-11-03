import os
import re

path = "quartz/components/MagazineHome.tsx"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update all hrefs in COVER_STORIES_POOL to the new 01-08 paths
replacements = [
    ('./stagioni/1960-1961', './02-cronistoria/stagioni/1960-1961'),
    ('./stagioni/2012-2013', './02-cronistoria/stagioni/2012-2013'),
    ('./vicende-legali/caso-catania-2003', './01-societa/vicende-legali/caso-catania-2003'),
    ('./stagioni/1982-1983', './02-cronistoria/stagioni/1982-1983'),
    ('./stagioni/2005-2006', './02-cronistoria/stagioni/2005-2006'),
    ('./stagioni/2023-2024', './02-cronistoria/stagioni/2023-2024'),
    ('./vicende-legali/treni-del-gol-2015', './01-societa/vicende-legali/treni-del-gol-2015'),
    ('./stagioni/2010-2011', './02-cronistoria/stagioni/2010-2011'),
    ('./vicende-legali/caso-catania-1993-eccellenza', './01-societa/vicende-legali/caso-catania-1993-eccellenza'),
    ('./stagioni/2008-2009', './02-cronistoria/stagioni/2008-2009'),
    ('./stagioni/2009-2010', './02-cronistoria/stagioni/2009-2010'),
    ('./societa/2022-pelligra-catania-fc', './01-societa/epoche/2022-pelligra-catania-fc'),
    ('./tesserati/allenatori/carmelo-di-bella', './03-tesserati/allenatori/carmelo-di-bella'),
    ('./societa/presidenti/angelo-massimino', './01-societa/presidenti/angelo-massimino'),
    ('./tesserati/allenatori/diego-pablo-simeone', './03-tesserati/allenatori/diego-pablo-simeone'),
    ('./tesserati/calciatori/gonzalo-bergessio', './03-tesserati/calciatori/storici/gonzalo-bergessio'),
    ('./tesserati/calciatori/alejandro-gomez', './03-tesserati/calciatori/storici/alejandro-gomez'),
    ('./tesserati/allenatori/sinisa-mihajlovic', './03-tesserati/allenatori/sinisa-mihajlovic'),
    ('./societa/presidenti/ross-pelligra', './01-societa/presidenti/ross-pelligra'),
    ('./tesserati/allenatori/pasquale-marino', './03-tesserati/allenatori/pasquale-marino'),
    ('./tesserati/calciatori/francesco-lodi', './03-tesserati/calciatori/storici/francesco-lodi'),
    ('./stagioni', './02-cronistoria/stagioni/index'),
    ('./partite', './02-cronistoria/partite-storiche/index'),
    ('./societa', './01-societa/index'),
    ('./stadio', './04-strutture/index'),
    ('./tesserati', './03-tesserati/index'),
    ('./tifoseria', './06-tifoseria-e-cultura/index'),
]

for old, new in replacements:
    text = text.replace(f'"{old}"', f'"{new}"')
    text = text.replace(f"'{old}'", f"'{new}'")

# Write updated file
with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated links in MagazineHome.tsx")
