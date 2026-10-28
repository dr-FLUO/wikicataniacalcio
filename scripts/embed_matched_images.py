import os
import re

embed_mappings = {
    "content/tesserati/allenatori/carmelo-di-bella.md": ("assets/images/allenatori/carmelo-di-bella-calcio-catania-allenatore-record-panchine-1958-1977.webp", "Carmelo Di Bella alla guida del Calcio Catania"),
    "content/tesserati/allenatori/cristiano-lucarelli.md": ("assets/images/allenatori/cristiano-lucarelli-calcio-catania-allenatore-coppa-italia-serie-c-2017-2024.webp", "Cristiano Lucarelli, tecnico rossazzurro vincitore della Coppa Italia Serie C"),
    "content/tesserati/allenatori/diego-simeone.md": ("assets/images/allenatori/diego-simeone-calcio-catania-allenatore-serie-a-2011.webp", "Diego Pablo Simeone sulla panchina del Catania in Serie A 2010-2011"),
    "content/tesserati/allenatori/domenico-toscano.md": ("assets/images/allenatori/domenico-toscano-calcio-catania-allenatore-serie-c-2024-2027.webp", "Domenico Toscano, allenatore del Catania FC"),
    "content/tesserati/allenatori/egizio-rubino.md": ("assets/images/allenatori/egizio-rubino-calcio-catania-allenatore-serie-a-1968-1974.webp", "Egizio Rubino, storico tecnico della promozione in Serie A del 1969-1970"),
    "content/tesserati/allenatori/guido-mazzetti.md": ("assets/images/allenatori/guido-mazzetti-calcio-catania-allenatore-anni-1970.webp", "Guido Mazzetti, leggenda della panchina etnea negli anni Settanta"),
    "content/tesserati/allenatori/pasquale-marino.md": ("assets/images/allenatori/pasquale-marino-calcio-catania-allenatore-promozione-serie-a-2005-2007.webp", "Pasquale Marino, artefice del ritorno in Serie A nel 2005-2006"),
    "content/tesserati/allenatori/vincenzo-montella.md": ("assets/images/allenatori/vincenzo-montella-calcio-catania-allenatore-serie-a-2011-2012.webp", "Vincenzo Montella, autore del record di punti in Serie A 2011-2012"),
    "content/tesserati/allenatori/walter-zenga.md": ("assets/images/allenatori/walter-zenga-calcio-catania-allenatore-serie-a-2008-2009.webp", "Walter Zenga, protagonista delle storiche salvezze e del derby di Palermo"),
    "content/societa/presidenti/angelo-massimino.md": ("assets/images/presidenti-dirigenti/angelo-massimino-calcio-catania-presidente-storico-1969-1996.webp", "Il 'Presidentissimo' Angelo Massimino"),
    "content/societa/presidenti/antonino-pulvirenti.md": ("assets/images/presidenti-dirigenti/antonino-pulvirenti-calcio-catania-presidente-serie-a-2004-2015.webp", "Antonino Pulvirenti, presidente del Catania dal 2004 al 2015"),
    "content/societa/presidenti/pietro-lo-monaco.md": ("assets/images/presidenti-dirigenti/pietro-lo-monaco-calcio-catania-amministratore-delegato-2004-2012.webp", "Pietro Lo Monaco, storico amministratore delegato del Catania in Serie A"),
    "content/societa/presidenti/ross-pelligra.md": ("assets/images/presidenti-dirigenti/ross-pelligra-calcio-catania-presidente-catania-fc-2022-oggi.webp", "Ross Pelligra, presidente e patron del Catania FC dal 2022"),
    "content/partite/1960-1961/catania-inter-2-0.md": ("assets/images/partite-storiche/catania-inter-2-0-clamoroso-al-cibali-serie-a-1960-1961.webp", "Fase di gioco della storica vittoria per 2-0 contro l'Inter di Helenio Herrera (Clamoroso al Cibali!)"),
    "content/partite/2009-2010/catania-inter-3-1.md": ("assets/images/partite-storiche/catania-inter-3-1-cucchiaio-rigore-mascara-serie-a-2009-2010.webp", "Festa rossazzurra al Cibali nel memorabile 3-1 contro l'Inter del Triplete"),
    "content/partite/2008-2009/palermo-catania-0-4.md": ("assets/images/partite-storiche/palermo-catania-0-4-gol-centrocampo-mascara-serie-a-2008-2009.webp", "Giuseppe Mascara festeggiato dopo il capolavoro balistico da 50 metri al Barbera"),
    "content/stagioni/1982-1983.md": ("assets/images/stagioni/formazioni-storiche/formazione-calcio-catania-spareggi-roma-serie-b-1982-1983.webp", "La formazione del Calcio Catania protagonista dello spareggio promozione di Roma nel giugno 1983"),
    "content/stadio/torre-del-grifo.md": ("assets/images/strutture-e-stadi/centro-sportivo-torre-del-grifo-village-calcio-catania.webp", "Panoramica del Centro Sportivo Torre del Grifo Village"),
    "content/stadio/piazza-esposizione.md": ("assets/images/strutture-e-stadi/campo-piazza-esposizione-calcio-catania-storico-1930.webp", "Lo storico Campo di Piazza Esposizione (oggi Piazza Verga) negli anni Trenta"),
    "content/tesserati/calciatori/claudio-ranieri.md": ("assets/images/calciatori/figurine/claudio-ranieri-calcio-catania-figurina-panini-1982-1983.webp", "Claudio Ranieri in maglia rossazzurra nel campionato di Serie B 1982-1983"),
    "content/tesserati/calciatori/aldo-cantarutti.md": ("assets/images/calciatori/figurine/aldo-cantarutti-calcio-catania-figurina-panini-1982-1983.webp", "Aldo Cantarutti, bomber degli spareggi promozione del 1983"),
    "content/tesserati/calciatori/damiano-morra.md": ("assets/images/calciatori/figurine/damiano-morra-calcio-catania-figurina-panini-1975-1984.webp", "Damiano Morra, recordman assoluto di presenze nella storia del Calcio Catania"),
    "content/tesserati/calciatori/aquilino-bonfanti.md": ("assets/images/calciatori/figurine/aquilino-bonfanti-calcio-catania-figurina-panini-1970-1971.webp", "Aquilino Bonfanti, capocannoniere della Serie B 1969-1970"),
    "content/tesserati/calciatori/giancarlo-danova.md": ("assets/images/calciatori/figurine/giancarlo-danova-calcio-catania-figurina-panini-1965-1966.webp", "Giancarlo Danova con la casacca del Catania in Serie A"),
    "content/tesserati/calciatori/roberto-inglese.md": ("assets/images/calciatori/rosa-attuale/roberto-inglese-calcio-catania-attaccante-bomber-2026-2027.webp", "Roberto Inglese, centravanti e punto di riferimento offensivo del Catania FC"),
}

embedded_count = 0
for md_path, (img_url, caption) in embed_mappings.items():
    if not os.path.exists(md_path):
        continue
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has image
    if img_url in content:
        continue
    
    # Add image right after frontmatter
    # Frontmatter is between --- and ---
    match = re.search(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if match:
        header = match.group(0)
        body = content[len(header):]
        
        # Check if frontmatter has image: field, update or add it
        fm_text = match.group(1)
        if "image:" not in fm_text:
            fm_text += f'\nimage: "{img_url}"'
            new_header = f"---\n{fm_text}\n---\n"
        else:
            new_header = header
            
        img_markdown = f"\n![{caption}](/{img_url})\n\n"
        new_content = new_header + img_markdown + body
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        embedded_count += 1
        print(f"Embedded into {md_path}")

print(f"Total files updated with authentic images: {embedded_count}")
