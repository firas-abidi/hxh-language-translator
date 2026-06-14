import sys, io, base64, json, re, numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IMG11   = r'C:\Users\firas\Downloads\hxh language\1.1.jpg'
JS_PATH = r'C:\Users\firas\Downloads\hxh_sprites.js'
GOLD = (212, 184, 96)
CELL = 64

# Calibrated positions from build_final.py (known-good)
ROW_CROP = {
    'A':(104,154),'KA':(224,274),'SA':(343,393),'TA':(463,513),'NA':(583,633),
    'HA':(703,753),'MA':(823,873),'YA':(943,993),'RA':(1063,1113),
    'WA':(1183,1233),'N':(1303,1353),'GA':(1423,1473),'ZA':(1543,1593),
    'DA':(1663,1713),'BA':(1783,1833),'PA':(1903,1953),
}
COL_SX = {'A':119,'I':187,'U':253,'E':321,'O':388}

# ── Load all current sprites ──────────────────────────────────────────────────
print("Loading sprites...")
with open(JS_PATH,'r',encoding='utf-8') as f:
    js_text = f.read()

sprites = {}  # kana -> b64 string (no header)
for kana, b64 in re.findall(r'"([^"]+)":\s*"data:image/png;base64,([A-Za-z0-9+/=]+)"', js_text):
    sprites[kana] = b64
print(f"  {len(sprites)} loaded")

# ── Step 1: Pure swaps (correct sprites exist, just on wrong kana) ────────────
print("Applying swaps...")
# Load the three sprites we're redistributing before touching anything
sprite_ho = sprites['ほ']   # currently ●  → goes to り
sprite_ma = sprites['ま']   # currently ⊕  → goes to ほ
sprite_u  = sprites['う']   # currently person → goes to ろ

sprites['り'] = sprite_ho   # り gets ● ✓
sprites['ほ'] = sprite_ma   # ほ gets ⊕ ✓
sprites['ろ'] = sprite_u    # ろ gets person figure ✓
print("  り ← ほ (●)")
print("  ほ ← ま (⊕)")
print("  ろ ← う (person)")

# ── Step 2: Fresh extractions from img1.1 (calibrated positions) ─────────────
# These kana got wrong img2 matches — force the correct img1.1 template instead
FRESH = {
    'い': ('A',  'I'),   # single dot
    'う': ('A',  'U'),   # single arch ∩
    'ぬ': ('NA', 'U'),   # double arch ∩∩
    'つ': ('TA', 'U'),   # U-shape + 3 strokes
    'ま': ('MA', 'A'),   # W/M zigzag
    'よ': ('YA', 'O'),   # ring with tail
}

img11 = Image.open(IMG11).convert('RGB')
arr11 = np.array(img11)
W11   = img11.width

def extract_from_img11(row_key, col_key):
    y1, y2 = ROW_CROP[row_key]
    sx     = COL_SX[col_key]
    x1 = max(0, sx-38); x2 = min(W11, sx+38)
    gray   = np.array(Image.fromarray(arr11[y1:y2, x1:x2]).convert('L'))
    binary = (255-gray > 150).astype(np.uint8) * 255
    return normalize(binary)

def normalize(b, pad=5):
    s  = Image.fromarray(b)
    bb = s.getbbox()
    if not bb or bb[2]-bb[0] < 4 or bb[3]-bb[1] < 4: return None
    bx1=max(0,bb[0]-pad); by1=max(0,bb[1]-pad)
    bx2=min(s.width,bb[2]+pad); by2=min(s.height,bb[3]+pad)
    t = s.crop((bx1,by1,bx2,by2)); tw,th = t.size; side = max(tw,th)
    sq = Image.new('L',(side,side),0)
    sq.paste(t,((side-tw)//2,(side-th)//2))
    return np.array(sq.resize((CELL,CELL), Image.LANCZOS))

def to_rgba(mask):
    r = np.zeros((CELL,CELL,4),dtype=np.uint8)
    r[:,:,0]=GOLD[0]; r[:,:,1]=GOLD[1]; r[:,:,2]=GOLD[2]; r[:,:,3]=mask
    return Image.fromarray(r,'RGBA')

def enc(img):
    buf = io.BytesIO(); img.save(buf,format='PNG')
    return base64.b64encode(buf.getvalue()).decode()

ROM = {'い':'i','う':'u','ぬ':'nu','つ':'tsu','ま':'ma','よ':'yo'}

print("Extracting fresh from img1.1...")
for kana,(row,col) in FRESH.items():
    mask = extract_from_img11(row, col)
    if mask is None:
        print(f"  WARN: {kana} empty — skipping")
        continue
    sprites[kana] = enc(to_rgba(mask))
    print(f"  OK  {kana} ({ROM[kana]})")

# ── Write JS ──────────────────────────────────────────────────────────────────
BASE_KANA = [
    'あ','い','う','え','お',
    'か','き','く','け','こ',
    'さ','し','す','せ','そ',
    'た','ち','つ','て','と',
    'な','に','ぬ','ね','の',
    'は','ひ','ふ','へ','ほ',
    'ま','み','む','め','も',
    'や','ゆ','よ',
    'ら','り','る','れ','ろ',
    'わ','を','ん',
    'が','ぎ','ぐ','げ','ご',
    'ざ','じ','ず','ぜ','ぞ',
    'だ','ぢ','づ','で','ど',
    'ば','び','ぶ','べ','ぼ',
    'ぱ','ぴ','ぷ','ぺ','ぽ',
]

print(f"Writing {JS_PATH}...")
with open(JS_PATH,'w',encoding='utf-8') as f:
    f.write('const SPRITES = {\n')
    for kana in BASE_KANA:
        if kana in sprites:
            f.write(f'  {json.dumps(kana,ensure_ascii=False)}: "data:image/png;base64,{sprites[kana]}",\n')
    f.write('};\n')
print("Done.")
