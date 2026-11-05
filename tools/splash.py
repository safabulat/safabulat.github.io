#!/usr/bin/env python3
"""The hub's pictures: each product as a branded splash (its own ground, the app inside a device body),
plus the family shot that heads the page and the share card a pasted link shows.

Built rather than cropped — the same reason the store frames are (midiboard/tools/shots/frames.py,
kirisalim/tools/og.py): headless Chrome lays the picture out, so a re-render months from now gives the
same picture. Grounds are each product's own: Midiboard's four pads, Crossleaf's navy and highlighter,
Kırışalım's green and pie slices. Device bodies are plain slabs, not Apple's licensed artwork.

    python3 tools/splash.py        → img/splash-*.jpg, img/hero.jpg, img/og.png, favicon.svg stays hand-written

Sources live in the product repos; this script only reads them.
"""
import base64, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEV = os.path.expanduser("~/Desktop/development")
OUT = os.path.join(ROOT, "img")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SRC = {
    "mb_surface": f"{DEV}/Mobile/midiboard/tools/shots/source/1.png",
    "mb_icon":    f"{DEV}/Mobile/midiboard/site/img/appicon.svg",
    "cl_ipad":    f"{ROOT}/img/crossleaf.jpg",
    "cl_icon":    f"{DEV}/Mobile/crossleaf/site/img/appicon.png",
    "ks_month":   f"{DEV}/Mobile/kirisalim/store/shots/raw/iphone-en-ay.png",
    "ks_chat":    f"{DEV}/Mobile/kirisalim/store/shots/raw/iphone-en-1.png",
    "ks_icon":    f"{DEV}/Mobile/kirisalim/site/img/icon.png",
    "deskestra":  f"{ROOT}/img/deskestra.png",
    "kickkick":   f"{ROOT}/img/kickkick.png",
    "hoophoop":   f"{ROOT}/img/hoophoop.png",
}


def uri(key):
    path = SRC[key]
    mime = {"svg": "image/svg+xml", "jpg": "image/jpeg"}.get(path.rsplit(".", 1)[1], "image/png")
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


# ── grounds ──────────────────────────────────────────────────────────────────
MB_HUES = ["#e14cc4", "#f0a02c", "#33bff0", "#2fdd9b"]
MB_PADS = [(4, 6, 60, 0), (22, 2, 42, 1), (40, 10, 74, 2), (63, 3, 48, 3), (84, 9, 62, 0),
           (8, 34, 48, 3), (30, 40, 64, 0), (90, 34, 54, 1), (2, 62, 70, 2), (19, 82, 44, 1),
           (44, 76, 60, 3), (66, 86, 50, 0), (86, 70, 72, 2), (74, 50, 40, 3), (55, 44, 36, 1)]


def mb_ground(scale=1.0):
    pads = "".join(
        f'<i style="left:{x}%;top:{y}%;width:{s*scale:.0f}px;height:{s*scale:.0f}px;background:{MB_HUES[h]}"></i>'
        for x, y, s, h in MB_PADS)
    return f'<div class="g-mb">{pads}</div>'


KS_HUES = ["#1C9A8F", "#E8705A", "#F4C24D"]
KS_SLICES = [(-8, -14, 200, 0, 10), (70, -18, 150, 1, 250), (86, 58, 230, 1, 200), (-10, 66, 180, 2, 60),
             (44, 82, 120, 2, 140)]


def ks_ground(scale=1.0):
    s_ = "".join(
        f'<i style="left:{x}%;top:{y}%;width:{s*scale:.0f}px;height:{s*scale:.0f}px;transform:rotate({r}deg);'
        f'background:conic-gradient({KS_HUES[h]} 0 116deg, transparent 116deg)"></i>'
        for x, y, s, h, r in KS_SLICES)
    return f'<div class="g-ks">{s_}</div>'


# Crossleaf: faint pages fanned behind the device, each with a highlighter stroke — the search result
# is the product, so the ground is made of found words.
CL_PAGES = [(6, 10, -9), (74, 6, 7), (2, 58, 6), (80, 60, -8)]


def cl_ground(scale=1.0):
    pages = []
    for x, y, r in CL_PAGES:
        lines = "".join(f'<b style="width:{w}%"></b>' for w in (82, 64, 90, 40, 76, 58))
        pages.append(f'<i style="left:{x}%;top:{y}%;width:{150*scale:.0f}px;height:{196*scale:.0f}px;'
                     f'transform:rotate({r}deg)">{lines}<u></u></i>')
    return f'<div class="g-cl">{"".join(pages)}</div>'


CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { width:__W__px; height:__H__px; overflow:hidden; position:relative;
  font-family:-apple-system,"SF Pro Display","Helvetica Neue",sans-serif; -webkit-font-smoothing:antialiased; }
.stage { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }

.mb  { background:radial-gradient(90% 90% at 50% 50%, #17171c 0%, #08080a 75%); }
.g-mb { position:absolute; inset:-8%; transform:rotate(-14deg); opacity:.5; }
.g-mb i { position:absolute; border-radius:24%; opacity:.6; }

.cl  { background:radial-gradient(110% 110% at 70% 30%, #23334d 0%, #151d2b 50%, #0d121b 100%); }
.g-cl i { position:absolute; background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.08);
  border-radius:8px; padding:18px 14px; display:flex; flex-direction:column; gap:9px; }
.g-cl b { display:block; height:5px; border-radius:3px; background:rgba(255,255,255,.14); }
.g-cl u { position:absolute; left:14px; top:44px; width:46%; height:11px; border-radius:3px;
  background:#f4d03f; opacity:.55; }

.ks  { background:radial-gradient(120% 120% at 30% 40%, #0F5F58 0%, #0A3F3A 55%, #072B28 100%); }
.g-ks { position:absolute; inset:0; opacity:.24; }
.g-ks i { position:absolute; border-radius:50%; }

.body { position:relative; background:linear-gradient(150deg,#2b2c31,#141417 40%,#1b1c20);
  box-shadow:0 30px 70px rgba(0,0,0,.6), 0 0 0 1.5px rgba(255,255,255,.08), inset 0 1px 2px rgba(255,255,255,.16); }
.screen { overflow:hidden; line-height:0; background:#000; }
.screen img { display:block; width:100%; height:auto; }
.phone-l { padding:9px; border-radius:46px; } .phone-l .screen { border-radius:38px; }
.phone-p { padding:8px; border-radius:42px; } .phone-p .screen { border-radius:35px; }
.ipad    { padding:12px; border-radius:30px; } .ipad .screen { border-radius:19px; }

.badge { position:absolute; display:flex; align-items:center; gap:10px; padding:8px 14px 8px 8px;
  border-radius:16px; background:rgba(16,16,20,.72); border:1px solid rgba(255,255,255,.12);
  backdrop-filter:blur(10px); color:#fff; font-weight:700; font-size:17px; letter-spacing:-.2px; }
.badge img { width:34px; height:34px; border-radius:9px; display:block; }
"""


def render(name, w, h, body, scale=2, fmt="jpg"):
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS.replace('__W__', str(w)).replace('__H__', str(h))}</style>"
            f"</head>{body}</html>")
    src = os.path.join(OUT, f"_{name}.html")
    png = os.path.join(OUT, f"_{name}.png")
    with open(src, "w") as f:
        f.write(html)
    # Supersampled: drawn at three times the final density, then shrunk by sips. Chrome rotates a big
    # screenshot by sampling it without mipmaps, so a tilted device drawn straight at final size came
    # out pixelated (Safa, 2026-11-05); at 3× the source is barely shrunk, and sips does the real
    # downscale with proper filtering — the tilted edges get anti-aliased on the way down too.
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale * 3}", f"--screenshot={png}",
                    f"--window-size={w},{h}", "file://" + src], capture_output=True)
    os.remove(src)
    subprocess.run(["sips", "-z", str(h * scale), str(w * scale), png], capture_output=True)
    final = os.path.join(OUT, f"{name}.{fmt}")
    if fmt == "jpg":
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "93", png, "--out", final],
                       capture_output=True)
        os.remove(png)
    else:
        os.replace(png, final)
    print(" ", os.path.relpath(final, ROOT))


def badge(icon, label, pos):
    return f'<div class="badge" style="{pos}"><img src="{uri(icon)}">{label}</div>'


# ── per-product splashes (sit beside the text, 5:4) ──────────────────────────
W, H = 600, 480

render("splash-midiboard", W, H, f"""<body class="mb">{mb_ground()}
<div class="stage"><div class="body phone-l" style="width:540px;transform:rotate(-4deg)">
  <div class="screen"><img src="{uri('mb_surface')}"></div></div></div>
{badge('mb_icon', 'Midiboard', 'left:22px;top:22px')}</body>""")

render("splash-crossleaf", W, H, f"""<body class="cl">{cl_ground()}
<div class="stage"><div class="body ipad" style="width:470px">
  <div class="screen"><img src="{uri('cl_ipad')}"></div></div></div>
{badge('cl_icon', 'Crossleaf', 'left:22px;top:22px')}</body>""")

render("splash-kirisalim", W, H, f"""<body class="ks">{ks_ground()}
<div class="stage" style="gap:0">
  <div class="body phone-p" style="width:178px;transform:translate(34px,26px) rotate(-6deg);opacity:.92">
    <div class="screen"><img src="{uri('ks_chat')}"></div></div>
  <div class="body phone-p" style="width:196px;z-index:2;transform:translate(-10px,-6px) rotate(3deg)">
    <div class="screen"><img src="{uri('ks_month')}"></div></div>
</div>
{badge('ks_icon', 'Kırışalım', 'left:22px;top:22px')}</body>""")


# ── the family shot: three products' grounds as one strip, devices across the seams ─────────────
def family(w, h):
    # Three grounds side by side, each a third, so the colour of the picture *is* the line-up.
    third = w / 3
    grounds = (f'<div class="mb" style="position:absolute;left:0;top:0;width:{third+1:.0f}px;bottom:0;overflow:hidden">{mb_ground(.8)}</div>'
               f'<div class="cl" style="position:absolute;left:{third:.0f}px;top:0;width:{third+1:.0f}px;bottom:0;overflow:hidden">{cl_ground(.8)}</div>'
               f'<div class="ks" style="position:absolute;left:{2*third:.0f}px;top:0;right:0;bottom:0;overflow:hidden">{ks_ground(.8)}</div>')
    k = h / 540
    devices = f"""
<div class="body ipad" style="position:absolute;width:{430*k:.0f}px;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2">
  <div class="screen"><img src="{uri('cl_ipad')}"></div></div>
<div class="body phone-l" style="position:absolute;width:{440*k:.0f}px;left:{w*0.03:.0f}px;top:{h*0.52:.0f}px;transform:rotate(-5deg);z-index:3">
  <div class="screen"><img src="{uri('mb_surface')}"></div></div>
<div class="body phone-p" style="position:absolute;width:{170*k:.0f}px;right:{w*0.06:.0f}px;top:{h*0.17:.0f}px;transform:rotate(5deg);z-index:3">
  <div class="screen"><img src="{uri('ks_month')}"></div></div>"""
    icons = "".join(f'<img src="{uri(i)}">' for i in ("deskestra", "kickkick", "hoophoop"))
    toys = (f'<div class="badge" style="left:{w*0.03:.0f}px;top:{h*0.08:.0f}px;gap:8px;padding:8px 14px 8px 8px">'
            f'{icons}<span style="margin-left:4px">Desk toys for Mac</span></div>')
    return f"<body style='background:#0f0f10'>{grounds}{devices}{toys}</body>"


render("hero", 1080, 540, family(1080, 540))
render("og", 1200, 630, family(1200, 630), scale=1, fmt="png")
