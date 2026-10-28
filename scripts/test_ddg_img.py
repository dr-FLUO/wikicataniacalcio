from duckduckgo_search import DDGS

ddgs = DDGS()
results = list(ddgs.images("Antonino Pulvirenti Catania calcio", max_results=3))
print("Results for Pulvirenti:")
for r in results:
    print(r.get('title'), "->", r.get('image'))
