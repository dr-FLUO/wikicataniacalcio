import requests
import re

url = "https://www.lasicilia.it/archivio/calcio-catania-nuovo-processo-per-lex-presidente-pulvirenti-per-appropriazione-indebita-966953/"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
imgs = re.findall(r'https://lasicilia\.cdn\.m33cloud\.com/[^"\']+\.jpg', r.text)
for im in set(imgs):
    print("La Sicilia Pulvirenti img:", im)
