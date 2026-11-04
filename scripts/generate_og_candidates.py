import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = r"C:/Users/sim0n/.gemini/antigravity/brain/08a97f3f-ee55-4830-86fe-3ddc0f657b06"
W, H = 1200, 630

RED = (209, 19, 23)      # #d11317
BLUE = (12, 178, 217)    # #0cb2d9
GOLD = (210, 153, 51)    # #d29933
DARK_BG = (14, 15, 18)

font_display_path = "quartz/static/fonts/BigShouldersDisplay-900.ttf"
font_sans_bold_path = "C:/Windows/Fonts/segoeuib.ttf"
font_sans_reg_path = "C:/Windows/Fonts/segoeui.ttf"

font_kicker = ImageFont.truetype(font_sans_bold_path, 19)
font_title = ImageFont.truetype(font_display_path, 74)
font_sub = ImageFont.truetype(font_sans_bold_path, 21)
font_badge = ImageFont.truetype(font_sans_bold_path, 16)
font_url = ImageFont.truetype(font_sans_bold_path, 18)

def render_og_banner(bg_path, out_name, brightness=0.40):
    # 1. Base canvas
    card = Image.new("RGBA", (W, H), DARK_BG + (255,))
    
    # 2. Background photo
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA")
        bg_ratio = bg.width / bg.height
        target_ratio = W / H
        if bg_ratio > target_ratio:
            new_h = H
            new_w = int(H * bg_ratio)
        else:
            new_w = W
            new_h = int(W / bg_ratio)
        bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - W) // 2
        top = (new_h - H) // 2
        bg_cropped = bg.crop((left, top, left + W, top + H))
        
        # Dim brightness
        dimmer = ImageEnhance.Brightness(bg_cropped).enhance(brightness)
        card.paste(dimmer, (0, 0))
    
    # 3. Vignette overlay: deep dark edges, softly lit center
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    for y in range(H):
        yf = y / H
        # smooth curve from top to bottom
        alpha = int(145 + 95 * yf)
        draw_ov.line([(0, y), (W, y)], fill=(10, 12, 16, min(250, alpha)))
        
    card = Image.alpha_composite(card, overlay)
    
    # Side shadow / vignette masks
    side_mask = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_side = ImageDraw.Draw(side_mask)
    for x in range(250):
        a = int(220 * (1 - x / 250)**1.5)
        draw_side.line([(x, 0), (x, H)], fill=(10, 12, 16, a))
        draw_side.line([(W - 1 - x, 0), (W - 1 - x, H)], fill=(10, 12, 16, a))
    card = Image.alpha_composite(card, side_mask)
    
    # Atmospheric center glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow)
    draw_glow.ellipse([W//2 - 260, 60, W//2 + 260, 500], fill=(12, 178, 217, 30))
    draw_glow.ellipse([W//2 - 180, 80, W//2 + 180, 440], fill=(209, 19, 23, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(45))
    card = Image.alpha_composite(card, glow)
    
    draw = ImageDraw.Draw(card)
    
    # 4. Top & Bottom Rossazzurro stripes (editorial mark)
    stripe_h = 7
    draw.rectangle([0, 0, W//2, stripe_h], fill=RED)
    draw.rectangle([W//2, 0, W, stripe_h], fill=BLUE)
    
    draw.rectangle([0, H - stripe_h, W//2, H], fill=RED)
    draw.rectangle([W//2, H - stripe_h, W, H], fill=BLUE)
    
    # 5. Central Emblem (Wiki Calcio Catania official icon)
    icon_path = "quartz/static/icon.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon_size = 136
        icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icon_x = (W - icon_size) // 2
        icon_y = 66
        
        # Soft drop shadow
        shadow = Image.new("RGBA", (icon_size + 30, icon_size + 30), (0, 0, 0, 0))
        sh_draw = ImageDraw.Draw(shadow)
        sh_draw.ellipse([15, 15, icon_size + 15, icon_size + 15], fill=(0, 0, 0, 190))
        shadow = shadow.filter(ImageFilter.GaussianBlur(12))
        card.paste(shadow, (icon_x - 15, icon_y - 6), shadow)
        card.paste(icon, (icon_x, icon_y), icon)
        
    # 6. Kicker
    kicker_text = "ENCICLOPEDIA STORICA & ARCHIVIO DIGITALE"
    bbox_k = font_kicker.getbbox(kicker_text)
    kw = bbox_k[2] - bbox_k[0]
    draw.text(((W - kw) // 2, 222), kicker_text, font=font_kicker, fill=BLUE)
    
    # 7. Main Title: WIKI CALCIO CATANIA
    title_text = "WIKI CALCIO CATANIA"
    bbox_t = font_title.getbbox(title_text)
    tw = bbox_t[2] - bbox_t[0]
    draw.text(((W - tw) // 2, 256), title_text, font=font_title, fill=(255, 255, 255))
    
    # 8. Subtitle
    sub_text = "LA MEMORIA ROSSAZZURRA · DAL 1929 A OGGI"
    bbox_s = font_sub.getbbox(sub_text)
    sw = bbox_s[2] - bbox_s[0]
    draw.text(((W - sw) // 2, 356), sub_text, font=font_sub, fill=(215, 220, 230))
    
    # 9. Badges
    badges = ["95 STAGIONI", "1.341 TESSERATI", "TABELLINI & PALMARES"]
    pill_padding_x = 18
    pill_h = 36
    pill_spacing = 14
    pill_widths = []
    for b in badges:
        bb = font_badge.getbbox(b)
        pill_widths.append((bb[2] - bb[0]) + 2 * pill_padding_x)
    
    total_pills_w = sum(pill_widths) + pill_spacing * (len(badges) - 1)
    start_x = (W - total_pills_w) // 2
    pill_y = 416
    
    curr_x = start_x
    for i, b in enumerate(badges):
        pw = pill_widths[i]
        draw.rounded_rectangle(
            [curr_x, pill_y, curr_x + pw, pill_y + pill_h],
            radius=18,
            fill=(24, 28, 36, 230),
            outline=(255, 255, 255, 55),
            width=1
        )
        bb = font_badge.getbbox(b)
        bw = bb[2] - bb[0]
        bh = bb[3] - bb[1]
        text_x = curr_x + (pw - bw) // 2
        text_y = pill_y + (pill_h - bh) // 2 - 2
        draw.text((text_x, text_y), b, font=font_badge, fill=(245, 245, 245))
        curr_x += pw + pill_spacing

    # 10. URL signature
    url_text = "www.wikicataniacalcio.com"
    bbox_u = font_url.getbbox(url_text)
    uw = bbox_u[2] - bbox_u[0]
    draw.text(((W - uw) // 2, 532), url_text, font=font_url, fill=(155, 170, 190))
    
    # Save main 1200x630
    out_path = os.path.join(OUT_DIR, out_name)
    rgb_card = card.convert("RGB")
    rgb_card.save(out_path, quality=95)
    print(f"Saved banner: {out_path}")
    
    # Also save 1:1 square preview simulation (center crop 630x630)
    sq_crop = rgb_card.crop(((W - H) // 2, 0, (W + H) // 2, H))
    sq_name = out_name.replace(".png", "_square.png")
    sq_path = os.path.join(OUT_DIR, sq_name)
    sq_crop.save(sq_path, quality=95)
    print(f"Saved square preview: {sq_path}")
    return out_path

# Generate variants
render_og_banner(
    "content/assets/images/tifoseria-e-curva/curva-nord-catania-coreografia-ciccio-famoso-stadio-massimino.webp",
    "og_curva_nord.png",
    brightness=0.38
)

render_og_banner(
    "content/assets/images/strutture-e-stadi/stadio-angelo-massimino-cibali-calcio-catania-tribuna-panoramica.webp",
    "og_massimino_panoramica.png",
    brightness=0.35
)

render_og_banner(
    "quartz/static/images/photos/catania-fc-match-cibali.jpg",
    "og_match_cibali.png",
    brightness=0.38
)
