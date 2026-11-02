#!/usr/bin/env python3
"""Render original SVG artwork to WebP/PNG/ICO assets. Usage: python3 tools/make_images.py

TEMPLATE NOTICE — read before reusing on a new game/brand:
1. Colors: EVERY hex constant in the CONFIG block below is the
   chickenroad.radio.am placeholder palette, not just the first few. Finish
   references/brand-design-research.md first, then replace all of them with
   the real game/provider's researched colors before rendering a single
   asset. Check the rendered output too: this script also draws the
   favicon/logo and the og image, so a half-swapped palette ships a
   wrong-colored social card.
0. Game name: set GAME_TITLE / GAME_TITLE_L1 / GAME_TITLE_L2 / EDITION_LABEL
   below. They are burned into the logo, mascot and og artwork as text, so
   leaving them unset ships another game's name on this site's social card.
2. Subject matter: hen()/egg()/board() draw an ORIGINAL (not copied) cartoon
   hen and egg because the first site this skill shipped was about a
   hen-crossing-lanes game. That subject is specific to THAT game, not to
   this skill. For a different crash/instant-win game (a plane for Aviator,
   an ice hole/fish for Ice Fishing, etc.), write new helper function(s) for
   an original illustration of THAT game's actual theme — keep the
   board()/lane/multiplier rendering technique (it is generic), but swap the
   character art to match what the game you are covering is actually about.
   Never copy the provider's real character art/screenshots; draw an
   original illustration inspired by the theme, in the researched brand
   colors.
"""
import os, io
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)

# ---- CONFIG (replace every value for a new site: see the TEMPLATE NOTICE above) ----
GAME_TITLE = 'CHICKEN ROAD'      # one-line title, used on the gameplay/sequel boards
GAME_TITLE_L1 = 'CHICKEN'        # og image, first line
GAME_TITLE_L2 = 'ROAD'           # og image, second line
EDITION_LABEL = '2026 EDITION'   # og image strip

# Brand palette (from brand-design-research.md), then supporting theme colors
PRIMARY = '#14213d'; PRIMARY2 = '#1f2f52'; ACCENT = '#ffc107'; ACCENT_DARK = '#ffb000'; ACCENT2 = '#e63946'; SURFACE_DARK = '#2b2d42'
CREAM = '#fff8e7'            # light neutral
CANVAS_SOFT = '#ffe8a3'      # mascot/figure canvas wash (accent-derived)
GRASS = '#9bd17a'            # ground band
SKY = '#bfe3ff'              # sky band
ACCENT_STROKE = '#e09b00'    # outline for accent-filled shapes
BOARD_LANE = '#3a3f5c'; BOARD_TILE = '#5c6178'; BOARD_EDGE = '#8a90aa'; BOARD_DEEP = '#24345a'
TEXT_SOFT = '#c9d2e8'        # muted text on dark artwork
# ------------------------------------------------------------------------------------


def hen(x, y, s=1.0, flip=False):
    """Original generic cartoon hen, origin at feet centre."""
    t = f'translate({x},{y}) scale({-s if flip else s},{s})'
    return f'''<g transform="{t}">
  <ellipse cx="0" cy="4" rx="46" ry="9" fill="#000" opacity=".18"/>
  <path d="M-14 -6 L-18 4 M-18 4 L-26 6 M-18 4 L-12 7" stroke="{ACCENT_DARK}" stroke-width="5" stroke-linecap="round" fill="none"/>
  <path d="M10 -6 L8 4 M8 4 L0 6 M8 4 L15 7" stroke="{ACCENT_DARK}" stroke-width="5" stroke-linecap="round" fill="none"/>
  <path d="M-52 -60 Q-70 -78 -58 -96 Q-48 -84 -40 -82 Z" fill="#f1f1f1" stroke="#d9d9d9" stroke-width="2"/>
  <ellipse cx="-4" cy="-42" rx="50" ry="40" fill="#fff" stroke="#e3e3e3" stroke-width="2"/>
  <path d="M-30 -48 Q-8 -30 18 -44 Q2 -20 -24 -28 Z" fill="#ececec"/>
  <circle cx="30" cy="-86" r="27" fill="#fff" stroke="#e3e3e3" stroke-width="2"/>
  <path d="M14 -110 Q18 -126 26 -112 Q32 -128 38 -112 Q46 -124 46 -106 Q30 -102 14 -110 Z" fill="{ACCENT2}"/>
  <path d="M52 -90 L70 -84 L52 -78 Z" fill="{ACCENT_DARK}"/>
  <path d="M50 -76 Q56 -64 48 -60 Q42 -66 46 -76 Z" fill="{ACCENT2}"/>
  <circle cx="38" cy="-92" r="5.5" fill="{PRIMARY}"/><circle cx="39.8" cy="-94" r="1.8" fill="#fff"/>
  <circle cx="26" cy="-78" r="5" fill="#ffb3b3" opacity=".6"/>
</g>'''


def egg(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
  <ellipse cx="0" cy="34" rx="34" ry="7" fill="#000" opacity=".2"/>
  <path d="M0 -40 C 24 -40 34 0 34 10 C 34 28 18 38 0 38 C -18 38 -34 28 -34 10 C -34 0 -24 -40 0 -40 Z" fill="{ACCENT}" stroke="{ACCENT_STROKE}" stroke-width="3"/>
  <ellipse cx="-11" cy="-10" rx="7" ry="13" fill="#fff" opacity=".55" transform="rotate(20 -11 -10)"/>
</g>'''


def board(w, h, lanes, mults, badge=None, title=None):
    top, bottom = 150, h - 70
    start_w = 190
    lane_w = (w - start_w - 150) / lanes
    parts = [f'<rect width="{w}" height="{h}" fill="{PRIMARY}"/>',
             f'<rect x="0" y="{top-20}" width="{w}" height="{bottom-top+40}" fill="{SURFACE_DARK}"/>',
             f'<rect x="0" y="{top-20}" width="{start_w}" height="{bottom-top+40}" fill="{BOARD_LANE}"/>']
    for i in range(lanes):
        lx = start_w + i * lane_w
        parts.append(f'<line x1="{lx:.1f}" y1="{top-20}" x2="{lx:.1f}" y2="{bottom+20}" stroke="#fff" stroke-width="4" stroke-dasharray="22 18" opacity=".55"/>')
        cx = lx + lane_w / 2
        cy = (top + bottom) / 2 + 10
        r = min(lane_w * 0.36, 46)
        parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r*0.62:.1f}" fill="{BOARD_TILE}" stroke="{BOARD_EDGE}" stroke-width="3"/>')
        parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r*0.62:.1f}" ry="{r*0.36:.1f}" fill="none" stroke="{BOARD_EDGE}" stroke-width="2"/>')
        if i < len(mults):
            fs = 22 if lane_w > 95 else 17
            tw = fs * 0.62 * len(mults[i]) + 18
            hl = i == 2
            parts.append(f'<rect x="{cx-tw/2:.1f}" y="{top-6}" width="{tw:.1f}" height="{fs+16}" rx="{(fs+16)/2:.1f}" fill="{ACCENT if hl else "#ffffff"}" opacity="{1 if hl else .92}"/>')
            parts.append(f'<text x="{cx:.1f}" y="{top+fs+2}" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="{fs}" text-anchor="middle" fill="{PRIMARY}">{mults[i]}</text>')
    # end zone with egg
    parts.append(f'<rect x="{w-150}" y="{top-20}" width="150" height="{bottom-top+40}" fill="{BOARD_DEEP}"/>')
    parts.append(egg(w - 75, (top + bottom) / 2 + 6, 1.15))
    # hen on start (next to lane 3 highlight -> hen stands after 2 safe steps)
    hx = start_w + lane_w * 2.5
    parts.append(hen(hx, bottom - 18, 0.95 if lane_w > 95 else 0.8))
    # cars hint at lane 5
    if lanes > 4:
        cx = start_w + lane_w * 4.5
        parts.append(f'<g transform="translate({cx-30:.1f},{bottom-110})"><rect width="60" height="96" rx="14" fill="{ACCENT2}"/><rect x="8" y="14" width="44" height="22" rx="5" fill="{SKY}"/><rect x="8" y="62" width="44" height="18" rx="5" fill="{SKY}"/></g>')
    # header
    t = title or GAME_TITLE
    parts.append(f'<text x="40" y="78" font-family="Arial Black,Arial,Helvetica,sans-serif" font-weight="900" font-size="46" fill="{ACCENT}" letter-spacing="2">{t}</text>')
    parts.append(f'<text x="42" y="112" font-family="Arial,Helvetica,sans-serif" font-size="22" fill="{TEXT_SOFT}">Illustration: each safe lane raises the multiplier</text>')
    # difficulty pills
    px = w - 520
    for j, lab in enumerate(['EASY', 'MEDIUM', 'HARD', 'HARDCORE']):
        pw = 92 if lab != 'HARDCORE' else 128
        on = j == 1
        parts.append(f'<rect x="{px}" y="46" width="{pw}" height="40" rx="20" fill="{ACCENT if on else "none"}" stroke="{ACCENT}" stroke-width="2"/>')
        parts.append(f'<text x="{px+pw/2}" y="72" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="16" text-anchor="middle" fill="{PRIMARY if on else ACCENT}">{lab}</text>')
        px += pw + 10
    # cash out button
    parts.append(f'<rect x="{w-330}" y="{h-58}" width="290" height="46" rx="23" fill="{ACCENT2}"/>')
    parts.append(f'<text x="{w-185}" y="{h-27}" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="22" text-anchor="middle" fill="#fff">CASH OUT</text>')
    parts.append(f'<rect x="40" y="{h-58}" width="230" height="46" rx="23" fill="none" stroke="{TEXT_SOFT}" stroke-width="2"/>')
    parts.append(f'<text x="155" y="{h-27}" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="20" text-anchor="middle" fill="{TEXT_SOFT}">GO / NEXT LANE</text>')
    if badge:
        parts.append(f'<g transform="translate({w-140},{h-130}) rotate(-12)"><circle r="0" /></g>')
        parts.append(f'<g transform="translate(520,58)"><rect x="0" y="-30" width="96" height="46" rx="12" fill="{ACCENT2}"/><text x="48" y="2" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="28" text-anchor="middle" fill="#fff">{badge}</text></g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + ''.join(parts) + '</svg>'


def logo_svg(size=512):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">
<defs><clipPath id="c"><rect width="512" height="512" rx="112"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="512" height="512" fill="{PRIMARY}"/>
<rect x="0" y="372" width="512" height="140" fill="{SURFACE_DARK}"/></g>
<g stroke="{ACCENT}" stroke-width="12" stroke-dasharray="44 30"><line x1="20" y1="446" x2="492" y2="446"/></g>
<g transform="translate(232,372) scale(2.6)">
  <path d="M-52 -60 Q-70 -78 -58 -96 Q-48 -84 -40 -82 Z" fill="#f1f1f1"/>
  <ellipse cx="-4" cy="-42" rx="50" ry="40" fill="#fff"/>
  <path d="M-30 -48 Q-8 -30 18 -44 Q2 -20 -24 -28 Z" fill="#e6e6e6"/>
  <circle cx="30" cy="-86" r="27" fill="#fff"/>
  <path d="M14 -110 Q18 -126 26 -112 Q32 -128 38 -112 Q46 -124 46 -106 Q30 -102 14 -110 Z" fill="{ACCENT2}"/>
  <path d="M52 -90 L70 -84 L52 -78 Z" fill="{ACCENT_DARK}"/>
  <path d="M50 -76 Q56 -64 48 -60 Q42 -66 46 -76 Z" fill="{ACCENT2}"/>
  <circle cx="38" cy="-92" r="5.5" fill="{PRIMARY}"/><circle cx="39.8" cy="-94" r="1.8" fill="#fff"/>
</g>
</svg>'''


def mascot_svg():
    w, h = 1200, 900
    p = [f'<rect width="{w}" height="{h}" fill="{CANVAS_SOFT}"/>',
         f'<circle cx="980" cy="170" r="110" fill="{ACCENT}" opacity=".9"/>',
         f'<path d="M0 520 Q300 470 600 520 T1200 520 V900 H0 Z" fill="{GRASS}"/>',
         f'<path d="M-50 900 L420 470 L780 470 L1250 900 Z" fill="{SURFACE_DARK}"/>',
         f'<path d="M600 480 L600 900" stroke="{ACCENT}" stroke-width="14" stroke-dasharray="60 46"/>',
         f'<path d="M420 470 L-50 900 M780 470 L1250 900" stroke="#fff" stroke-width="8" opacity=".7"/>',
         f'<text x="150" y="480" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="300" fill="{ACCENT2}" opacity=".92">2</text>',
         hen(640, 820, 2.6),
         egg(1040, 760, 1.6),
         f'<text x="60" y="110" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="70" fill="{PRIMARY}">{GAME_TITLE}</text>',
         f'<text x="64" y="160" font-family="Arial,Helvetica,sans-serif" font-size="30" fill="{PRIMARY}">Original artwork, not game footage</text>']
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + ''.join(p) + '</svg>'


def og_svg():
    w, h = 1200, 630
    p = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PRIMARY}"/><stop offset="1" stop-color="{PRIMARY2}"/></linearGradient></defs>',
         f'<rect width="{w}" height="{h}" fill="url(#g)"/>',
         f'<rect x="0" y="470" width="{w}" height="160" fill="{SURFACE_DARK}"/>',
         f'<line x1="0" y1="550" x2="{w}" y2="550" stroke="{ACCENT}" stroke-width="12" stroke-dasharray="60 40"/>',
         f'<text x="70" y="190" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="104" fill="{ACCENT}">{GAME_TITLE_L1}</text>',
         f'<text x="70" y="300" font-family="Arial Black,Arial,sans-serif" font-weight="900" font-size="104" fill="#fff">{GAME_TITLE_L2}</text>',
         f'<text x="74" y="370" font-family="Arial,Helvetica,sans-serif" font-size="36" fill="{TEXT_SOFT}">How it works, if it pays, where to play</text>',
         f'<rect x="74" y="398" width="300" height="52" rx="26" fill="{ACCENT2}"/>',
         f'<text x="224" y="434" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="26" text-anchor="middle" fill="#fff">{EDITION_LABEL}</text>',
         hen(900, 520, 2.9), egg(1110, 520, 1.1)]
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + ''.join(p) + '</svg>'


def render(page, svg, w, h):
    page.set_viewport_size({'width': w, 'height': h})
    page.set_content(f'<html><body style="margin:0">{svg}</body></html>')
    return Image.open(io.BytesIO(page.screenshot(clip={'x': 0, 'y': 0, 'width': w, 'height': h}))).convert('RGB')


def save_webp(img, name, q=82):
    path = os.path.join(OUT, name)
    while True:
        img.save(path, 'WEBP', quality=q, method=6)
        if os.path.getsize(path) < 120_000 or q < 40:
            break
        q -= 8
    print(name, img.size, os.path.getsize(path))


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    logo = render(pg, logo_svg(), 512, 512)
    save_webp(logo, 'logo.webp')
    save_webp(render(pg, board(1200, 675, 6, ['x1.02', 'x1.08', 'x1.15', 'x1.24', 'x1.34', 'x1.46']), 1200, 675), 'gameplay.webp')
    save_webp(render(pg, mascot_svg(), 1200, 900), 'mascot.webp')
    save_webp(render(pg, board(1200, 675, 9, ['x1.01', 'x1.04', 'x1.08', 'x1.13', 'x1.18', 'x1.24', 'x1.30', 'x1.37', 'x1.45'], badge='2.0', title=GAME_TITLE), 1200, 675), 'sequel.webp')
    save_webp(render(pg, og_svg(), 1200, 630), 'og.webp')
    # icons: render logo bigger without rounded transparency issue
    pg.set_viewport_size({'width': 512, 'height': 512})
    pg.set_content(f'<html><body style="margin:0;background:transparent">{logo_svg()}</body></html>')
    rgba = Image.open(io.BytesIO(pg.screenshot(omit_background=True, clip={'x': 0, 'y': 0, 'width': 512, 'height': 512}))).convert('RGBA')
    rgba.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT, 'favicon-32.png'))
    logo.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, 'apple-touch-icon.png'))
    rgba.save(os.path.join(ROOT, 'assets', 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    b.close()
