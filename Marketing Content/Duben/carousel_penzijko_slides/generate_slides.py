#!/usr/bin/env python3
"""
Instagram Carousel Generator — David Šimana
Téma: České penzijko — skryté poplatky a ušlý zisk
Brand barva: #8E51FF (fialová)
Formát: 1080x1080px PNG
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap

# ─── BRAND COLORS ────────────────────────────────────────────────────────────
BRAND_PURPLE   = (142, 81, 255)    # #8E51FF — primární brand barva
BRAND_PURPLE_D = (90, 40, 180)     # tmavší fialová pro gradienty
BRAND_PURPLE_L = (180, 140, 255)   # světlejší fialová pro akcenty
DARK_BG        = (10, 8, 20)       # téměř černé pozadí
DARK_BG2       = (18, 14, 35)      # druhé tmavé pozadí
WHITE          = (255, 255, 255)
LIGHT_GRAY     = (200, 200, 210)
YELLOW_ACCENT  = (255, 210, 60)    # pro čísla / důraz
RED_ACCENT     = (255, 70, 70)

# ─── FONTS ───────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/noto"
FONT_BLACK    = os.path.join(FONT_DIR, "NotoSans-Black.ttf")
FONT_BOLD     = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
FONT_EXTRABOLD= os.path.join(FONT_DIR, "NotoSans-ExtraBold.ttf")
FONT_REGULAR  = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

W, H = 1080, 1080
OUT_DIR = "/home/ubuntu/carousel_penzijko"

def get_font(path, size):
    return ImageFont.truetype(path, size)

def draw_gradient_bg(img, color_top, color_bottom):
    """Vertikální gradient pozadí."""
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def draw_purple_accent_bar(draw, y, width=6, height=60, x=60):
    """Fialový vertikální accent bar vlevo od textu."""
    draw.rounded_rectangle([x, y, x + width, y + height], radius=3, fill=BRAND_PURPLE)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=2):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def wrap_text(text, font, max_width, draw):
    """Zalamuje text podle pixel šířky."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_multiline(draw, lines, font, x, y, fill, line_spacing=10):
    """Vykreslí více řádků textu."""
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        current_y += (bbox[3] - bbox[1]) + line_spacing
    return current_y

def add_logo_text(draw, text="@davidsimana.cz"):
    """Přidá logo/jméno do pravého dolního rohu."""
    font = get_font(FONT_BOLD, 28)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 40, H - 50), text, font=font, fill=(180, 140, 255, 200))

def add_slide_number(draw, current, total):
    """Číslo slidu v pravém horním rohu."""
    font = get_font(FONT_REGULAR, 26)
    text = f"{current}/{total}"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((W - tw - 40, 40), text, font=font, fill=(150, 120, 220))

def add_purple_dots_decoration(draw):
    """Dekorativní tečky v rohu."""
    for i in range(3):
        for j in range(3):
            alpha = 60 + (i + j) * 20
            draw.ellipse([W - 80 + i*20, 80 + j*20, W - 68 + i*20, 92 + j*20],
                        fill=(*BRAND_PURPLE, alpha))

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — HOOK
# ═══════════════════════════════════════════════════════════════════════════════
def slide_1():
    img = Image.new("RGB", (W, H))
    draw_gradient_bg(img, DARK_BG, (25, 10, 50))
    draw = ImageDraw.Draw(img)

    # Fialový dekorativní kruh v pozadí
    for r in range(400, 100, -50):
        alpha = max(5, 30 - (400 - r) // 15)
        draw.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r],
                    outline=(*BRAND_PURPLE, alpha), width=1)

    # Top accent linka
    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)

    # Číslo slidu
    add_slide_number(draw, 1, 6)

    # Hlavní hook text
    font_big = get_font(FONT_BLACK, 86)
    font_sub = get_font(FONT_BOLD, 42)
    font_small = get_font(FONT_REGULAR, 32)

    # "Státní příspěvek" — žlutě
    line1 = "Státní příspěvek"
    bbox = draw.textbbox((0, 0), line1, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 160), line1, font=font_sub, fill=YELLOW_ACCENT)

    # "zdarma?" — velké bílé
    line2 = "zdarma?"
    bbox = draw.textbbox((0, 0), line2, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 220), line2, font=font_big, fill=WHITE)

    # Oddělovač
    draw.rectangle([(W//2 - 60, 340), (W//2 + 60, 346)], fill=BRAND_PURPLE)

    # Podtitulek
    lines_sub = [
        "Myslíte si, že vám stát",
        "přidává peníze zadarmo.",
        "Přitom platíte víc,",
        "než dostáváte."
    ]
    y = 375
    for line in lines_sub:
        bbox = draw.textbbox((0, 0), line, font=font_small)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_small, fill=LIGHT_GRAY)
        y += 50

    # Bottom CTA box
    draw_rounded_rect(draw, [80, 680, W - 80, 780], radius=16,
                     fill=(142, 81, 255, 40), outline=BRAND_PURPLE, width=2)
    font_cta = get_font(FONT_BOLD, 34)
    cta = "Ukážu vám čísla, která vás překvapí"
    bbox = draw.textbbox((0, 0), cta, font=font_cta)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 715), cta, font=font_cta, fill=BRAND_PURPLE_L)

    # Šipka dolů
    arrow_x, arrow_y = W // 2, 840
    draw.polygon([
        (arrow_x - 20, arrow_y),
        (arrow_x + 20, arrow_y),
        (arrow_x, arrow_y + 30)
    ], fill=BRAND_PURPLE)

    # Logo
    add_logo_text(draw)

    img.save(os.path.join(OUT_DIR, "slide_01_hook.png"))
    print("✓ Slide 1 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — ILUZE vs REALITA
# ═══════════════════════════════════════════════════════════════════════════════
def slide_2():
    img = Image.new("RGB", (W, H))
    draw_gradient_bg(img, DARK_BG, (20, 8, 40))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)
    add_slide_number(draw, 2, 6)

    font_title = get_font(FONT_BLACK, 58)
    font_label = get_font(FONT_BOLD, 36)
    font_body  = get_font(FONT_REGULAR, 30)
    font_num   = get_font(FONT_BLACK, 72)

    # Nadpis
    title = "Co vidíte vs. co se děje"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 60), title, font=font_title, fill=WHITE)

    # Levý sloupec — ILUZE
    col_left = 60
    col_right = W // 2 + 30
    col_w = W // 2 - 90

    # Levá karta — zelená (iluze)
    draw_rounded_rect(draw, [col_left, 160, col_left + col_w, 500],
                     radius=20, fill=(20, 60, 30), outline=(60, 180, 80), width=2)
    label_l = "Co si myslíte"
    bbox = draw.textbbox((0, 0), label_l, font=font_label)
    tw = bbox[2] - bbox[0]
    draw.text((col_left + (col_w - tw) // 2, 185), label_l, font=font_label, fill=(80, 220, 100))

    draw.text((col_left + 30, 260), "+340 Kč", font=font_num, fill=(80, 220, 100))
    draw.text((col_left + 30, 350), "od státu každý", font=font_body, fill=LIGHT_GRAY)
    draw.text((col_left + 30, 390), "měsíc zdarma", font=font_body, fill=LIGHT_GRAY)

    # Pravá karta — červená (realita)
    draw_rounded_rect(draw, [col_right, 160, col_right + col_w, 500],
                     radius=20, fill=(60, 15, 15), outline=(220, 60, 60), width=2)
    label_r = "Co se děje"
    bbox = draw.textbbox((0, 0), label_r, font=font_label)
    tw = bbox[2] - bbox[0]
    draw.text((col_right + (col_w - tw) // 2, 185), label_r, font=font_label, fill=(220, 80, 80))

    draw.text((col_right + 20, 260), "−49 %", font=font_num, fill=(255, 80, 80))
    draw.text((col_right + 20, 350), "výnosů sežerou", font=font_body, fill=LIGHT_GRAY)
    draw.text((col_right + 20, 390), "poplatky za 10 let", font=font_body, fill=LIGHT_GRAY)

    # VS badge uprostřed
    draw.ellipse([W//2 - 36, 300, W//2 + 36, 372], fill=BRAND_PURPLE)
    font_vs = get_font(FONT_BLACK, 32)
    draw.text((W//2 - 20, 318), "VS", font=font_vs, fill=WHITE)

    # Spodní text
    draw.rectangle([(80, 530), (W - 80, 532)], fill=(80, 50, 140))
    font_bottom = get_font(FONT_BOLD, 34)
    lines = [
        "Penzijní společnosti mají jistý zisk.",
        "Vy nesete 100 % rizika."
    ]
    y = 560
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_bottom)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), line, font=font_bottom, fill=WHITE)
        y += 55

    # Bottom highlight box
    draw_rounded_rect(draw, [80, 700, W - 80, 800], radius=16,
                     fill=(50, 20, 100), outline=BRAND_PURPLE, width=2)
    font_hl = get_font(FONT_BOLD, 32)
    hl = "Státní příspěvek je past na poplatky"
    bbox = draw.textbbox((0, 0), hl, font=font_hl)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 735), hl, font=font_hl, fill=YELLOW_ACCENT)

    add_logo_text(draw)
    img.save(os.path.join(OUT_DIR, "slide_02_iluze_vs_realita.png"))
    print("✓ Slide 2 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — POPLATKY ŽEROU VÝNOSY (srovnání fondů)
# ═══════════════════════════════════════════════════════════════════════════════
def slide_3():
    img = Image.new("RGB", (W, H))
    draw_gradient_bg(img, DARK_BG, (15, 5, 35))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)
    add_slide_number(draw, 3, 6)

    font_title  = get_font(FONT_BLACK, 52)
    font_sub    = get_font(FONT_BOLD, 28)
    font_label  = get_font(FONT_BOLD, 30)
    font_num    = get_font(FONT_BLACK, 44)
    font_small  = get_font(FONT_REGULAR, 24)

    # Nadpis
    title = "O kolik přijdete kvůli poplatkům"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 55), title, font=font_title, fill=WHITE)

    sub = "za 10 let spoření (bez státních příspěvků)"
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 120), sub, font=font_sub, fill=LIGHT_GRAY)

    # Data: fondy a ztráty
    data = [
        ("🇨🇿 Staré penzijní fondy",   "-49 %", (220, 50, 50),  0.98),
        ("🇨🇿 Vyvážené fondy (DPS)",    "-42 %", (220, 80, 50),  0.84),
        ("🇨🇿 Dynamické fondy (DPS)",   "-37 %", (220, 120, 50), 0.74),
        ("🇸🇰 Slovenské indexové fondy","-7 %",  (80, 180, 80),  0.14),
        ("🇸🇪 Švédský AP7",             "-1 %",  (60, 200, 120), 0.02),
    ]

    bar_x = 60
    bar_y = 185
    bar_h = 100
    bar_gap = 20
    bar_max_w = W - 120

    for i, (label, value, color, ratio) in enumerate(data):
        y = bar_y + i * (bar_h + bar_gap)

        # Pozadí baru
        draw_rounded_rect(draw, [bar_x, y, bar_x + bar_max_w, y + bar_h],
                         radius=12, fill=(30, 20, 50))

        # Výplň baru (proporcionální)
        fill_w = int(bar_max_w * ratio)
        if fill_w > 24:
            draw_rounded_rect(draw, [bar_x, y, bar_x + fill_w, y + bar_h],
                             radius=12, fill=(*color, 180))

        # Label
        draw.text((bar_x + 20, y + 14), label, font=font_label, fill=WHITE)

        # Číslo
        bbox = draw.textbbox((0, 0), value, font=font_num)
        tw = bbox[2] - bbox[0]
        draw.text((bar_x + bar_max_w - tw - 20, y + 22), value, font=font_num, fill=color)

    # Spodní závěr
    y_bottom = bar_y + len(data) * (bar_h + bar_gap) + 20
    draw.rectangle([(60, y_bottom), (W - 60, y_bottom + 2)], fill=BRAND_PURPLE)

    font_concl = get_font(FONT_BLACK, 40)
    lines_c = ["Česká penzijka jsou", "nejdražší v porovnání"]
    y_c = y_bottom + 20
    for line in lines_c:
        bbox = draw.textbbox((0, 0), line, font=font_concl)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_c), line, font=font_concl, fill=WHITE)
        y_c += 55

    src = "Zdroj: IDEA CERGE-EI, Studie 01/2026"
    bbox = draw.textbbox((0, 0), src, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 55), src, font=font_small, fill=(100, 80, 150))

    add_logo_text(draw)
    img.save(os.path.join(OUT_DIR, "slide_03_poplatky_srovnani.png"))
    print("✓ Slide 3 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — KOLIK MUSÍTE SPOŘIT (srovnání měsíčních úspor)
# ═══════════════════════════════════════════════════════════════════════════════
def slide_4():
    img = Image.new("RGB", (W, H))
    draw_gradient_bg(img, DARK_BG, (20, 8, 45))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)
    add_slide_number(draw, 4, 6)

    font_title = get_font(FONT_BLACK, 50)
    font_sub   = get_font(FONT_BOLD, 28)
    font_label = get_font(FONT_BOLD, 28)
    font_num   = get_font(FONT_BLACK, 52)
    font_small = get_font(FONT_REGULAR, 24)

    # Nadpis
    title = "Kolik spořit na rentu 10 000 Kč/měs."
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 55), title, font=font_title, fill=WHITE)

    sub = "na 20 let — měsíční vklad"
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 120), sub, font=font_sub, fill=LIGHT_GRAY)

    # Data
    savings_data = [
        ("🇨🇿 Staré + nové fondy", "5 550 Kč", (220, 50, 50),  1.0),
        ("🇨🇿 Nové penzijní fondy","4 010 Kč", (220, 100, 50), 0.72),
        ("🇨🇿 Dynamické fondy",    "1 400 Kč", (220, 160, 50), 0.25),
        ("🇸🇰 Slovenské indexové", "  410 Kč", (80, 180, 80),  0.074),
        ("🇸🇪 Švédský AP7",        "  260 Kč", (60, 200, 120), 0.047),
    ]

    bar_x = 60
    bar_y = 180
    bar_h = 108
    bar_gap = 16
    bar_max_w = W - 120

    for i, (label, value, color, ratio) in enumerate(savings_data):
        y = bar_y + i * (bar_h + bar_gap)

        # Pozadí
        draw_rounded_rect(draw, [bar_x, y, bar_x + bar_max_w, y + bar_h],
                         radius=12, fill=(28, 18, 48))

        # Výplň
        fill_w = max(24, int(bar_max_w * ratio))
        draw_rounded_rect(draw, [bar_x, y, bar_x + fill_w, y + bar_h],
                         radius=12, fill=(*color, 160))

        # Label
        draw.text((bar_x + 18, y + 14), label, font=font_label, fill=WHITE)

        # Číslo
        bbox = draw.textbbox((0, 0), value, font=font_num)
        tw = bbox[2] - bbox[0]
        draw.text((bar_x + bar_max_w - tw - 18, y + 24), value, font=font_num, fill=color)

    # Závěr
    y_bottom = bar_y + len(savings_data) * (bar_h + bar_gap) + 15
    draw_rounded_rect(draw, [60, y_bottom, W - 60, y_bottom + 90],
                     radius=16, fill=(60, 20, 120), outline=BRAND_PURPLE, width=2)

    font_concl = get_font(FONT_BLACK, 36)
    line1 = "Spořit 21× více než Švédsko?"
    bbox = draw.textbbox((0, 0), line1, font=font_concl)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_bottom + 15), line1, font=font_concl, fill=YELLOW_ACCENT)

    line2 = "Tohle je cena vysokých poplatků."
    bbox = draw.textbbox((0, 0), line2, font=font_concl)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_bottom + 55), line2, font=font_concl, fill=WHITE)

    src = "Zdroj: IDEA CERGE-EI, Studie 01/2026"
    bbox = draw.textbbox((0, 0), src, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 55), src, font=font_small, fill=(100, 80, 150))

    add_logo_text(draw)
    img.save(os.path.join(OUT_DIR, "slide_04_mesicni_uspora.png"))
    print("✓ Slide 4 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — VÝKONNOST ZA 10 LET
# ═══════════════════════════════════════════════════════════════════════════════
def slide_5():
    img = Image.new("RGB", (W, H))
    draw_gradient_bg(img, DARK_BG, (18, 6, 40))
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)
    add_slide_number(draw, 5, 6)

    font_title = get_font(FONT_BLACK, 52)
    font_sub   = get_font(FONT_BOLD, 28)
    font_label = get_font(FONT_BOLD, 28)
    font_num   = get_font(FONT_BLACK, 56)
    font_small = get_font(FONT_REGULAR, 24)
    font_body  = get_font(FONT_REGULAR, 28)

    # Nadpis
    title = "Kumulovaná výkonnost za 10 let"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 55), title, font=font_title, fill=WHITE)

    # Bar chart data
    perf_data = [
        ("🇨🇿 Staré + nové fondy", "18 %",  (180, 60, 60),  0.079),
        ("🇨🇿 Nové fondy (DPS)",   "33 %",  (200, 100, 50), 0.144),
        ("🇨🇿 Dynamické fondy",    "88 %",  (220, 160, 50), 0.384),
        ("🇸🇰 Slovenské indexové", "172 %", (80, 180, 80),  0.750),
        ("🇸🇪 Švédský AP7",        "229 %", (60, 200, 120), 1.0),
    ]

    # Svislý bar chart
    chart_x = 80
    chart_y_bottom = 820
    chart_h = 480
    bar_w = 140
    bar_gap = 60
    total_bars = len(perf_data)
    total_w = total_bars * bar_w + (total_bars - 1) * bar_gap
    start_x = (W - total_w) // 2

    # Inflace linka (cca 88% = dynamické fondy)
    infl_y = chart_y_bottom - int(chart_h * 0.384)
    draw.line([(chart_x - 20, infl_y), (W - chart_x + 20, infl_y)],
              fill=(255, 80, 80), width=2)
    font_infl = get_font(FONT_BOLD, 22)
    draw.text((W - 180, infl_y - 28), "inflace", font=font_infl, fill=(255, 80, 80))

    for i, (label, value, color, ratio) in enumerate(perf_data):
        bx = start_x + i * (bar_w + bar_gap)
        bar_height = int(chart_h * ratio)
        by_top = chart_y_bottom - bar_height

        # Bar
        draw_rounded_rect(draw, [bx, by_top, bx + bar_w, chart_y_bottom],
                         radius=10, fill=color)

        # Číslo nad barem
        bbox = draw.textbbox((0, 0), value, font=font_num)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (bar_w - tw) // 2, by_top - 60), value, font=font_num, fill=color)

        # Label pod barem (dvouřádkový)
        parts = label.split(" ", 1)
        flag = parts[0]
        name = parts[1] if len(parts) > 1 else ""
        # Zalamování
        name_lines = []
        words = name.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            bbox_t = draw.textbbox((0, 0), test, font=font_small)
            if bbox_t[2] - bbox_t[0] <= bar_w + 10:
                cur = test
            else:
                if cur:
                    name_lines.append(cur)
                cur = w
        if cur:
            name_lines.append(cur)

        # Flag
        bbox = draw.textbbox((0, 0), flag, font=font_label)
        fw = bbox[2] - bbox[0]
        draw.text((bx + (bar_w - fw) // 2, chart_y_bottom + 10), flag, font=font_label, fill=WHITE)
        # Name lines
        ly = chart_y_bottom + 50
        for nl in name_lines:
            bbox = draw.textbbox((0, 0), nl, font=font_small)
            nlw = bbox[2] - bbox[0]
            draw.text((bx + (bar_w - nlw) // 2, ly), nl, font=font_small, fill=LIGHT_GRAY)
            ly += 28

    # Závěr
    font_concl = get_font(FONT_BLACK, 36)
    line1 = "Nové fondy: jen 2,7 % ročně."
    line2 = "Inflace to smazala."
    bbox = draw.textbbox((0, 0), line1, font=font_concl)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 140), line1, font=font_concl, fill=YELLOW_ACCENT)
    bbox = draw.textbbox((0, 0), line2, font=font_concl)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 185), line2, font=font_concl, fill=LIGHT_GRAY)

    src = "Zdroj: IDEA CERGE-EI, Studie 01/2026"
    bbox = draw.textbbox((0, 0), src, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 30), src, font=font_small, fill=(100, 80, 150))

    add_logo_text(draw)
    img.save(os.path.join(OUT_DIR, "slide_05_vykonnost.png"))
    print("✓ Slide 5 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — CTA s Davidovou fotografií
# ═══════════════════════════════════════════════════════════════════════════════
def slide_6():
    # Načíst Davidovu fotku
    photo_path = os.path.join(OUT_DIR, "david_photo2.webp")
    photo = Image.open(photo_path).convert("RGBA")

    # Ořez na čtverec (střed)
    pw, ph = photo.size
    side = min(pw, ph)
    left = (pw - side) // 2
    top = max(0, (ph - side) // 3)  # trochu výš pro obličej
    photo = photo.crop((left, top, left + side, top + side))
    photo = photo.resize((W, H), Image.LANCZOS)

    # Tmavý overlay
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    # Gradient overlay — spodní polovina tmavší
    for y in range(H):
        ratio = y / H
        alpha = int(120 + ratio * 120)
        draw_ov.line([(0, y), (W, y)], fill=(10, 5, 25, alpha))

    # Fialový overlay nahoře
    for y in range(200):
        alpha = int(160 * (1 - y / 200))
        draw_ov.line([(0, y), (W, y)], fill=(*BRAND_PURPLE_D, alpha))

    img = Image.alpha_composite(photo, overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top accent linka
    draw.rectangle([0, 0, W, 6], fill=BRAND_PURPLE)
    add_slide_number(draw, 6, 6)

    font_big   = get_font(FONT_BLACK, 62)
    font_med   = get_font(FONT_BOLD, 36)
    font_small = get_font(FONT_REGULAR, 28)
    font_cta   = get_font(FONT_BLACK, 40)
    font_name  = get_font(FONT_BOLD, 32)

    # Jméno + titul nahoře
    draw.text((60, 50), "David Šimana", font=font_name, fill=WHITE)
    draw.text((60, 90), "Finanční poradce | Fin2u", font=font_small, fill=BRAND_PURPLE_L)

    # Hlavní message — spodní část
    y_start = 560

    # Box pro text
    draw_rounded_rect(draw, [40, y_start - 20, W - 40, H - 40],
                     radius=20, fill=(10, 5, 25, 200))

    line1 = "Penzijko vás okrádá."
    bbox = draw.textbbox((0, 0), line1, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_start), line1, font=font_big, fill=WHITE)

    line2 = "Existuje lepší cesta."
    bbox = draw.textbbox((0, 0), line2, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y_start + 75), line2, font=font_big, fill=BRAND_PURPLE_L)

    # Oddělovač
    draw.rectangle([(W//2 - 80, y_start + 155), (W//2 + 80, y_start + 159)], fill=BRAND_PURPLE)

    # CTA text
    cta_lines = [
        "Napište mi slovo  DŮCHOD",
        "a ukážu vám, jak spořit",
        "bez nesmyslných poplatků."
    ]
    y_cta = y_start + 175
    for line in cta_lines:
        bbox = draw.textbbox((0, 0), line, font=font_med)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y_cta), line, font=font_med, fill=LIGHT_GRAY)
        y_cta += 50

    # CTA button
    btn_y = y_cta + 15
    draw_rounded_rect(draw, [W//2 - 220, btn_y, W//2 + 220, btn_y + 70],
                     radius=35, fill=BRAND_PURPLE)
    btn_text = "Uložte si tento post"
    bbox = draw.textbbox((0, 0), btn_text, font=font_cta)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, btn_y + 12), btn_text, font=font_cta, fill=WHITE)

    img.save(os.path.join(OUT_DIR, "slide_06_cta_david.png"))
    print("✓ Slide 6 saved")

# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generuji carousel slidy...")
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    print(f"\n✅ Všech 6 slidů uloženo do: {OUT_DIR}")
