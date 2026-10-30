import re

with open('quartz/components/MagazineHome.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix derby barbera 2009
text = re.sub(
    r'(id:\s*"derby-barbera-2009"[\s\S]*?href:\s*)"\./02-cronistoria/stagioni/2008-2009"',
    r'\1"./02-cronistoria/partite-storiche/2008-2009/palermo-catania-0-4"',
    text
)

# Fix catania inter 1961
text = re.sub(
    r'(id:\s*"catania-inter-1961"[\s\S]*?href:\s*)"\./02-cronistoria/stagioni/1960-1961"',
    r'\1"./02-cronistoria/partite-storiche/1960-1961/catania-inter-2-0"',
    text
)

# Fix catania inter 3-1 2010
text = re.sub(
    r'(id:\s*"catania-inter-2010"[\s\S]*?href:\s*)"\./02-cronistoria/stagioni/2009-2010"',
    r'\1"./02-cronistoria/partite-storiche/2009-2010/catania-inter-3-1"',
    text
)

# Fix finale coppa padova 2024
text = re.sub(
    r'(id:\s*"coppa-italia-c-2024"[\s\S]*?href:\s*)"\./02-cronistoria/coppa-italia-serie-c"',
    r'\1"./02-cronistoria/partite-storiche/2023-2024/finale-coppa-catania-padova-4-2"',
    text
)

# Check any curve/ link remaining in MagazineHome.tsx
text = text.replace('curve/curva-sud', 'settori/curva-sud')
text = text.replace('curve/curva-nord', 'settori/curva-nord')
text = text.replace('curve/tribuna-b', 'settori/tribuna-b')
text = text.replace('tifoseria-e-cultura/curve', 'tifoseria-e-cultura/settori')

with open('quartz/components/MagazineHome.tsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("MagazineHome.tsx links corrected successfully!")
