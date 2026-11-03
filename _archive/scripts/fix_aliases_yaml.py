import os
import yaml

settori_dir = 'content/06-tifoseria-e-cultura/settori'
fixed = 0

for root, dirs, files in os.walk(settori_dir):
    for f in files:
        if f.endswith('.md'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            if c.startswith('---'):
                parts = c.split('---', 2)
                fm_text = parts[1]
                body = parts[2]
                
                # Normalize aliases lines
                lines = fm_text.split('\n')
                new_lines = []
                in_aliases = False
                for line in lines:
                    if line.strip().startswith('aliases:'):
                        in_aliases = True
                        new_lines.append(line)
                    elif in_aliases:
                        if line.strip().startswith('-'):
                            val = line.strip().lstrip('-').strip().strip('"').strip("'")
                            new_lines.append(f'  - "{val}"')
                        elif line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                            in_aliases = False
                            new_lines.append(line)
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                
                new_fm = '\n'.join(new_lines)
                try:
                    # test parse
                    yaml.safe_load(new_fm)
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(f"---{new_fm}---{body}")
                    fixed += 1
                except Exception as e:
                    print(f"Error on {p}: {e}")

print(f"Validated and formatted {fixed} files in settori.")
