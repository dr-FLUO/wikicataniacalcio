import json
import re

with open('data_unlinked_entities.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Filtro blacklist di etichette UI, metadati e titoli di template
blacklist_words = {
    'scheda', 'presenze', 'profilo', 'parametro', 'creative commons', 'wikimedia',
    'licenza', 'dettaglio', 'voci correlate', 'maglia rossazzurra', 'stadio di casa',
    'carriera', 'wikipedia', 'archivio storico', 'pubblico dominio', 'federale',
    'collegamenti', 'ruolo tattico', 'nazionalit', 'luogo di nascita', 'club di appartenenza',
    'riferimento ufficiale', 'dossier', 'approfondimento', 'sezione', 'quadratura',
    'fonte primaria', 'fonti primarie', 'certificazione', 'protocollo', 'contesto storico',
    'risultati e tabellini', 'rosa della stagione', 'calciomercato', 'organigramma',
    'cronaca della stagione', 'campionato', 'federazione italiana giuoco', 'lega nazionale',
    'serie a', 'serie b', 'serie c', 'serie d', 'coppa italia', 'tutto il catania', 'geo edizioni',
    'la gazzetta dello sport', 'corriere dello sport', 'tuttosport', 'la sicilia', 'almanacco illustrato'
}

def is_valid_real_entity(name):
    name_low = name.lower().strip()
    if len(name_low) < 3:
        return False
    for bw in blacklist_words:
        if bw in name_low:
            return False
    # Rimuovi stringhe spezzate o con newline
    if '\n' in name or '\r' in name or len(name) > 40:
        return False
    # Deve contenere lettere e non solo numeri/punteggiatura
    if not re.search(r'[a-zA-ZÀ-ÿ]', name):
        return False
    return True

filtered = [it for it in items if is_valid_real_entity(it['name'])]

# Suddivisione tematica intelligente
persone_storiche = [] # Giornalisti, Autori, Presidenti, Dirigenti, Arbitri
calciatori_tecnici = [] # Calciatori/Allenatori citati
eventi_giudiziari = [] # Eventi, sentenze, vicende
club_avversari = [] # Squadre/club citati
luoghi_stadi = [] # Stadi, campi, piazze

for it in filtered:
    name = it['name']
    low = name.lower()
    cats = it.get('categories', [])
    
    # Riconoscimento categorie
    if any(c in ['Presidenti / Proprietà', 'Dirigenti / Area Tecnica', 'Arbitri storici', 'Allenatori'] for c in cats):
        persone_storiche.append(it)
    elif any(term in low for term in ['stadio', 'campo', 'arena', 'palasport', 'piazza', 'corso', 'via ']):
        luoghi_stadi.append(it)
    elif any(term in low for term in ['caso ', 'radiazione', 'scandalo', 'scommesse', 'alluvione', 'spareggio', 'spareggi', 'rivolta', 'clamoroso', 'terremoto', 'derby']):
        eventi_giudiziari.append(it)
    elif any(term in low for term in ['calcio', 'u.s.', 'a.c.', 'f.c.', 's.s.', 'sportiva', 'united', 'palermo', 'messina', 'siracusa', 'acireale', 'reggina', 'trapani', 'inter', 'milan', 'roma', 'juventus', 'napoli', 'lazio', 'fiorentina', 'bari', 'foggia', 'taranto', 'cosenza', 'salernitana', 'lecce', 'avellino', 'catanzaro']):
        club_avversari.append(it)
    else:
        # Persona o entità generica
        words = name.split()
        if len(words) == 2 and words[0][0].isupper() and words[1][0].isupper():
            persone_storiche.append(it)
        else:
            persone_storiche.append(it)

print(f"Totale entità candidate reali estratte: {len(filtered)}")

def print_section(title, lst, limit=15):
    print(f"\n=======================================================")
    print(f" {title} (Top {min(limit, len(lst))})")
    print(f"=======================================================")
    for idx, it in enumerate(lst[:limit], 1):
        sample = ', '.join([s.split('/')[-1] for s in it['sample_pages'][:3]])
        print(f"{idx:2d}. {it['name']:<28} | Pagine: {it['distinct_pages']:<4} | Citazioni: {it['total_mentions']:<4} | Fonti: {sample}")

print_section("PERSONAGGI (Autori, Giornalisti, Presidenti, Dirigenti, Arbitri)", persone_storiche, 25)
print_section("EVENTI STORICI, SCANDALI, CASI GIUDIZIARI & SPAREGGI", eventi_giudiziari, 15)
print_section("STADI, IMPIANTI E LUOGHI STORICI", luoghi_stadi, 15)
print_section("CLUB & AVVERSARI STORICI PIÙ CITATI", club_avversari, 15)

# Salva output strutturato
out = {
    "persone_storiche": persone_storiche[:50],
    "eventi_giudiziari": eventi_giudiziari[:30],
    "luoghi_stadi": luoghi_stadi[:30],
    "club_avversari": club_avversari[:30]
}
with open("data_candidates_classified.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
