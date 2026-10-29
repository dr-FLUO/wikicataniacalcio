import json

with open('data_unlinked_entities.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Blacklist words covering template headers and metadata labels
blacklist = {
    'scheda', 'presenze', 'profilo', 'parametro', 'creative', 'wikimedia',
    'licenza', 'dettaglio', 'voci', 'maglia', 'stadio', 'carriera', 'wikipedia',
    'archivio', 'pubblico', 'federale', 'collegamenti', 'ruolo', 'nazionalit',
    'luogo', 'club', 'riferimento', 'dossier', 'approfondimento', 'sezione',
    'quadratura', 'fonte', 'fonti', 'certificazione', 'protocollo', 'contesto',
    'risultati', 'rosa', 'calciomercato', 'organigramma', 'cronaca', 'campionato',
    'federazione', 'lega', 'serie', 'coppa', 'tutto', 'geo', 'gazzetta', 'corriere',
    'tuttosport', 'sicilia', 'almanacco', 'note', 'sintesi', 'verifica', 'ragione',
    'marcatori', 'coppe', 'classifica', 'staff', 'conduzione', 'denominazione',
    'gestione', 'competizioni', 'verdetto', 'annuario', 'impianto', 'partita',
    'giornata', 'andata', 'ritorno', 'minuto', 'rigore', 'autorete', 'tempo',
    'reti', 'gol', 'sconfitta', 'vittoria', 'pareggio', 'punti', 'promozione',
    'retrocessione', 'tabellino', 'formazione', 'titolari', 'panchina', 'stagione',
    'stagioni', 'calciatori', 'allenatori', 'presidenti', 'dirigenti', 'arbitro',
    'campo', 'trasferta', 'casa', 'spettatori', 'incasso', 'arbitri', 'guardalinee'
}

clean_people = []
clean_events = []
clean_venues = []

for it in items:
    name = it['name']
    words = [w.lower() for w in name.split()]
    
    # Escludi se contiene parole di blacklist
    if any(w in blacklist for w in words):
        continue
    if len(name) < 4 or len(name) > 40:
        continue
        
    low = name.lower()
    
    if any(ev in low for ev in ['caso ', 'scandalo', 'processo', 'sentenza', 'scommesse', 'radiazione', 'spareggi', 'alluvione', 'clamoroso', 'trattativa']):
        clean_events.append(it)
    elif any(v in low for v in ['palasport', 'pala', 'piazza', 'corso', 'villa', 'porto', 'aeroporto']):
        clean_venues.append(it)
    elif len(words) >= 2 and all(w[0].isupper() for w in name.split()):
        clean_people.append(it)

print(f"Persone pulite: {len(clean_people)}")
print(f"Eventi puliti: {len(clean_events)}")
print(f"Luoghi puliti: {len(clean_venues)}")

print("\n--- TOP 35 PERSONE REALI SENZA PAGINA ---")
for idx, p in enumerate(clean_people[:35], 1):
    ex = ', '.join([s.split('/')[-1] for s in p['sample_pages'][:3]])
    print(f"{idx:2d}. {p['name']:<30} | {p['distinct_pages']:3d} pag | {p['total_mentions']:3d} cit | {ex}")

print("\n--- TOP 15 EVENTI / CASI SENZA PAGINA ---")
for idx, e in enumerate(clean_events[:15], 1):
    ex = ', '.join([s.split('/')[-1] for s in e['sample_pages'][:3]])
    print(f"{idx:2d}. {e['name']:<30} | {e['distinct_pages']:3d} pag | {e['total_mentions']:3d} cit | {ex}")
