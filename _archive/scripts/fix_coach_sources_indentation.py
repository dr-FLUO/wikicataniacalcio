import glob, re
from pathlib import Path

coach_files = list(Path("content/03-tesserati/allenatori").glob("**/*.md"))
fixed = 0

for cf in coach_files:
    raw = cf.read_text(encoding="utf-8")
    # if sources has 2-space indented list items mixed with 0-space
    # match pattern:
    # sources:\n  - author: "Wikipedia Italia"\n    title: ...
    if "sources:\n  - author: \"Wikipedia Italia\"" in raw:
        # replace with 0-space indentation
        raw = raw.replace(
            "sources:\n  - author: \"Wikipedia Italia\"",
            "sources:\n- author: \"Wikipedia Italia\""
        )
        # also fix indentation of following lines under this item:
        # "    title:" -> "  title:"
        # "    publisher:" -> "  publisher:"
        # "    year:" -> "  year:"
        # "    url:" -> "  url:"
        # "    reference:" -> "  reference:"
        raw = re.sub(
            r'(- author: "Wikipedia Italia"\n)    (title:.*?\n)    (publisher:.*?\n)    (year:.*?\n)    (url:.*?\n)    (reference:.*?\n)',
            r'\1  \2  \3  \4  \5  \6',
            raw
        )
        cf.write_text(raw, encoding="utf-8")
        fixed += 1

print(f"[OK] Fixed sources indentation in {fixed} coach files.")
