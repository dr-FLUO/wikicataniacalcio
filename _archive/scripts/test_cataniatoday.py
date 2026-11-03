import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://www.cataniatoday.it/sport/calcio/catania-lo-monaco-dimissioni-27-novembre-2019.html', headers=headers)
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
for im in imgs:
    if any(ext in im.lower() for ext in ['.jpg', '.jpeg', '.webp', '.png']):
        print(im)
