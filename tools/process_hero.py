import os, numpy as np
from PIL import Image, ImageOps, ImageFilter

SRC = r'C:/Users/firas/Downloads/kikikikiko'
OUT = r'C:/Users/firas/Downloads/assets'
os.makedirs(OUT, exist_ok=True)

GOLD  = np.array([198, 159, 78])
PARCH = np.array([214, 203, 182])
INK   = np.array([22, 18, 13])

# ── image 1: Togashi's dog doodle → gold line art on transparent ──────────────
d = Image.open(f'{SRC}/image 1.jpg').convert('L')
# trim the photo border / paper a touch via autocontrast
d = ImageOps.autocontrast(d, cutoff=1)
a = np.array(d).astype(float)
# lines are dark (<~130); paper is light. alpha ramps in for dark pixels.
alpha = np.clip((140 - a) / 70, 0, 1) ** 0.85 * 255
rgba = np.zeros((*a.shape, 4), np.uint8)
rgba[:, :, 0], rgba[:, :, 1], rgba[:, :, 2] = GOLD
rgba[:, :, 3] = alpha.astype(np.uint8)
Image.fromarray(rgba, 'RGBA').save(f'{OUT}/emblem_dog.png')
print('emblem_dog.png', rgba.shape)

# ── image 2: Togashi portrait → gold duotone, vignette + tonal fade ───────────
p = Image.open(f'{SRC}/image 2.jpg').convert('L')
p = ImageOps.autocontrast(p, cutoff=2)
v = np.array(p).astype(float) / 255.0
rgb = (INK[None, None, :] * (1 - v[:, :, None]) + GOLD[None, None, :] * v[:, :, None]).astype(np.uint8)
h, w = v.shape
yy, xx = np.mgrid[0:h, 0:w]
cx, cy = w * 0.46, h * 0.42
dist = np.sqrt(((xx - cx) / (w * 0.60)) ** 2 + ((yy - cy) / (h * 0.60)) ** 2)
vig = np.clip(1.25 - dist, 0, 1)
alpha = (vig * (0.32 + 0.68 * v) * 255).astype(np.uint8)   # dark suit melts away
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save(f'{OUT}/portrait_togashi.png')
print('portrait_togashi.png', (h, w))

# ── image 3: Gon panel → parchment glow line art, side fade ───────────────────
g = Image.open(f'{SRC}/image 3.png').convert('L')
g = ImageOps.autocontrast(g, cutoff=1)
v = np.array(g).astype(float) / 255.0
rgb = np.zeros((*v.shape, 3), np.uint8)
rgb[:, :] = PARCH
alpha = np.clip((v - 0.16) / 0.84, 0, 1) ** 0.9 * 255
h, w = v.shape
xfade = np.clip(1.35 - np.abs(np.linspace(-1, 1, w))[None, :] ** 3, 0, 1)
yfade = np.clip(1.35 - np.abs(np.linspace(-1, 1, h))[:, None] ** 3, 0, 1)
alpha = (alpha * xfade * yfade).astype(np.uint8)
Image.fromarray(np.dstack([rgb, alpha]), 'RGBA').save(f'{OUT}/panel_gon.png')
print('panel_gon.png', (h, w))
print('done')
