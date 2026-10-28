import requests
import re
from PIL import Image
from io import BytesIO
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_page_images(url, pattern):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return re.findall(pattern, r.text)
    except Exception as e:
        print(f"Error {url}: {e}")
    return []

# Test Pulvirenti from Cataniatoday
imgs = get_page_images('https://www.cataniatoday.it/sport/calcio-catania-pulvirenti-processo-bancarotta.html', r'https://citynews-[^"\']+\.jpg')
print("Cataniatoday Pulvirenti:", imgs[:3])

# Test Lo Monaco
imgs_lm = get_page_images('https://www.cataniatoday.it/sport/calcio/catania-lo-monaco-dimissioni-27-novembre-2019.html', r'https://citynews-[^"\']+\.jpg')
print("Cataniatoday Lo Monaco:", imgs_lm[:3])
