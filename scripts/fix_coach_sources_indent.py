import glob
import re
import yaml

files = glob.glob('content/03-tesserati/allenatori/*.md')
fixed = 0

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        continue
    parts = content.split('---', 2)
    if len(parts) < 3:
        continue

    fm_raw = parts[1]
    
    # Check if yaml fails or if indentation is broken under sources:
    # Look for:
    # sources:
    #   - author: ...
    # - author: ...
    # We want all items under sources: to be indented consistently with '- author:' (0 space indent) or '  - author:'
    
    # Let's match the block 'sources:\n  - author: "Wikipedia Italia" ...\n- author:'
    pattern = re.compile(r'(sources:\r?\n)(  - author: [^\r\n]+\r?\n    title: [^\r\n]+\r?\n    publisher: [^\r\n]+\r?\n    year: [^\r\n]+\r?\n    url: [^\r\n]+\r?\n    reference: [^\r\n]+\r?\n)(- author:)')
    
    m = pattern.search(fm_raw)
    if m:
        # unindent the wikipedia block by 2 spaces so it starts with '- author:'
        wiki_block = m.group(2)
        unindented_lines = []
        for line in wiki_block.splitlines(True):
            if line.startswith('  '):
                unindented_lines.append(line[2:])
            else:
                unindented_lines.append(line)
        new_block = m.group(1) + ''.join(unindented_lines) + m.group(3)
        new_fm = pattern.sub(new_block, fm_raw, count=1)
        
        # Test if new_fm parses cleanly with yaml
        try:
            yaml.safe_load(new_fm)
            new_content = '---' + new_fm + '---' + parts[2]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
        except Exception as e:
            print(f'Still failed {filepath}: {e}')

print(f'Fixed {fixed} files')
