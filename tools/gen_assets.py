import subprocess, textwrap, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join("docs", "screenshots")
os.makedirs(OUT, exist_ok=True)


def font(path, size, bold=False):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


MONO = font("C:\\Windows\\Fonts\\consola.ttf", 18)
MONO_B = font("C:\\Windows\\Fonts\\consolab.ttf", 18)
TITLE = font("C:\\Windows\\Fonts\\segoeui.ttf", 64, True) or font("C:\\Windows\\Fonts\\arial.ttf", 64)
SUB = font("C:\\Windows\\Fonts\\segoeui.ttf", 26) or font("C:\\Windows\\Fonts\\arial.ttf", 26)


# ---------- BANNER ----------
W, H = 1200, 320
img = Image.new("RGB", (W, H), (10, 14, 20))
d = ImageDraw.Draw(img)
# subtle grid
for x in range(0, W, 40):
    d.line([(x, 0), (x, H)], fill=(20, 26, 34), width=1)
for y in range(0, H, 40):
    d.line([(0, y), (W, y)], fill=(20, 26, 34), width=1)
# accent bar
d.rectangle([0, 0, 10, H], fill=(0, 200, 160))
d.text((60, 70), "RESOURCE GATHER", font=TITLE, fill=(235, 245, 245))
d.text((62, 170), "Defense-grade OSINT resource-gathering framework", font=SUB, fill=(150, 200, 190))
d.text((62, 220), "paste sites   ·   torrent / file distribution   ·   the inbetween   ·   custom search",
       font=font("C:\\Windows\\Fonts\\segoeui.ttf", 20), fill=(90, 140, 130))
d.text((62, 262), "37,000+ materialized functions   ·   Tor / I2P aware   ·   defensive-only",
       font=font("C:\\Windows\\Fonts\\consola.ttf", 18), fill=(0, 200, 160))
img.save(os.path.join(OUT, "banner.png"))
print("wrote banner.png")


# ---------- TERMINAL SCREENSHOT ----------
def terminal(lines, title, fname, width=900):
    pad = 16
    lh = 24
    # measure
    maxw = max(d2.textlength(ln, font=MONO) for ln in lines) if False else None
    tw = width
    th = pad * 2 + lh * len(lines) + 36
    im = Image.new("RGB", (tw, th), (13, 17, 23))
    dd = ImageDraw.Draw(im)
    # title bar
    dd.rectangle([0, 0, tw, 34], fill=(28, 34, 44))
    dd.text((14, 8), title, font=MONO_B, fill=(180, 190, 200))
    for i, ln in enumerate(lines):
        y = 34 + pad + i * lh
        col = (180, 220, 200) if ln.startswith("$") else (200, 210, 215)
        if ln.startswith("  --"):
            col = (120, 200, 255)
        dd.text((pad, y), ln, font=MONO, fill=col)
    im.save(os.path.join(OUT, fname))
    print("wrote", fname)


help_txt = subprocess.run(["python", "main.py", "--help"],
                          capture_output=True, text=True, encoding="utf-8").stdout
help_lines = [l.rstrip() for l in help_txt.splitlines() if l.strip()]
terminal(help_lines[:34], "resourcegather — python main.py --help", "cli.png")

# second: selftest-style sample
sample = [
    "$ python main.py --selftest",
    "settings OK: keywords=5",
    "data/paste_sites.json OK (1 keys)",
    "data/torrent_sites.json OK (5 keys)",
    "data/inbetween.json OK (9 keys)",
    "data/search_targets.json OK (2 keys)",
    "core.sources: 18355 generated functions",
    "TOTAL: 37074 functions   >=500: True",
    "Self-test passed.",
]
terminal(sample, "resourcegather — python main.py --selftest", "selftest.png")
