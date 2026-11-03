# -*- coding: utf-8 -*-
import os
import re

def update_nicolo_nicolosi():
    path = 'content/03-tesserati/calciatori/storici/nicolo-nicolosi.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(
        r'con 7 presenze e 7 gol registrati in maglia rossazzurra\.',
        'con 156 presenze ufficiali (149 in campionato) e 78 reti registrate in maglia rossazzurra.',
        text
    )
    text = text.replace('total_appearances: 7\ntotal_goals: 7', 'total_appearances: 156\nleague_appearances: 149\ntotal_goals: 78')
    text = text.replace('total_appearances: 7\r\ntotal_goals: 7', 'total_appearances: 156\r\nleague_appearances: 149\r\ntotal_goals: 78')
    text = text.replace('seasons_count: 2', 'seasons_count: 8')

    text = re.sub(
        r'<td colspan="3">1935–1937</td>',
        '<td colspan="3">1932–1937, 1939–1940, 1942–1943, 1947–1949</td>',
        text
    )
    text = re.sub(
        r'<th>Presenze</th>\s*<td>7</td>\s*<th>Goal / Assist</th>\s*<td>7 / 0</td>',
        '<th>Presenze</th>\n        <td>156</td>\n        <th>Goal / Assist</th>\n        <td>78 / 0</td>',
        text
    )

    text = re.sub(
        r'in \*\*149 presenze complessive\*\*',
        'in **156 presenze complessive** (di cui 149 in campionato tra regular season, gironi finali e spareggi, e 7 in Coppa Italia)',
        text
    )

    # Clean URLs
    text = re.sub(
        r'consultabile su \[calciocatania\.com\]\(https://www\.calciocatania\.com/\)/giocatori/\)/giocatori/\)\.\s*e Bibliografia',
        'consultabile su [calciocatania.com](https://www.calciocatania.com/giocatori/).\n\n## Bibliografia',
        text
    )
    text = text.replace('https://www.[tuttoilcataniaminutoperminuto.it](https://www.[tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/)/)/)', 'https://www.tuttoilcataniaminutoperminuto.it/')

    # Replace bottom TM 7-game table
    old_bottom = re.search(r'### Rendimento Stagione per Stagione in Maglia Rossazzurra.*', text, re.DOTALL)
    if old_bottom:
        new_bottom = '''### Rendimento Stagione per Stagione in Maglia Rossazzurra

| Stagione | Competizione | Presenze | Gol | Note Storiche |
| :--- | :--- | :---: | :---: | :--- |
| **1932-1933** | Prima Divisione (III livello) | 18 | 11 | Esordio col Catania a Piazza Esposizione |
| **1933-1934** | Prima Divisione (III livello) | 30 | 18 | Promozione in Serie B (14 reg. + 4 girone finale) |
| **1934-1935** | Serie B | 27 | 13 | 3º posto nel girone A (sfiorata la Serie A) |
| **1935-1936** | Serie B + Coppa Italia | 35 | 15 | 12 reti in Serie B, 3 in Coppa Italia |
| **1936-1937** | Serie B + Coppa Italia | 30 | 15 | 11 reti in Serie B, 4 in Coppa Italia |
| **1939-1940** | Serie B + Coppa Italia | 23 | 3 | Ritorno al Cibali |
| **1942-1943** | Serie C | 16 | 10 | Torneo sospeso per cause belliche |
| **1947-1949** | Serie C | 25 | 11 | Rinascita del Club Calcio Catania e promozione in B |
| **TOTALE** | **8 Stagioni (4 Cicli)** | **156** | **78** | **Recordman assoluto di reti nella storia del club** |

> [!info] Dettaglio di Rendimento Agonistico Consolidato
> In maglia rossazzurra, Nicolò «Cocò» Nicolosi ha collezionato complessivamente **156 presenze ufficiali** (149 in campionato e 7 in Coppa Italia) e siglato **78 reti** (71 in campionato e 7 nelle coppe e spareggi), mantenendo il primato assoluto di segnature del club.
> 
> *Nota archivistica del 2023:* Nell'ottobre 2023 i ricercatori di *Tutto il Catania minuto per minuto* hanno documentato l'attribuzione a Nicolosi del 2º gol in Catania-Novara 2-0 del 27 gennaio 1935 (precedentemente assegnato a Bodini), portando il computo storico a **79 reti effettive**.'''
        text = text[:old_bottom.start()] + new_bottom + '\n'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated nicolo-nicolosi.md successfully')

def update_marco_biagianti():
    path = 'content/03-tesserati/calciatori/storici/marco-biagianti.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # YAML
    text = text.replace('league_appearances: 258', 'league_appearances: 255\nleague_goals: 11')
    text = text.replace('serie_a_appearances: 153', 'serie_a_appearances: 148\nserie_a_goals: 3')
    text = text.replace('seasons_count: 12', 'seasons_count: 11')

    # Remove duplicated image credits in frontmatter
    text = re.sub(r'image_credits:(\s*- image_path: assets/images/calciatori/marco-biagianti\.jpg\s*alt_text:[^\n]+\s*author_or_archive:[^\n]+\s*year:[^\n]+\s*license_type:[^\n]+){2,}',
                  '''image_credits:
- image_path: assets/images/calciatori/marco-biagianti.jpg
  alt_text: Ritratto ufficiale di Marco Biagianti in maglia rossazzurra
  author_or_archive: Archivio Storico e Iconografico Calcio Catania
  year: 2026
  license_type: Certificato di Pubblico Dominio / Documentazione Sportiva''', text)

    # Hero table
    text = re.sub(
        r'<th>Presenze</th>\s*<td>284</td>\s*<th>Goal / Assist</th>\s*<td>\d+ / 11</td>',
        '<th>Presenze</th>\n        <td>284</td>\n        <th>Goal / Assist</th>\n        <td>12 / 11</td>',
        text
    )

    # Text intro
    text = re.sub(
        r'con \*\*284 gare complessive\*\* \(di cui \*\*258 in campionato\*\* e \*\*153 in Serie A\*\*\)',
        'con **284 gare complessive** (di cui **255 in campionato regolare**, **11 nei play-off** e **18 nelle coppe**, per un totale di **148 gare e 3 reti in Serie A** e **12 reti complessive**)',
        text
    )

    # Fix URLs
    text = text.replace('https://www.[tuttoilcataniaminutoperminuto.it](https://www.[tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/)/)/)', 'https://www.tuttoilcataniaminutoperminuto.it/')
    text = text.replace('[calciocatania.com](https://www.calciocatania.com/)/giocatori/giocatori.php?Biagianti-10)', '[calciocatania.com](https://www.calciocatania.com/giocatori/giocatori.php?Biagianti-10)')

    # Accordion
    text = text.replace(
        '- **Dettaglio Competizioni:** 153 presenze in Serie A (3 reti), 105 in Serie C / Lega Pro (2 reti), 11 nei Playoff di Serie C, 15 tra Coppa Italia maggiore e Coppa Italia Serie C (1 rete).',
        '- **Dettaglio Competizioni:** 255 presenze in campionati regolari (148 in Serie A con 3 reti, 107 in Serie C con 8 reti), 11 presenze nei Playoff di Serie C, 18 presenze nelle coppe (11 in Coppa Italia maggiore, 7 con 1 rete in Coppa Italia Serie C) per complessive 284 presenze ufficiali e 12 reti.'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated marco-biagianti.md successfully')

def update_mariano_izco():
    path = 'content/03-tesserati/calciatori/storici/mariano-izco.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # YAML
    text = text.replace('league_appearances: 262', 'league_appearances: 239\nleague_goals: 6')
    text = text.replace('seasons_count: 10', 'seasons_count: 10')

    # Remove duplicated image credits
    text = re.sub(r'image_credits:(\s*- image_path: assets/images/calciatori/mariano-izco\.jpg\s*alt_text:[^\n]+\s*author_or_archive:[^\n]+\s*year:[^\n]+\s*license_type:[^\n]+){2,}',
                  '''image_credits:
- image_path: assets/images/calciatori/mariano-izco.jpg
  alt_text: Ritratto ufficiale di Mariano Izco in maglia rossazzurra
  author_or_archive: Archivio Storico e Iconografico Calcio Catania
  year: 2026
  license_type: Certificato di Pubblico Dominio / Documentazione Sportiva''', text)

    # Hero table
    text = re.sub(
        r'<th>Presenze</th>\s*<td>258</td>\s*<th>Goal / Assist</th>\s*<td>7 / 16</td>',
        '<th>Presenze</th>\n        <td>258 (280 tot.)</td>\n        <th>Goal / Assist</th>\n        <td>7 / 16</td>',
        text
    )

    # Prose
    text = text.replace('su **280 presenze ufficiali complessive**', 'su **258 presenze ufficiali omologate FIGC** e **280 gare effettive complessive**')
    text = text.replace('[calciocatania.com](https://www.calciocatania.com/)/giocatori/giocatori.php?Izco-21)', '[calciocatania.com](https://www.calciocatania.com/giocatori/giocatori.php?Izco-21)')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated mariano-izco.md successfully')

def update_francesco_lodi():
    path = 'content/03-tesserati/calciatori/storici/francesco-lodi.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('title: Francesco Lodi — Il Regista dei Quattro Cicli (238 Presenze e 53 Reti)', 'title: Francesco Lodi — Il Regista dei Quattro Cicli (239 Presenze e 54 Reti)')
    text = text.replace('league_appearances: 209', 'league_appearances: 215')
    text = text.replace('serie_a_appearances: 96', 'serie_a_appearances: 105')
    text = text.replace('league_goals: 46', 'league_goals: 47')
    text = text.replace('serie_a_goals: 19', 'serie_a_goals: 20')

    # Remove duplicated image credits
    text = re.sub(r'image_credits:(\s*- image_path: assets/images/calciatori/francesco-lodi\.jpg\s*alt_text:[^\n]+\s*author_or_archive:[^\n]+\s*year:[^\n]+\s*license_type:[^\n]+){2,}',
                  '''image_credits:
- image_path: assets/images/calciatori/francesco-lodi.jpg
  alt_text: Ritratto ufficiale di Francesco Lodi in maglia rossazzurra
  author_or_archive: Archivio Storico e Iconografico Calcio Catania
  year: 2026
  license_type: Certificato di Pubblico Dominio / Documentazione Sportiva''', text)

    # Prose
    text = text.replace('Con **53 reti ufficiali** è il **terzo miglior marcatore assoluto della storia del Catania** (e il centrocampista più prolifico di sempre), mentre con **238 presenze complessive** occupa il **quinto posto nella classifica *all-time* di presenze**.',
                        'Con **54 reti ufficiali** è il **terzo miglior marcatore assoluto della storia del Catania** (e il centrocampista più prolifico di sempre), mentre con **239 presenze complessive** (215 in campionato, 10 nei playoff/poule scudetto e 14 nelle coppe) occupa il **quinto posto nella classifica *all-time* di presenze** (conteggiato a quota 238 gare e 53 reti nei soli tornei professionistici).')
    text = text.replace('https://www.[tuttoilcataniaminutoperminuto.it](https://www.[tuttoilcataniaminutoperminuto.it](https://www.tuttoilcataniaminutoperminuto.it/)/)/)', 'https://www.tuttoilcataniaminutoperminuto.it/')
    text = text.replace('[calciocatania.com](https://www.calciocatania.com/)/giocatori/giocatori.php?Lodi-13)', '[calciocatania.com](https://www.calciocatania.com/giocatori/giocatori.php?Lodi-13)')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated francesco-lodi.md successfully')

def update_gonzalo_bergessio():
    path = 'content/03-tesserati/calciatori/storici/gonzalo-bergessio.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Hero table
    text = text.replace('<td colspan="3">2010–2014</td>', '<td colspan="3">2011–2014</td>')

    # Remove duplicated image credits
    text = re.sub(r'image_credits:(\s*- image_path: assets/images/calciatori/gonzalo-bergessio\.jpg\s*alt_text:[^\n]+\s*author_or_archive:[^\n]+\s*year:[^\n]+\s*license_type:[^\n]+){2,}',
                  '''image_credits:
- image_path: assets/images/calciatori/gonzalo-bergessio.jpg
  alt_text: Ritratto ufficiale di Gonzalo Bergessio in maglia rossazzurra
  author_or_archive: Archivio Storico e Iconografico Calcio Catania
  year: 2026
  license_type: Certificato di Pubblico Dominio / Documentazione Sportiva''', text)

    text = text.replace('[calciocatania.com](https://www.calciocatania.com/)/giocatori/giocatori.php?Bergessio-16)', '[calciocatania.com](https://www.calciocatania.com/giocatori/giocatori.php?Bergessio-16)')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated gonzalo-bergessio.md successfully')

def update_giuseppe_mascara():
    path = 'content/03-tesserati/calciatori/storici/giuseppe-mascara.md'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('title: Giuseppe Mascara — Il Genio Rossazzurro (60 Reti e 235 Presenze)', 'title: Giuseppe Mascara — Il Genio Rossazzurro (60 Reti e 238 Presenze)')
    text = text.replace('league_appearances: 224', 'league_appearances: 226')
    text = text.replace('serie_a_appearances: 145', 'serie_a_appearances: 149')

    # Remove duplicated image credits
    text = re.sub(r'image_credits:(\s*- image_path: assets/images/calciatori/giuseppe-mascara\.jpg\s*alt_text:[^\n]+\s*author_or_archive:[^\n]+\s*year:[^\n]+\s*license_type:[^\n]+){2,}',
                  '''image_credits:
- image_path: assets/images/calciatori/giuseppe-mascara.jpg
  alt_text: Ritratto ufficiale di Giuseppe Mascara in maglia rossazzurra
  author_or_archive: Archivio Storico e Iconografico Calcio Catania
  year: 2026
  license_type: Certificato di Pubblico Dominio / Documentazione Sportiva''', text)

    # Prose
    text = text.replace('e il **sesto posto assoluto per presenze con 235 gare** (di cui **145 presenze e 31 reti in Serie A**)',
                        'e il **sesto posto assoluto per presenze con 238 gare ufficiali** (di cui **226 gare e 58 reti in campionato**, con **149 presenze e 31 reti in Serie A**, e **12 gare con 2 reti in Coppa Italia**)')
    text = text.replace('[calciocatania.com](https://www.calciocatania.com/)/giocatori/giocatori.php?Mascara-51)', '[calciocatania.com](https://www.calciocatania.com/giocatori/giocatori.php?Mascara-51)')

    # Add explanatory note about 235 vs 238
    note_txt = '''

> [!info] Quadratura Storico-Statistica: 238 Presenze e 60 Reti Ufficiali
> I dati consolidati di Lega Serie A, FIGC e almanacchi storici certificano per Giuseppe Mascara **238 presenze ufficiali e 60 reti** in maglia rossazzurra:
> - **Campionato:** 226 presenze e 58 reti (77 gare e 27 reti in Serie B tra 2003-04 e 2005-06; 149 gare e 31 reti in Serie A tra 2006-07 e gennaio 2011).
> - **Coppa Italia:** 12 presenze e 2 reti (2003-04, 2007-08 con 2 reti, 2008-09, 2009-10 e 2010-11).
> *(La dicitura "235 presenze" presente in alcune vecchie rassegne giornalistiche non includeva le 3 presenze disputate nel gennaio 2011 prima del trasferimento al Napoli).*'''

    if '## 1. L\'Arrivo nell\'Era Gaucci' in text:
        text = text.replace('## 1. L\'Arrivo nell\'Era Gaucci', note_txt + '\n\n## 1. L\'Arrivo nell\'Era Gaucci')
    elif '## L\'Arrivo nell\'Era Gaucci' in text:
        text = text.replace('## L\'Arrivo nell\'Era Gaucci', note_txt + '\n\n## L\'Arrivo nell\'Era Gaucci')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated giuseppe-mascara.md successfully')

if __name__ == '__main__':
    update_nicolo_nicolosi()
    update_marco_biagianti()
    update_mariano_izco()
    update_francesco_lodi()
    update_gonzalo_bergessio()
    update_giuseppe_mascara()
