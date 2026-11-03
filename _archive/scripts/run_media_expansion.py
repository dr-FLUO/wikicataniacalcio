# -*- coding: utf-8 -*-
"""
Esecutore per l'espansione e aggiornamento della sezione 07-media-e-comunicazione.
Risolve sempre i percorsi a partire dalla radice del repository.
"""
import os
import sys
import shutil

# Assicuriamo la codifica corretta su Windows
sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Se per sbaglio esiste scripts/content, rimuovilo
errant_dir = os.path.join(os.path.dirname(__file__), "content")
if os.path.exists(errant_dir):
    shutil.rmtree(errant_dir)
    print(f"Rimosso percorso errato: {errant_dir}")

# Aggiungi scripts al sys.path
sys.path.insert(0, os.path.dirname(__file__))

from data_media_new import NEW_FILES
from data_media_firme import FIRME_FILES
from data_media_updates import UPDATED_FILES

total_written = 0

all_dicts = [
    ("Nuove Testate (5)", NEW_FILES),
    ("Nuove Firme e Voci (14)", FIRME_FILES),
    ("Aggiornamenti File Esistenti (16)", UPDATED_FILES)
]

for group_name, file_dict in all_dicts:
    print(f"--- Applicazione gruppo: {group_name} ---")
    for rel_path, content in file_dict.items():
        abs_target = os.path.join(REPO_ROOT, rel_path)
        # Assicura directory genitore
        os.makedirs(os.path.dirname(abs_target), exist_ok=True)
        # Scrivi file in UTF-8
        with open(abs_target, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content.strip() + '\n')
        total_written += 1
        print(f"  [OK] {rel_path}")

print(f"\nOperazione completata con successo. Scritti/aggiornati in totale: {total_written} file Markdown.")
