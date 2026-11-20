"""Generate the Haru character reference sheet as a single SVG.

All parts are drawn in a shared "body space": crown of the head at y=0,
chin at y~113, soles at y=880, body centred on x=0 (~8 heads tall).
"""
from pathlib import Path

# ---------------------------------------------------------------- palette
LINE = "#2b2524"
LINE_SOFT = "#8c7f78"
SKIN = "#fdf1e8"
SKIN_SH = "#f1dacd"
BLUSH = "#f3b9ad"
LIP = "#d99a90"
HAIR = "#2d2b32"
HAIR_LINE = "#18161b"
HAIR_HI = "#6c6b78"
SHIRT = "#ffffff"
SHIRT_SH = "#ebe8e3"
CARD = "#e6d7bf"
CARD_SH = "#d2bf9f"
CARD_LINE = "#8f7a5c"
PANTS = "#d6d6d9"
PANTS_SH = "#c0c0c5"
SOCK = "#fbfbfb"
SOCK_SH = "#e7e7e7"
GUIDE = "#efebe5"
PANEL = "#e9e4dc"

S = f'stroke="{LINE}" stroke-linejoin="round" stroke-linecap="round"'


def p(d, fill, sw=1.6, stroke=LINE, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')


def ln(d, sw=1.0, stroke=LINE, op=1.0):
    return (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')


# ================================================================ EYES
# Small, heavy-lidded adult male eyes. Iris centre at (0,0); outer corner
# at x=-11 (viewer's left eye). The right eye is the mirror image.
EYES = {
    "open": dict(
        sclera="M -11 -1 Q -1 -6 10 -2 Q 7 4.5 0 5 Q -7 4.5 -11 -1 Z",
        lid="M -12.5 -0.5 Q -1 -7 11 -2.5", crease="M -10 -5 Q 0 -10 9 -6",
        lower="M -8 6 Q 0 7.5 7 5", iris=(0, 1), hl=True, bags=False),
    "calm": dict(
        sclera="M -11 0 Q -1 -3.5 10 -1 Q 7 4.5 0 5 Q -7 4.5 -11 0 Z",
        lid="M -12.5 0.5 Q -1 -4.5 11 -1.5", crease="M -10 -4 Q 0 -8 9 -5",
        lower="M -8 6 Q 0 7.5 7 5", iris=(0.3, 1.8), hl=True, bags=True),
    "up": dict(
        sclera="M -11 -1 Q -1 -6 10 -2 Q 7 4.5 0 5 Q -7 4.5 -11 -1 Z",
        lid="M -12.5 -0.5 Q -1 -7 11 -2.5", crease="M -10 -5 Q 0 -10 9 -6",
        lower="M -8 6 Q 0 7.5 7 5", iris=(2, -1.2), hl=True, bags=False),
    "worried": dict(
        sclera="M -11 -0.5 Q -2 -5.5 10 -3 Q 7 4.5 0 5 Q -7 4.5 -11 -0.5 Z",
        lid="M -12.5 0 Q -2 -6.5 11 -3.5", crease="M -10 -4 Q -2 -9.5 9 -7.5",
        lower="M -8 6 Q 0 7.5 7 5", iris=(-1, 1.2), hl=True, bags=True),
    "half": dict(
        sclera="M -11 1.5 Q -1 -0.5 10 0.5 Q 7 4.5 0 5 Q -7 4.5 -11 1.5 Z",
        lid="M -12.5 2 Q -1 -1.5 11 0", crease="M -10 -2.5 Q 0 -6 9 -3.5",
        lower="M -8 6 Q 0 7.5 7 5", iris=(-0.5, 3), hl=True, bags=True),
    "smile": dict(
        sclera="M -11 0 Q -1 -4 10 -1.5 Q 6 2.5 0 2.8 Q -6 2.5 -11 0 Z",
        lid="M -12.5 0.5 Q -1 -5 11 -2", crease="M -10 -4.5 Q 0 -8.5 9 -5.5",
        lower="M -9 3.8 Q 0 5.2 8 2.2", iris=(0, 0.8), hl=True, bags=False),
    "squint": dict(
        sclera="M -11 1 Q -1 -1 10 0 Q 6 2.5 0 2.8 Q -6 2.5 -11 1 Z",
        lid="M -12.5 1.5 Q -1 -2 11 -0.5", crease="M -10 -3 Q 0 -6 9 -3.5",
        lower="M -9 4 Q 0 4.8 8 3", iris=(-0.5, 1.5), hl=False, bags=False),
    "shut": dict(
        sclera=None, lid="M -11.5 0.5 Q -1 3.5 10.5 0.5", crease="M -10 -3.5 Q 0 -1.5 9 -3.5",
        lower="M -9 4 Q 0 5 8 3.5", iris=None, hl=False, bags=False),
}


def eye_defs():
    out = []
    for name, e in EYES.items():
        g = []
        if e["bags"]:  # tired shadow under the eye
            g.append('<path d="M -11 4 Q 0 12 10 3 Q 0 8.5 -11 4 Z" fill="#cdbdb6" opacity="0.55"/>')
        if e["sclera"]:
            out.append(f'<clipPath id="sc_{name}"><path d="{e["sclera"]}"/></clipPath>')
            g.append(p(e["sclera"], "#ffffff", 0.6, LINE_SOFT))
            ix, iy = e["iris"]
            g.append(f'<g clip-path="url(#sc_{name})">'
                     f'<path d="{e["lid"]} L 12 3 L -13 3 Z" fill="#e2e2e8" transform="translate(0,1.6)"/>'
                     f'<circle cx="{ix}" cy="{iy}" r="4.4" fill="url(#iris)" stroke="#232227" stroke-width="0.8"/>'
                     f'<circle cx="{ix}" cy="{iy + 0.3}" r="2.1" fill="#1d1c21"/>'
                     f'</g>')
        g.append(ln(e["crease"], 0.8, LINE, 0.5))
        g.append(ln(e["lid"], 2.2, "#221c1b"))
        g.append(ln(e["lower"], 0.8, LINE, 0.55))
        out.append(f'<g id="eye_{name}">{"".join(g)}</g>')
    return "".join(out)


EY = 70  # eye line


def eye_pair(left, right=None):
    right = right or left
    s = (f'<use href="#eye_{left}" transform="translate(-18,{EY})"/>'
         f'<use href="#eye_{right}" transform="translate(18,{EY}) scale(-1,1)"/>')
    for cx, name, mir in ((-18, left, 1), (18, right, -1)):
        e = EYES[name]
        if e["hl"]:
            ix, iy = e["iris"]
            s += f'<circle cx="{cx + ix * mir - 1.5}" cy="{EY + iy - 1.3}" r="1.1" fill="#fff"/>'
    return s


# ================================================================ HEAD (front)
# Longer adult face; chin at y=122 before the head is lifted by HEAD_LIFT.
HEAD_LIFT = -10
FACE = ("M -41 40 C -42 62 -40 80 -35 92 L -14 116 Q 0 123 14 116 L 35 92 "
        "C 40 80 42 62 41 40 C 38 0 -38 0 -41 40 Z")
BACK_HAIR = ("M -50 70 C -60 18 -42 -21 0 -21 C 42 -21 60 18 50 70 L 46 88 L 41 78 "
             "L 37 97 L 31 86 L -31 86 L -37 97 L -41 78 L -46 88 Z")
FRINGE = ("M -50 46 C -57 8 -36 -20 2 -20 C 40 -20 58 8 50 46 "
          "Q 57 56 49 60 Q 52 72 45 83 Q 42 70 38 64 Q 36 56 34 50 Q 32 60 30 66 "
          "Q 26 52 22 44 Q 20 54 15 62 Q 13 50 9 42 Q 6 56 2 69 "
          "Q -1 52 -4 42 Q -8 54 -13 62 Q -14 50 -19 44 Q -22 56 -28 66 "
          "Q -30 56 -33 50 Q -36 58 -38 64 Q -42 72 -45 83 Q -52 72 -49 60 "
          "Q -57 56 -50 46 Z")
FRINGE_TUFTS = ["M -8 -19 Q -2 -32 12 -30 Q 5 -25 8 -19 Z",
                "M 12 -18 Q 24 -28 34 -20 Q 26 -20 24 -14 Z",
                "M 48 24 Q 57 30 58 39 Q 53 35 49 37 Z",
                "M -48 26 Q -57 32 -57 41 Q -52 37 -49 39 Z",
                "M -30 -12 Q -40 -16 -45 -10 Q -40 -8 -37 -4 Z"]
FRINGE_STRANDS = [
    "M 4 -14 Q 1 30 2 66", "M 4 -14 Q 12 22 15 60", "M -4 -10 Q -10 22 -13 60",
    "M 12 -10 Q 26 20 30 63", "M -14 -6 Q -24 22 -28 63", "M 22 -6 Q 40 24 45 80",
    "M -24 -2 Q -40 24 -45 80", "M 0 -16 Q -6 10 -8 40", "M 18 -12 Q 24 10 22 40",
]
FRINGE_HI = [
    "M -30 4 Q -16 -6 -2 -6", "M 6 -7 Q 20 -6 32 4",
    "M -38 18 Q -36 12 -33 9", "M 36 10 Q 40 16 41 22",
]

BROWS = {  # left brow (viewer's left); right is mirrored
    "calm":    "M -31 58 Q -20 55.5 -8 57",
    "up":      "M -31 55 Q -20 51.5 -8 53.5",
    "worried": "M -31 59 Q -20 57 -9 52.5",
    "wince":   "M -31 55 Q -20 56 -9 61",
    "sad":     "M -31 60 Q -20 58 -9 54.5",
    "smile":   "M -31 57 Q -20 54 -8 56",
}

MY = 106  # mouth line
MOUTHS = {
    "calm": ln(f"M -6 {MY} L 6 {MY}", 1.3),
    "up": f'<ellipse cx="1" cy="{MY}" rx="2.6" ry="1.7" fill="{LIP}" stroke="{LINE}" stroke-width="0.9"/>',
    "worried": ln(f"M -6 {MY + .5} Q -3 {MY - 1.4} 0 {MY - .4} Q 3 {MY + .6} 6 {MY - 1}", 1.3),
    "wince": (f'<path d="M -8 {MY - 1} Q 0 {MY - 3.5} 8 {MY} Q 1 {MY + 2} -8 {MY - 1} Z" fill="#fff" '
              f'stroke="{LINE}" stroke-width="1.1" stroke-linejoin="round"/>'),
    "sad": ln(f"M -6 {MY + 1} Q 0 {MY - 1.5} 6 {MY + 1}", 1.3),
    "smile": ln(f"M -9 {MY - 2} Q 0 {MY + 3.5} 9 {MY - 2}", 1.4),
}


def mirror_path(d):
    res, i, toks = [], 0, d.split()
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            res.append(t)
            i += 1
            continue
        res.append(str(-float(toks[i])))
        res.append(toks[i + 1])
        i += 2
    return " ".join(res)


EAR = "M -40 58 C -52 52 -55 72 -49 84 C -47 90 -42 91 -39 85 Z"
EAR_IN = "M -43 64 Q -49 70 -46 80 Q -43 78 -43 74"


def head_front(expr="calm", eyes=None, extras=""):
    eyes = eyes or {"calm": ("calm",), "up": ("up",), "worried": ("worried",),
                    "wince": ("shut", "squint"), "sad": ("half",),
                    "smile": ("smile",)}[expr]
    brow = BROWS[expr]
    g = [p(BACK_HAIR, HAIR, 1.4, HAIR_LINE)]
    for sx in (1, -1):
        g.append(f'<g transform="scale({sx},1)">' + p(EAR, SKIN, 1.3)
                 + ln(EAR_IN, 0.9, LINE, 0.6) + "</g>")
    g.append(p(FACE, SKIN, 1.6))
    g.append(f'<g clip-path="url(#faceClip)">'
             f'<path d="M -46 30 L 46 30 L 46 54 Q 38 70 30 70 Q 22 64 15 66 Q 8 64 2 73 '
             f'Q -6 64 -13 66 Q -20 64 -28 70 Q -38 70 -46 54 Z" fill="{SKIN_SH}"/>'
             f'<path d="M -42 70 Q -40 84 -35 92 L -18 112 L -37 86 Z" fill="{SKIN_SH}" opacity="0.7"/>'
             f'</g>')
    g.append(eye_pair(*eyes))
    # nose: bridge line + shadowed side + nostril tick
    g.append(f'<path d="M 2 80 Q 4 89 5.5 93 L 2 94 Z" fill="{SKIN_SH}"/>')
    g.append(ln("M 1 78 Q 3 88 5.5 93 Q 3.5 95.5 0 95", 1.1, LINE, 0.8))
    g.append(MOUTHS[expr])
    if expr == "smile":
        for cx in (-25, 25):
            g.append(f'<ellipse cx="{cx}" cy="90" rx="7" ry="3" fill="{BLUSH}" opacity="0.2"/>')
    brows = ln(brow, 2.1, "#221c1b") + ln(mirror_path(brow), 2.1, "#221c1b")
    g.append(brows)
    for d in FRINGE_TUFTS:
        g.append(p(d, HAIR, 1.3, HAIR_LINE))
    g.append(p(FRINGE, HAIR, 1.5, HAIR_LINE))
    for d in FRINGE_STRANDS:
        g.append(ln(d, 0.9, "#4e4c57", 0.9))
    for d in FRINGE_HI:
        g.append(ln(d, 2.4, HAIR_HI, 0.75))
    g.append(f'<g opacity="0.35">{brows}</g>')
    if expr == "wince":
        for x, y in ((50, 36), (55, 43), (57, 51)):
            g.append(ln(f"M {x} {y} l 6 -3", 1.2, LINE, 0.7))
    g.append(extras)
    return f'<g transform="translate(0,{HEAD_LIFT})">{"".join(g)}</g>'


# ================================================================ HEAD (side, facing right)
def head_side():
    face = ("M -30 30 C -30 0 30 -6 34 30 C 35 42 36 48 35 52 C 36 60 40 70 43 77 "
            "Q 44 80 40 82 L 37 83 Q 37 86 38 88 Q 36 90 35.5 91 Q 37 93 36 96 "
            "Q 34 99 33 100 Q 35 108 29 110 L 6 103 L -10 90 C -24 80 -32 60 -30 30 Z")
    hair = ("M -41 76 C -56 30 -32 -22 10 -19 C 40 -16 50 18 45 50 "
            "Q 41 47 38 59 Q 35 47 30 40 Q 28 50 24 57 Q 22 45 16 38 "
            "Q 14 52 12 62 Q 11 70 10 80 Q 5 72 2 58 "
            "C -6 52 -13 56 -14 64 Q -15 76 -18 88 Q -22 82 -26 94 "
            "Q -31 84 -37 90 Q -39 82 -41 76 Z")
    tufts = ["M -4 -18 Q 4 -30 14 -27 Q 8 -23 10 -17 Z", "M -36 20 Q -46 24 -48 34 Q -42 30 -38 32 Z"]
    g = [p(face, SKIN, 1.6)]
    g.append(f'<path d="M 6 103 L 29 110 Q 20 105 10 98 Z" fill="{SKIN_SH}"/>')
    # eye
    g.append(f'<clipPath id="sideEye"><path d="M 23 64 Q 28 62 32.5 65 L 31.8 69.5 Q 27.5 71 24 70 Z"/></clipPath>')
    g.append(p("M 23 64 Q 28 62 32.5 65 L 31.8 69.5 Q 27.5 71 24 70 Z", "#fff", 0.6, LINE_SOFT))
    g.append('<g clip-path="url(#sideEye)"><ellipse cx="30" cy="67" rx="2.4" ry="4" fill="url(#iris)"/>'
             '<circle cx="29.3" cy="65.6" r="0.8" fill="#fff"/></g>')
    g.append(ln("M 22.5 64 Q 28 61.5 33 65", 2.2, "#221c1b"))
    g.append(ln("M 24 71 Q 28 72.5 31.5 70.5", 0.8, LINE, 0.55) + '<path d="M 23 71 Q 28 76 32 71 Q 28 74 23 71 Z" fill="#cdbdb6" opacity="0.55"/>')
    g.append(ln("M 23 60 Q 28 58 32 60.5", 0.8, LINE, 0.5))
    g.append(ln("M 33 91 L 35.5 91", 1.1))
    brow = ln("M 21 56 Q 28 54 34 56", 2.1, "#221c1b")
    g.append(brow)
    for d in tufts:
        g.append(p(d, HAIR, 1.3, HAIR_LINE))
    g.append(p(hair, HAIR, 1.5, HAIR_LINE))
    for d in ("M 8 -12 Q 30 6 38 54", "M 0 -12 Q 20 12 24 54", "M -10 -8 Q 8 20 10 76",
              "M -20 -4 Q -18 40 -24 90", "M -32 10 Q -36 50 -36 86"):
        g.append(ln(d, 0.9, "#4e4c57", 0.9))
    for d in ("M -26 2 Q -10 -10 10 -10", "M 18 -6 Q 30 2 36 14"):
        g.append(ln(d, 2.4, HAIR_HI, 0.75))
    # ear sits over the hair mass
    g.append(p("M 0 58 C -8 56 -10 70 -6 78 C -2 84 4 82 6 76 C 8 68 6 60 0 58 Z", SKIN, 1.3))
    g.append(ln("M -1 63 Q -5 70 -2 76 Q 2 74 2 70", 0.9, LINE, 0.6))
    # sideburn lock in front of ear
    g.append(p("M 12 60 Q 11 70 10 80 Q 6 72 4 60 Z", HAIR, 1.2, HAIR_LINE))
    g.append(f'<g opacity="0.4">{brow}</g>')
    return "".join(g)


# ================================================================ HEAD (back)
def head_back():
    hair = ("M -54 62 C -60 6 -38 -21 0 -21 C 38 -21 60 6 54 62 C 52 82 46 96 38 104 "
            "L 33 88 L 27 98 L 19 90 L 10 102 L 2 92 L -6 101 L -14 90 L -22 98 "
            "L -30 88 L -38 101 C -46 96 -52 82 -54 62 Z")
    g = []
    for sx in (1, -1):
        g.append(f'<g transform="scale({sx},1)">'
                 + p(EAR, SKIN, 1.3)
                 + "</g>")
    for d in ("M -8 -18 Q -2 -30 10 -28 Q 4 -24 6 -18 Z", "M 48 24 Q 57 30 58 39 Q 53 35 49 37 Z",
              "M -48 26 Q -57 32 -57 41 Q -52 37 -49 39 Z"):
        g.append(p(d, HAIR, 1.3, HAIR_LINE))
    g.append(p(hair, HAIR, 1.5, HAIR_LINE))
    for d in ("M 2 -4 Q -6 30 -7 104", "M 2 -4 Q 10 30 9 104", "M -2 -6 Q -24 30 -24 100",
              "M 4 -6 Q 26 30 24 100", "M -6 -4 Q -40 20 -40 96", "M 8 -4 Q 40 20 40 96",
              "M 0 -2 Q -2 50 0 100"):
        g.append(ln(d, 0.9, "#4e4c57", 0.9))
    # crown whorl + gloss band
    g.append(ln("M -4 4 Q 2 0 4 6 Q 2 10 -2 8", 1.0, HAIR_HI, 0.8))
    g.append(ln("M -36 14 Q -10 0 14 2", 2.6, HAIR_HI, 0.7))
    g.append(ln("M 24 6 Q 34 10 40 18", 2.6, HAIR_HI, 0.7))
    return "".join(g)


# ================================================================ BODY (front)
def legs_front(back=False):
    pants = ("M -45 418 C -47 560 -49 700 -47 852 L -9 855 C -9 720 -5 560 0 470 "
             "C 5 560 9 720 9 855 L 47 852 C 49 700 47 560 45 418 Z")
    g = [p(pants, PANTS, 1.6)]
    # inner-leg shading + creases
    g.append(f'<path d="M -9 855 C -9 720 -5 560 0 470 C -4 560 -18 720 -20 855 Z" fill="{PANTS_SH}"/>')
    g.append(f'<path d="M 9 855 C 9 720 5 560 0 470 C 4 560 18 720 20 855 Z" fill="{PANTS_SH}"/>')
    g.append(p(pants, "none", 1.6))
    for sx in (1, -1):
        g.append(f'<g transform="scale({sx},1)">'
                 + ln("M -30 480 Q -27 620 -28 840", 0.9, LINE_SOFT, 0.7)
                 + ln("M -40 640 Q -32 650 -24 646", 0.8, LINE_SOFT, 0.7)
                 + ln("M -42 800 Q -32 808 -16 806", 0.8, LINE_SOFT, 0.7)
                 + ln("M -46 836 Q -28 846 -10 842", 0.8, LINE_SOFT, 0.7)
                 + "</g>")
    if back:
        g.append(ln("M 0 420 L 0 470", 1.0, LINE, 0.7))
        g.append(ln("M -38 446 Q -24 452 -10 446", 0.9, LINE_SOFT, 0.8))
        g.append(ln("M 38 446 Q 24 452 10 446", 0.9, LINE_SOFT, 0.8))
    else:
        g.append(ln("M 0 420 L 0 466", 1.0, LINE, 0.6))
        g.append(ln("M -36 424 Q -30 440 -32 462", 0.9, LINE_SOFT, 0.8))
        g.append(ln("M 36 424 Q 30 440 32 462", 0.9, LINE_SOFT, 0.8))
    # socks / feet
    for sx in (1, -1):
        foot = ("M -44 851 C -48 862 -50 874 -44 881 L -13 881 C -8 874 -9 860 -11 853 Z"
                if not back else
                "M -44 851 C -46 864 -46 876 -42 881 L -14 881 C -10 876 -10 862 -11 853 Z")
        g.append(f'<g transform="scale({sx},1)">'
                 + p(foot, SOCK, 1.4)
                 + f'<path d="M -44 851 L -11 853 L -11 860 Q -28 864 -45 858 Z" fill="{SOCK_SH}"/>'
                 + ln("M -46 870 Q -30 874 -12 871", 0.8, LINE_SOFT, 0.6)
                 + "</g>")
    return "".join(g)


def torso_front():
    g = []
    # neck
    g.append(p("M -14 96 L -15 140 L 15 140 L 14 96 Z", SKIN, 1.4) + ln("M -1 124 Q 1 128 0 131", 0.9, LINE, 0.5))
    g.append(f'<path d="M -14 104 Q 0 120 14 104 L 14 118 Q 0 128 -14 118 Z" fill="{SKIN_SH}"/>')
    # cardigan back of collar, seen behind the neck
    g.append(p("M -22 140 Q -16 128 0 127 Q 16 128 22 140 L 14 141 Q 0 134 -14 141 Z", CARD_SH, 1.3))
    # T-shirt
    g.append(p("M -30 136 Q -16 132 -12 134 Q 0 148 12 134 Q 16 132 30 136 L 32 448 L -32 448 Z",
               SHIRT, 1.5))
    g.append(ln("M -14 135 Q 0 152 14 135", 1.0, LINE, 0.6))
    g.append(f'<path d="M -12 134 Q 0 148 12 134 Q 0 154 -12 134 Z" fill="{SHIRT_SH}"/>')
    g.append(ln("M -8 250 Q -2 280 -6 330", 0.8, LINE_SOFT, 0.6))
    g.append(ln("M 6 360 Q 10 400 6 440", 0.8, LINE_SOFT, 0.6))
    # cardigan body panels (open front)
    for sx in (1, -1):
        body = ("M -14 139 L -58 148 C -66 250 -64 380 -60 480 L -22 484 "
                "C -24 380 -26 260 -15 150 Z")
        band = "M -14 139 C -25 260 -23 380 -22 484 L -30 484 C -32 380 -33 260 -21 141 Z"
        g.append(f'<g transform="scale({sx},1)">'
                 + p(body, CARD, 1.6)
                 + f'<path d="M -58 148 C -66 250 -64 380 -60 480 L -50 481 C -54 380 -56 260 -50 160 Z" fill="{CARD_SH}"/>'
                 + p(band, CARD, 1.2)
                 + f'<path d="M -61 458 L -22 461 L -22 484 L -60 480 Z" fill="{CARD_SH}" opacity="0.5"/>'
                 + ln("M -61 458 L -22 461", 1.0, CARD_LINE, 0.9)
                 + "".join(ln(f"M {x} {459 + (x + 61) * 0.07} L {x} {481 + (x + 61) * 0.08}", 0.6, CARD_LINE, 0.55)
                           for x in range(-57, -22, 5))
                 + ln("M -40 230 Q -44 300 -40 380", 0.8, CARD_LINE, 0.5)
                 + "</g>")
    # buttons on the wearer's right placket (viewer's left)
    for y in (200, 260, 320, 380, 440):
        g.append(f'<circle cx="-26" cy="{y}" r="2.6" fill="#f7f1e6" stroke="{CARD_LINE}" stroke-width="0.9"/>')
    # sleeves with dropped shoulders + hands
    for sx in (1, -1):
        sleeve = ("M -56 147 C -72 150 -79 166 -81 192 C -87 282 -91 382 -91 457 "
                  "L -65 458 C -65 382 -63 300 -61 232 Z")
        g.append(f'<g transform="scale({sx},1)">'
                 + p("M -88 478 C -91 498 -86 520 -77 525 C -68 526 -63 508 -66 478 Z", SKIN, 1.4)
                 + ln("M -84 500 Q -82 510 -79 516", 0.8, LINE, 0.55)
                 + ln("M -76 498 Q -74 508 -72 514", 0.8, LINE, 0.55)
                 + ln("M -67 486 Q -64 496 -68 504", 0.9, LINE, 0.6)
                 + p(sleeve, CARD, 1.6)
                 + f'<path d="M -81 192 C -87 282 -91 382 -91 457 L -82 457 C -82 380 -80 290 -74 200 Z" fill="{CARD_SH}"/>'
                 + ln("M -70 152 Q -74 170 -75 186", 0.9, CARD_LINE, 0.7)
                 + ln("M -80 300 Q -74 312 -66 306", 0.8, CARD_LINE, 0.55)
                 + ln("M -84 380 Q -76 392 -66 386", 0.8, CARD_LINE, 0.55)
                 + p("M -91 456 L -65 457 L -66 480 L -89 480 Z", CARD, 1.3)
                 + "".join(ln(f"M {x} 458 L {x} 479", 0.6, CARD_LINE, 0.55) for x in range(-87, -66, 4))
                 + "</g>")
    return "".join(g)


def figure_front():
    return legs_front() + f'<g transform="scale(1.1,1)">{torso_front()}</g>' + head_front("calm")


# ================================================================ BODY (side)
def figure_side():
    g = []
    # far leg (slightly behind, a touch darker)
    g.append(p("M -24 430 C -30 520 -22 600 -18 700 C -16 780 -14 820 -14 852 L 22 852 "
               "C 22 780 18 690 22 600 C 24 520 22 470 22 430 Z", PANTS_SH, 1.4,
               extra='transform="translate(-6,0)"'))
    g.append(p("M -20 851 C -22 866 -20 879 -14 880 L 38 880 C 44 878 42 868 34 864 "
               "C 20 860 16 856 16 851 Z", SOCK_SH, 1.3, extra='transform="translate(-6,0)"'))
    # near leg
    pants = ("M -31 418 C -36 470 -28 520 -23 600 C -21 700 -19 780 -19 855 L 26 855 "
             "C 24 760 21 680 24 600 C 27 520 30 470 27 418 Z")
    g.append(p(pants, PANTS, 1.6))
    g.append(f'<path d="M -31 418 C -36 470 -28 520 -23 600 C -21 700 -19 780 -19 855 L -10 855 '
             f'C -12 760 -14 660 -14 600 C -18 520 -24 470 -22 418 Z" fill="{PANTS_SH}"/>')
    g.append(p(pants, "none", 1.6))
    g.append(ln("M 6 470 Q 4 640 6 840", 0.9, LINE_SOFT, 0.7))
    g.append(ln("M 24 640 Q 14 650 4 646", 0.8, LINE_SOFT, 0.7))
    g.append(ln("M 26 836 Q 4 846 -18 842", 0.8, LINE_SOFT, 0.7))
    g.append(p("M -18 852 C -20 866 -18 879 -12 880 L 44 880 C 50 878 48 868 40 864 "
               "C 26 860 22 856 24 852 Z", SOCK, 1.4))
    g.append(f'<path d="M -18 852 L 24 852 L 24 858 Q 4 862 -18 858 Z" fill="{SOCK_SH}"/>')
    # neck, slight forward lean
    g.append(p("M -16 88 L -16 140 L 18 140 L 16 102 Z", SKIN, 1.4) + ln("M 16 114 Q 19 118 17 122", 0.9, LINE, 0.6))
    g.append(f'<path d="M -14 96 L 14 104 L 14 118 L -14 112 Z" fill="{SKIN_SH}"/>')
    # T-shirt sliver at chest
    g.append(p("M 6 132 C 26 150 32 220 28 300 C 26 380 26 420 28 446 L 10 446 Z", SHIRT, 1.4))
    # cardigan body
    card = ("M -24 136 C -40 160 -40 260 -38 360 C -38 420 -40 460 -40 482 L 26 484 "
            "C 22 440 22 380 24 300 C 26 220 26 170 10 134 Q -6 130 -24 136 Z")
    g.append(p(card, CARD, 1.6))
    g.append(f'<path d="M -24 136 C -40 160 -40 260 -38 360 C -38 420 -40 460 -40 482 L -29 482 '
             f'C -31 420 -31 300 -24 160 Z" fill="{CARD_SH}"/>')
    g.append(p("M 10 134 C 26 170 26 220 24 300 C 22 380 22 440 26 484 L 18 484 C 14 440 14 380 16 300 "
               "C 18 220 18 170 4 138 Z", CARD, 1.2))
    g.append(p("M -40 460 L 26 462 L 26 484 L -40 482 Z", CARD, 1.2))
    g.append("".join(ln(f"M {x} 461 L {x} 483", 0.6, CARD_LINE, 0.55) for x in range(-36, 26, 5)))
    # collar rib around neck
    g.append(p("M -24 136 Q -6 128 10 134 L 4 140 Q -8 136 -20 141 Z", CARD_SH, 1.2))
    # arm / sleeve hanging, hand
    g.append(p("M -6 476 C -9 500 -3 524 7 527 C 15 525 17 505 15 476 Z", SKIN, 1.4))
    g.append(ln("M 3 500 Q 6 512 6 520", 0.8, LINE, 0.55))
    sleeve = ("M -16 143 C -32 150 -32 180 -27 220 C -22 320 -16 400 -12 458 L 18 458 "
              "C 16 400 13 320 12 220 C 13 180 8 148 -16 143 Z")
    g.append(p(sleeve, CARD, 1.6))
    g.append(f'<path d="M -27 220 C -22 320 -16 400 -12 458 L -3 458 C -6 400 -10 320 -16 220 Z" fill="{CARD_SH}"/>')
    g.append(ln("M -20 300 Q -4 310 10 304", 0.8, CARD_LINE, 0.55))
    g.append(ln("M -14 390 Q 0 400 14 394", 0.8, CARD_LINE, 0.55))
    g.append(p("M -12 457 L 18 457 L 17 480 L -9 480 Z", CARD, 1.3))
    g.append("".join(ln(f"M {x} 458 L {x} 479", 0.6, CARD_LINE, 0.55) for x in range(-8, 17, 4)))
    g.append(f'<g transform="translate(0,-10) scale(1,1.08)">{head_side()}</g>')
    return "".join(g)


# ================================================================ BODY (back)
def figure_back():
    g = [legs_front(back=True), '<g transform="scale(1.1,1)">']
    g.append(p("M -14 90 L -15 140 L 15 140 L 14 90 Z", SKIN, 1.4))
    # cardigan back (one piece)
    for sx in (1, -1):
        g.append(f'<g transform="scale({sx},1)">'
                 + p("M 0 132 L -58 148 C -66 250 -64 380 -60 480 L 0 484 Z", CARD, 1.6)
                 + f'<path d="M -58 148 C -66 250 -64 380 -60 480 L -50 481 C -54 380 -56 260 -50 160 Z" fill="{CARD_SH}"/>'
                 + ln("M -40 240 Q -44 320 -40 400", 0.8, CARD_LINE, 0.5)
                 + "</g>")
    g.append(p("M -60 480 L 60 480 L 60 458 L -61 458 Z", CARD, 1.2))
    g.append("".join(ln(f"M {x} 459 L {x} 479", 0.6, CARD_LINE, 0.55) for x in range(-57, 60, 5)))
    g.append(ln("M 0 300 Q -10 360 -4 450", 0.8, CARD_LINE, 0.45))
    g.append(p("M -22 140 Q -14 130 0 129 Q 14 130 22 140 Q 0 146 -22 140 Z", CARD_SH, 1.3))
    for sx in (1, -1):
        sleeve = ("M -56 147 C -72 150 -79 166 -81 192 C -87 282 -91 382 -91 457 "
                  "L -65 458 C -65 382 -63 300 -61 232 Z")
        g.append(f'<g transform="scale({sx},1)">'
                 + p("M -88 478 C -91 498 -86 520 -77 525 C -68 526 -63 508 -66 478 Z", SKIN, 1.4)
                 + p(sleeve, CARD, 1.6)
                 + f'<path d="M -61 232 C -63 300 -65 382 -65 458 L -72 458 C -72 380 -70 300 -66 220 Z" fill="{CARD_SH}"/>'
                 + ln("M -70 152 Q -74 170 -75 186", 0.9, CARD_LINE, 0.7)
                 + ln("M -80 330 Q -74 342 -66 336", 0.8, CARD_LINE, 0.55)
                 + p("M -91 456 L -65 457 L -66 480 L -89 480 Z", CARD, 1.3)
                 + "".join(ln(f"M {x} 458 L {x} 479", 0.6, CARD_LINE, 0.55) for x in range(-87, -66, 4))
                 + "</g>")
    g.append('</g>')
    g.append(f'<g transform="translate(0,-10)">{head_back()}</g>')
    return "".join(g)


# ================================================================ EXPRESSION BUSTS
def bust_shoulders():
    g = [p("M -14 96 L -15 150 L 15 150 L 14 96 Z", SKIN, 1.4) + ln("M -1 124 Q 1 128 0 131", 0.9, LINE, 0.5),
         f'<path d="M -14 104 Q 0 120 14 104 L 14 118 Q 0 128 -14 118 Z" fill="{SKIN_SH}"/>',
         p("M -22 140 Q -16 128 0 127 Q 16 128 22 140 L 14 141 Q 0 134 -14 141 Z", CARD_SH, 1.3),
         p("M -30 136 Q -16 132 -12 134 Q 0 148 12 134 Q 16 132 30 136 L 32 300 L -32 300 Z", SHIRT, 1.5),
         ln("M -14 135 Q 0 152 14 135", 1.0, LINE, 0.6),
         f'<path d="M -12 134 Q 0 148 12 134 Q 0 154 -12 134 Z" fill="{SHIRT_SH}"/>']
    for sx in (1, -1):
        g.append(f'<g transform="scale({sx},1)">'
                 + p("M -14 139 L -58 148 C -64 200 -66 260 -66 300 L -22 300 C -24 260 -22 200 -15 150 Z", CARD, 1.6)
                 + p("M -14 139 C -22 200 -23 260 -22 300 L -30 300 C -31 260 -30 200 -21 141 Z", CARD, 1.2)
                 + p("M -56 147 C -72 150 -79 166 -81 192 C -85 240 -88 280 -88 300 L -64 300 "
                     "C -63 260 -62 240 -61 232 Z", CARD, 1.6)
                 + ln("M -70 152 Q -74 170 -75 186", 0.9, CARD_LINE, 0.7)
                 + "</g>")
    g.append(f'<circle cx="-26" cy="200" r="2.6" fill="#f7f1e6" stroke="{CARD_LINE}" stroke-width="0.9"/>')
    return "".join(g)


def worried_hand():
    return (p("M 6 230 L 18 141 L 46 147 L 54 230 Z", CARD, 1.6)
            + f'<path d="M 6 230 L 18 141 L 26 143 L 18 230 Z" fill="{CARD_SH}"/>'
            + p("M 22 140 C 12 128 9 115 11 106 C 12 100 17 98 21 100 C 25 97 30 99 31 103 "
                "C 35 102 40 106 40 113 C 44 119 46 130 45 146 Z", SKIN, 1.4)
            + ln("M 21 100 Q 22 108 19 115", 0.9, LINE, 0.6)
            + ln("M 31 103 Q 31 111 27 118", 0.9, LINE, 0.6)
            + ln("M 14 112 Q 20 122 28 124", 0.9, LINE, 0.55)
            + p("M 17 139 L 46 145 L 45 158 L 15 152 Z", CARD, 1.3)
            + "".join(ln(f"M {x} {139 + (x - 17) * 0.2} L {x - 1} {152 + (x - 17) * 0.2}", 0.6, CARD_LINE, 0.55)
                      for x in range(20, 45, 4)))


def bust(expr):
    tilt = {"calm": 0, "up": -7, "worried": 2, "wince": -3, "sad": 5, "smile": 4}[expr]
    head = head_front(expr)
    g = f'<g transform="scale(1.1,1)">{bust_shoulders()}</g>' + f'<g transform="rotate({tilt} 0 108)">{head}</g>'
    if expr == "worried":
        g += worried_hand()
    return g


# ================================================================ SHEET
W, H = 2100, 1100


def build():
    defs = ("<defs>"
            '<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#2b2c33"/><stop offset="0.55" stop-color="#4f535c"/>'
            '<stop offset="1" stop-color="#8c919b"/></linearGradient>'
            f'<clipPath id="faceClip"><path d="{FACE}"/></clipPath>'
            + eye_defs() + "</defs>")

    body = []
    # faint proportion guides across the turnaround (head units of ~110)
    fy0, fs = 92, 1.0
    for k in (0, 113, 440, 650, 880):
        y = fy0 + k * fs
        body.append(f'<line x1="60" x2="1000" y1="{y}" y2="{y}" stroke="{GUIDE}" stroke-width="1.2" '
                    f'stroke-dasharray="6 6"/>')
    for cx, fig in ((200, figure_front()), (530, figure_side()), (860, figure_back())):
        body.append(f'<ellipse cx="{cx + (6 if cx == 530 else 0)}" cy="{fy0 + 882 * fs}" rx="78" ry="9" '
                    f'fill="#ece8e2"/>')
        body.append(f'<g transform="translate({cx},{fy0}) scale({fs})">{fig}</g>')

    # expression grid 3 x 2
    exprs = ["calm", "up", "worried", "wince", "sad", "smile"]
    pw, ph, gx, gy = 300, 470, 20, 30
    x0, y0, sc = 1090, 65, 1.9
    for i, e in enumerate(exprs):
        col, row = i % 3, i // 3
        px, py = x0 + col * (pw + gx), y0 + row * (ph + gy)
        cid = f"panel{i}"
        body.append(f'<clipPath id="{cid}"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18"/></clipPath>')
        body.append(f'<g clip-path="url(#{cid})"><g transform="translate({px + pw / 2},{py + 72}) scale({sc})">'
                    f'{bust(e)}</g></g>')
        body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="none" '
                    f'stroke="{PANEL}" stroke-width="1.5"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'{defs}<rect width="{W}" height="{H}" fill="#ffffff"/>{"".join(body)}</svg>')


if __name__ == "__main__":
    out = Path(__file__).with_name("haru_reference_sheet.svg")
    out.write_text(build())
    print(out)
