#!/usr/bin/env python3
"""Renderiza a capa do ebook em estilo tipografico minimalista (ref: @yourdivorcebestfriend).
Texto perfeito em portugues, fundo creme, serifa elegante. Saida em alta resolucao."""
from PIL import Image, ImageDraw, ImageFont

# ---- Paleta (simplificada para o estilo minimal) ----
CREAM   = (244, 240, 232)   # fundo creme quente, quase branco
INK     = (43, 43, 43)      # grafite (texto)
MUTED   = (122, 122, 116)   # cinza quente (kicker / subtitulo)
ACCENT  = (192, 115, 79)    # terracota (acento unico)

W, H = 1600, 2400  # capa retrato 2:3, alta resolucao

SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_R  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def text_w(draw, s, fnt, tracking=0):
    if tracking == 0:
        return draw.textlength(s, font=fnt)
    return sum(draw.textlength(c, font=fnt) for c in s) + tracking * max(len(s) - 1, 0)

def draw_centered(draw, y, s, fnt, fill, tracking=0):
    total = text_w(draw, s, fnt, tracking)
    x = (W - total) / 2
    if tracking == 0:
        draw.text((x, y), s, font=fnt, fill=fill)
    else:
        for c in s:
            draw.text((x, y), c, font=fnt, fill=fill)
            x += draw.textlength(c, font=fnt) + tracking

def wrap(draw, words, fnt, max_w):
    lines, cur = [], ""
    for w in words.split():
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def line_height(fnt):
    a = fnt.getmetrics()
    return a[0] + a[1]

def make_cover(path, kicker, title, subtitle, author, rule=True):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    margin = 150
    max_w = W - 2 * margin

    # Kicker (topo, caixa alta, espacado)
    fk = font(SANS_R, 34)
    draw_centered(d, 300, kicker.upper(), fk, MUTED, tracking=10)

    # Acento: traco curto sob o kicker
    if rule:
        rw = 90
        d.line([( (W-rw)/2, 380), ((W+rw)/2, 380)], fill=ACCENT, width=4)

    # Titulo (serifa grande, centralizado, com quebra)
    ft = font(SERIF_B, 150)
    tlines = wrap(d, title, ft, max_w)
    lh = int(line_height(ft) * 0.98)
    block_h = lh * len(tlines)
    ty = 880 - block_h / 2
    for ln in tlines:
        draw_centered(d, ty, ln, ft, INK)
        ty += lh

    # Subtitulo (italico serifa, menor, cinza)
    fs = font(SERIF_I, 58)
    slines = wrap(d, subtitle, fs, max_w - 120)
    slh = int(line_height(fs) * 1.12)
    sy = max(ty + 80, 1180)
    for ln in slines:
        draw_centered(d, sy, ln, fs, MUTED)
        sy += slh

    # Autor (rodape)
    if author:
        fa = font(SANS_R, 36)
        draw_centered(d, H - 320, author.upper(), fa, INK, tracking=8)

    img.save(path, "PNG")
    return path

if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out, exist_ok=True)

    # Variacao A: titulo principal
    make_cover(
        os.path.join(out, "capa-v1.png"),
        kicker="Guia prático · 6 semanas",
        title="Depois da Traição",
        subtitle="Como reconstruir a confiança sem se forçar a perdoar",
        author="Dani Hayoshi",
    )

    # Variacao B: subtitulo completo, sem traco
    make_cover(
        os.path.join(out, "capa-v2.png"),
        kicker="Reconstrução da confiança",
        title="Depois da Traição",
        subtitle="O plano de 6 semanas para reconstruir a confiança sem se forçar a perdoar",
        author="Dani Hayoshi",
        rule=False,
    )
    print("ok")
