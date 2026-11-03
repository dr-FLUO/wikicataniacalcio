import os
import re
import yaml

fixed_files = 0
self_aliases_removed = 0

for root, dirs, files in os.walk('content'):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                content = fp.read()

            if not content.startswith('---'):
                continue

            parts = content.split('---', 2)
            if len(parts) < 3:
                continue

            fm_raw = parts[1]
            body = parts[2]

            try:
                fm = yaml.safe_load(fm_raw) or {}
            except Exception:
                continue

            rel_path = os.path.relpath(p, 'content').replace('\\', '/').replace('.md', '')
            rel_folder = rel_path[:-6] if rel_path.endswith('/index') else rel_path

            current_slug = fm.get('slug', rel_path)
            slug_clean = current_slug.rstrip('/')
            if slug_clean.endswith('/index'):
                slug_clean = slug_clean[:-6]

            # If index.md, ensure slug is the folder slug, not folder/index
            slug_changed = False
            if f == 'index.md' and fm.get('slug'):
                if fm['slug'] != rel_folder:
                    fm['slug'] = rel_folder
                    slug_changed = True

            aliases = fm.get('aliases', [])
            if isinstance(aliases, list) and len(aliases) > 0:
                new_aliases = []
                seen_aliases = set()
                for a in aliases:
                    a_clean = str(a).strip().strip('/')
                    # Condition for circular alias:
                    # matches current slug, matches relative path, matches folder path
                    is_circular = (
                        a_clean == current_slug.strip('/') or
                        a_clean == slug_clean or
                        a_clean == rel_path or
                        a_clean == rel_folder or
                        a_clean == f"{rel_folder}/index"
                    )

                    if is_circular:
                        self_aliases_removed += 1
                        continue

                    if a_clean not in seen_aliases and a_clean:
                        seen_aliases.add(a_clean)
                        new_aliases.append(a_clean)

                if len(new_aliases) != len(aliases) or slug_changed:
                    if new_aliases:
                        fm['aliases'] = new_aliases
                    else:
                        del fm['aliases']
                    
                    new_fm_raw = yaml.dump(fm, allow_unicode=True, sort_keys=False)
                    new_content = f"---\n{new_fm_raw}---{body}"
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(new_content)
                    fixed_files += 1

print(f"Sanitization complete: removed {self_aliases_removed} circular aliases across {fixed_files} files.")
