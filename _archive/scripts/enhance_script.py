import os
import re
import yaml

def enhance():
    with open('scripts/update_all_player_cards.py', 'r', encoding='utf-8') as f:
        code = f.read()

    idx_start = code.find("    # Extract photo URL")
    idx_end = code.find("    # Check if there's already an nfc-player-hero-card")

    new_extraction = '''    # Extract photo URL
    photo_url = None
    candidate_img = fm.get('image') or fm.get('cover_image')
    if not candidate_img and 'image_credits' in fm and isinstance(fm['image_credits'], list):
        for ic in fm['image_credits']:
            if isinstance(ic, dict) and 'image_path' in ic:
                ip = str(ic['image_path']).strip()
                if any(ip.lower().endswith(ext) for ext in ['.webp', '.png', '.jpg', '.jpeg']) and not ip.startswith('http'):
                    candidate_img = ip
                    break

    if candidate_img:
        img_str = str(candidate_img).strip()
        if img_str.startswith('http'):
            photo_url = img_str
        else:
            norm = img_str.replace('\\\\', '/').lstrip('./').lstrip('/')
            idx_assets = norm.find('assets/')
            if idx_assets != -1:
                norm = norm[idx_assets:]
            photo_url = '/' + norm

    if not photo_url:
        m_src = re.search(r'src="([^"]+assets/[^"]+\.(?:webp|png|jpg|jpeg))"', body, re.IGNORECASE)
        if m_src:
            photo_url = m_src.group(1)
        else:
            m_md = re.search(r'!\\[.*?\\]\\(([^)]*assets/[^)]+\\.(?:webp|png|jpg|jpeg))\\)', body, re.IGNORECASE)
            if m_md:
                norm = m_md.group(1).replace('\\\\', '/').lstrip('./').lstrip('/')
                idx_assets = norm.find('assets/')
                if idx_assets != -1:
                    norm = norm[idx_assets:]
                photo_url = '/' + norm
'''

    code = code[:idx_start] + new_extraction + '\n' + code[idx_end:]
    with open('scripts/update_all_player_cards.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Enhanced script written successfully!")

if __name__ == '__main__':
    enhance()
