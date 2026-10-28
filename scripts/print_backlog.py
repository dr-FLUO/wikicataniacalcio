import json

with open("backlog_priorita.json", "r", encoding="utf-8") as f:
    data = json.load(f)

backlog = data["prioritized_backlog"]
print(f"Total red wikilinks in backlog: {len(backlog)}")
for i, item in enumerate(backlog[:50], 1):
    cnt = item["incoming_references_count"]
    target = item["target_slug"]
    score = item["priority_score"]
    sources = ", ".join([s.split("/")[-1] for s in item["source_pages"][:3]])
    print(f"{i:2d}. ({cnt}x) [[{target}]] -> font: {sources}")
