import urllib.request
import json

def get_wiki_image(title, lang="it"):
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=pageimages|images&format=json&pithumbsize=800"
    req = urllib.request.Request(url, headers={'User-Agent': 'WikiCataniaBot/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                if 'thumbnail' in pdata:
                    return pdata['thumbnail']['source']
                if 'images' in pdata:
                    return [img['title'] for img in pdata['images']]
    except Exception as e:
        return f"Error: {e}"
    return None

test_names = ["Cristiano Lucarelli", "Domenico Toscano", "Claudio Ranieri", "Amedeo Biavati", "Stefano Sturaro", "Antonino Pulvirenti", "Pietro Lo Monaco"]
for name in test_names:
    res = get_wiki_image(name)
    print(f"{name}: {res}")
