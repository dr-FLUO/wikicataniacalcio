import json

with open('data/player_local_images.json', encoding='utf-8') as f:
    local_imgs = json.load(f)

with open('data/calciocatania_all_players.json', encoding='utf-8') as f:
    all_players = json.load(f)

targets = ['castellini', 'lunetta', 'adamonis', 'montalto', 'quaini', 'cicerelli', 'vavassori', 'fusaro', 'sorrentino', 'miltone', 'pulvirenti', 'lo monaco', 'maimone', 'finocchiaro']

for p in all_players:
    name = p.get('name', '').lower()
    for t in targets:
        if t in name:
            pid = str(p.get('id'))
            has_img = local_imgs.get(pid)
            print(f"{t.upper()}: id={pid}, name={p.get('name')}, local_image={has_img}")
