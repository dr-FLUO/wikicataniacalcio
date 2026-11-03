import requests
import re

headers = {'User-Agent': 'Mozilla/5.0'}
urls = [
    'https://www.cataniatoday.it/sport/calcio-catania-pulvirenti-processo-bancarotta.html',
    'https://www.cataniatoday.it/sport/calcio/catania-lo-monaco-dimissioni-27-novembre-2019.html'
]
for u in urls:
    r = requests.get(u, headers=headers)
    og = re.findall(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', r.text)
    if not og:
        og = re.findall(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', r.text)
    print(u, og)
