"""Draw the passport spread of the Republic of Sulara (invented).

One image, 1024x1024, PIL only, deterministic: no randomness, no
network, no clock. Every date on the document agrees: the passport was
issued 12 MAR 2024, expires 12 MAR 2034, and every stamp falls between
those dates. The telling detail is CONDITION 7, the salt caravan permit.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

INK = (31, 42, 51)
TEAL = (20, 86, 79)
GOLD = (176, 141, 47)
CREAM = (242, 236, 220)
CREAM2 = (238, 231, 210)
RED = (169, 50, 38)
BLUE = (29, 78, 137)
GREEN = (46, 107, 52)
PURPLE = (91, 45, 142)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_c(d, xy, s, f, fill, size, anchor="mm"):
    d.text(xy, s, font=font(f, size), fill=fill, anchor=anchor)


def mrz_check(s):
    vals = {}
    for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = i
    vals["<"] = 0
    total = 0
    for i, ch in enumerate(s):
        total += vals[ch] * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<SURHADDAD<<LAYLA<AMIRA" + "<" * 20
    doc = "SR4829137"
    dob = "880914"
    exp = "340312"
    personal = "<" * 14
    line2 = (
        doc + mrz_check(doc)
        + "SUR" + dob + mrz_check(dob)
        + "F" + exp + mrz_check(exp)
        + personal
    )
    line2 += mrz_check(line2)
    return line1, line2


def guilloche(d, x0, y0, x1, y1, color, step=7, amp=2.2):
    for y in range(y0, y1, step):
        pts = []
        for x in range(x0, x1 + 1, 6):
            pts.append((x, y + amp * math.sin((x - x0) / 26.0 + y / 9.0)))
        d.line(pts, fill=color, width=1)


def stamp(d, cx, cy, w, h, angle, color, lines, sub="", sub2=""):
    """A rectangular entry/exit stamp, drawn on its own layer and rotated."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=8,
                         outline=color + (255,), width=3)
    sd.rounded_rectangle([25, 25, 15 + w, 15 + h], radius=6,
                         outline=color + (200,), width=1)
    f1 = font(SANS_B, 20)
    f2 = font(SANS_B, 16)
    f3 = font(SANS_B, 13)
    f4 = font(SANS, 10)
    y = 30
    for i, ln in enumerate(lines):
        ff = f1 if i == 0 else f2
        sd.text((20 + w // 2, y), ln, font=ff, fill=color + (255,),
                anchor="ma")
        y += 23 if i == 0 else 20
    if sub:
        sd.text((20 + w // 2, y + 1), sub, font=f3, fill=color + (230,),
                anchor="ma")
        y += 16
    if sub2:
        sd.text((20 + w // 2, y + 1), sub2, font=f4, fill=color + (210,),
                anchor="ma")
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    d._image.paste(layer, (cx - w // 2 - 20, cy - h // 2 - 20), layer)


def portrait(d, x0, y0, w, h):
    """Flat-style passport portrait: a salt-caravan guide in an ochre scarf."""
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=4,
                        fill=(214, 226, 219), outline=(120, 130, 120), width=2)
    # soft halo
    d.ellipse([x0 + w // 2 - 52, y0 + 8, x0 + w // 2 + 52, y0 + 112],
              fill=(228, 234, 226))
    # shoulders / robe
    d.polygon([(x0 + 8, y0 + h - 4), (x0 + w // 2 - 42, y0 + 128),
               (x0 + w // 2 + 42, y0 + 128), (x0 + w - 8, y0 + h - 4)],
              fill=(35, 74, 68))
    d.polygon([(x0 + w // 2 - 14, y0 + 128), (x0 + w // 2 + 14, y0 + 128),
               (x0 + w // 2, y0 + 152)], fill=(242, 236, 220))
    # neck
    d.rectangle([x0 + w // 2 - 13, y0 + 108, x0 + w // 2 + 13, y0 + 132],
                fill=(178, 122, 78))
    # face
    d.ellipse([x0 + w // 2 - 30, y0 + 34, x0 + w // 2 + 30, y0 + 108],
              fill=(201, 143, 95))
    # headscarf: ochre, covers top and sides of the head
    d.pieslice([x0 + w // 2 - 38, y0 + 18, x0 + w // 2 + 38, y0 + 96],
               180, 360, fill=(201, 138, 46))
    d.polygon([(x0 + w // 2 - 38, y0 + 52), (x0 + w // 2 - 30, y0 + 34),
               (x0 + w // 2 - 30, y0 + 96), (x0 + w // 2 - 38, y0 + 104)],
              fill=(178, 118, 36))
    d.polygon([(x0 + w // 2 + 38, y0 + 52), (x0 + w // 2 + 30, y0 + 34),
               (x0 + w // 2 + 30, y0 + 96), (x0 + w // 2 + 38, y0 + 104)],
              fill=(178, 118, 36))
    # scarf fold line
    d.arc([x0 + w // 2 - 38, y0 + 18, x0 + w // 2 + 38, y0 + 96],
          200, 340, fill=(150, 96, 26), width=2)
    # brows, eyes
    for s in (-1, 1):
        ex = x0 + w // 2 + s * 14
        d.arc([ex - 8, y0 + 58, ex + 8, y0 + 68], 200, 340,
              fill=(60, 38, 22), width=2)
        d.ellipse([ex - 5, y0 + 66, ex + 5, y0 + 72], fill=(255, 255, 255))
        d.ellipse([ex - 3, y0 + 67, ex + 3, y0 + 72], fill=(52, 32, 18))
    # nose + mouth
    d.line([(x0 + w // 2, y0 + 72), (x0 + w // 2 - 2, y0 + 84),
            (x0 + w // 2 + 2, y0 + 86)], fill=(150, 96, 60), width=2)
    d.arc([x0 + w // 2 - 8, y0 + 90, x0 + w // 2 + 8, y0 + 100], 15, 165,
          fill=(122, 62, 52), width=2)
    # gold earring hint
    d.ellipse([x0 + w // 2 - 36, y0 + 92, x0 + w // 2 - 31, y0 + 97],
              fill=GOLD)


def coat_of_arms(d, cx, cy, r):
    """Sun over the salt pan, flanked by two caravan staffs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    d.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7],
              outline=GOLD, width=1)
    # sun disc
    d.ellipse([cx - 13, cy - 22, cx + 13, cy + 4], fill=GOLD)
    for a in range(0, 360, 45):
        x1 = cx + 17 * math.cos(math.radians(a))
        y1 = cy - 9 + 17 * math.sin(math.radians(a))
        x2 = cx + 23 * math.cos(math.radians(a))
        y2 = cy - 9 + 23 * math.sin(math.radians(a))
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)
    # salt pan: three pale lines
    for i, yy in enumerate((cy + 10, cy + 16, cy + 22)):
        d.line([(cx - r + 12, yy), (cx + r - 12, yy)],
               fill=(TEAL if i % 2 == 0 else GOLD), width=2)
    # staffs
    for s in (-1, 1):
        x = cx + s * (r - 4)
        d.line([(x, cy - r + 10), (x, cy + r - 10)], fill=TEAL, width=3)
        d.ellipse([x - 3, cy - r + 6, x + 3, cy - r + 12], fill=TEAL)


def draw():
    img = Image.new("RGB", (W, H), (38, 34, 30))
    d = ImageDraw.Draw(img)
    # faint leather grain
    for i in range(0, H, 6):
        d.line([(0, i), (W, i)], fill=(42, 38, 33), width=1)
    # the spread: two pages
    px, py, pw, ph = 44, 62, 462, 880
    qx = px + pw + 12
    # gutter shadow
    d.rectangle([px + pw - 4, py, px + pw + 16, py + ph], fill=(20, 18, 16))
    d.rectangle([px - 6, py - 6, px + pw + 6, py + ph + 6], fill=(28, 25, 22))
    d.rectangle([qx - 6, py - 6, qx + pw + 6, py + ph + 6], fill=(28, 25, 22))
    d.rectangle([px, py, px + pw, py + ph], fill=CREAM)
    d.rectangle([qx, py, qx + pw, py + ph], fill=CREAM)
    guilloche(d, px + 10, py + 10, px + pw - 10, py + ph - 10,
              (226, 216, 190))
    guilloche(d, qx + 10, py + 10, qx + pw - 10, py + ph - 10,
              (226, 216, 190))
    # page edge lines
    d.rectangle([px, py, px + pw, py + ph], outline=(190, 178, 150), width=2)
    d.rectangle([qx, py, qx + pw, py + ph], outline=(190, 178, 150), width=2)
    # faint watermark
    wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    wd.text((W // 2, H // 2), "SULARA", font=font(SERIF_B, 92),
            fill=(176, 141, 47, 26), anchor="mm")
    wm = wm.rotate(-24, resample=Image.BICUBIC)
    img.paste(wm, (0, 0), wm)
    d = ImageDraw.Draw(img)

    # ============ LEFT PAGE: data page ============
    cx = px + pw // 2
    coat_of_arms(d, cx, py + 52, 34)
    text_c(d, (cx, py + 106), "REPUBLIC OF SULARA", SERIF_B, TEAL, 26)
    text_c(d, (cx, py + 130), "P A S S P O R T", SERIF, INK, 15)
    d.line([(px + 24, py + 148), (px + pw - 24, py + 148)], fill=TEAL, width=2)
    d.line([(px + 24, py + 152), (px + pw - 24, py + 152)], fill=GOLD, width=1)
    # type / code / number row
    text_c(d, (px + 30, py + 168), "Type", SANS, (110, 100, 80), 11)
    text_c(d, (px + 30, py + 186), "P", SANS_B, INK, 17)
    text_c(d, (px + 150, py + 168), "Country code", SANS, (110, 100, 80), 11)
    text_c(d, (px + 150, py + 186), "SUR", SANS_B, INK, 17)
    text_c(d, (px + 280, py + 168), "Passport No.", SANS, (110, 100, 80), 11)
    text_c(d, (px + 280, py + 186), "SR4829137", SANS_B, INK, 17)

    # portrait + data fields
    portrait(d, px + 26, py + 212, 148, 188)
    # round seal overlapping the portrait's lower right
    sx, sy = px + 150, py + 372
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], outline=TEAL, width=2)
    d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], outline=TEAL, width=1)
    text_c(d, (sx, sy - 6), "★", SANS_B, TEAL, 14)
    text_c(d, (sx, sy + 9), "SULARA", SANS_B, TEAL, 9)

    fields = [
        ("Surname", "HADDAD"),
        ("Given names", "LAYLA AMIRA"),
        ("Nationality", "SULARAN"),
        ("Date of birth", "14 SEP 1988"),
        ("Place of birth", "ZHAL-PAN, SULARA"),
        ("Sex", "F"),
        ("Date of issue", "12 MAR 2024"),
        ("Date of expiry", "12 MAR 2034"),
        ("Authority", "MINISTRY OF THE PAN"),
        ("Place of issue", "TAMARAK, SULARA"),
    ]
    fx = px + 196
    fy = py + 214
    for i, (label, value) in enumerate(fields):
        y = fy + i * 34
        text_c(d, (fx, y), label, SANS, (110, 100, 80), 10, anchor="lm")
        text_c(d, (fx, y + 15), value, SANS_B, INK, 14, anchor="lm")
    # signature
    d.line([(px + 26, py + 428), (px + 168, py + 428)], fill=INK, width=1)
    text_c(d, (px + 97, py + 442), "Holder's signature", SANS,
           (110, 100, 80), 9)
    d.text((px + 34, py + 402), "Layla Haddad", font=font(SERIF_I, 20),
           fill=(40, 60, 90))
    # personal note line under the data block
    d.line([(px + 196, py + 556), (px + pw - 26, py + 556)], fill=(190, 178, 150), width=1)
    text_c(d, (cx, py + 574), "Salt caravan guide, licensed since 2011",
           SERIF_I, (90, 80, 60), 13)
    # MRZ
    l1, l2 = mrz_lines()
    d.rectangle([px + 16, py + 596, px + pw - 16, py + 668], fill=(250, 248, 240))
    d.rectangle([px + 16, py + 596, px + pw - 16, py + 668],
                outline=(150, 140, 115), width=1)
    mf = font(MONO, 15)
    d.text((px + 26, py + 606), l1, font=mf, fill=INK)
    d.text((px + 26, py + 630), l2, font=mf, fill=INK)
    text_c(d, (cx, py + 690), "This passport remains the property of the",
           SANS, (110, 100, 80), 10)
    text_c(d, (cx, py + 706), "Republic of Sulara.",
           SANS, (110, 100, 80), 10)
    # page number
    text_c(d, (cx, py + 850), "2", SERIF, (110, 100, 80), 12)

    # ============ RIGHT PAGE: visas & stamps ============
    qcx = qx + pw // 2
    text_c(d, (qcx, py + 34), "VISAS", SERIF_B, TEAL, 24)
    text_c(d, (qcx, py + 58), "ENTRY AND EXIT STAMPS", SERIF, INK, 12)
    d.line([(qx + 24, py + 76), (qx + pw - 24, py + 76)], fill=TEAL, width=2)
    d.line([(qx + 24, py + 80), (qx + pw - 24, py + 80)], fill=GOLD, width=1)

    stamp(d, qx + 130, py + 192, 200, 108, -4, BLUE,
          ["KHARUN", "ARRIVAL"], "28 JUN 2024", "POST 3 · TAMARAK GATE")
    stamp(d, qx + 340, py + 192, 200, 108, 5, BLUE,
          ["KHARUN", "DEPARTURE"], "03 JUL 2024", "POST 3 · TAMARAK GATE")
    stamp(d, qx + 130, py + 314, 200, 108, 3, RED,
          ["VELDORRA", "ARRIVAL"], "15 NOV 2024", "PASS 7 · NORTH ROAD")
    stamp(d, qx + 340, py + 314, 200, 108, -5, RED,
          ["VELDORRA", "DEPARTURE"], "22 NOV 2024", "PASS 7 · NORTH ROAD")
    stamp(d, qx + 130, py + 436, 200, 108, -3, GREEN,
          ["OSTARA", "ARRIVAL"], "09 APR 2025", "HARBOUR 2 · EAST QUAY")
    stamp(d, qx + 340, py + 436, 200, 108, 4, GREEN,
          ["OSTARA", "DEPARTURE"], "18 APR 2025", "HARBOUR 2 · EAST QUAY")

    # the telling detail: CONDITION 7, the salt caravan permit
    bx0, by0, bx1, by1 = qx + 26, py + 540, qx + pw - 26, py + 700
    d.rectangle([bx0, by0, bx1, by1], outline=RED, width=3)
    d.rectangle([bx0 + 5, by0 + 5, bx1 - 5, by1 - 5], outline=RED, width=1)
    text_c(d, ((bx0 + bx1) // 2, by0 + 26), "CONDITION 7 — SALT CARAVAN PERMIT",
           SANS_B, RED, 15)
    d.line([(bx0 + 16, by0 + 44), (bx1 - 16, by0 + 44)], fill=RED, width=1)
    cond = ("HOLDER IS LICENSED TO CROSS THE WHITE PAN ONLY\n"
            "BETWEEN FIRST AND LAST LIGHT. A NIGHT CROSSING\n"
            "REQUIRES A SEPARATE MOON PERMIT.")
    d.multiline_text(((bx0 + bx1) // 2, by0 + 62), cond,
                     font=font(SANS, 14), fill=INK, anchor="ma",
                     align="center", spacing=6)
    # fee stamp overlapping the box's lower edge, clear of the text
    stamp(d, bx1 - 82, by1 - 2, 150, 56, -6, PURPLE,
          ["SALT TAX PAID"], "40 DIRHAMS", "12 MAR 2024")

    text_c(d, (qcx, py + 730), "Neighbouring stamps agree with the date of issue:",
           SERIF_I, (90, 80, 60), 12)
    text_c(d, (qcx, py + 752), "no stamp predates this passport.",
           SERIF_I, (90, 80, 60), 12)
    text_c(d, (qcx, py + 850), "3", SERIF, (110, 100, 80), 12)

    # cover edge hint at the very bottom
    d.rectangle([0, H - 10, W, H], fill=(24, 21, 18))
    return img


def main():
    img = draw()
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
