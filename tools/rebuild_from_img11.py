import sys, io, base64, json, numpy as np
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IMG11  = r'C:\Users\firas\Downloads\hxh language\1.1.jpg'
JS_OUT = r'C:\Users\firas\Downloads\hxh_sprites.js'

GOLD = (212, 184, 96)
CELL = 64

ROW_CROP = {
    'A':(104,154),'KA':(224,274),'SA':(343,393),'TA':(463,513),'NA':(583,633),
    'HA':(703,753),'MA':(823,873),'YA':(943,993),'RA':(1063,1113),
    'WA':(1183,1233),'N':(1303,1353),'GA':(1423,1473),'ZA':(1543,1593),
    'DA':(1663,1713),'BA':(1783,1833),'PA':(1903,1953),
}
COL_SX = {'A':119,'I':187,'U':253,'E':321,'O':388}

GRID = {
    ('A','A'):'あ',('A','I'):'い',('A','U'):'う',('A','E'):'え',('A','O'):'お',
    ('KA','A'):'か',('KA','I'):'き',('KA','U'):'く',('KA','E'):'け',('KA','O'):'こ',
    ('SA','A'):'さ',('SA','I'):'し',('SA','U'):'す',('SA','E'):'せ',('SA','O'):'そ',
    ('TA','A'):'た',('TA','I'):'ち',('TA','U'):'つ',('TA','E'):'て',('TA','O'):'と',
    ('NA','A'):'な',('NA','I'):'に',('NA','U'):'ぬ',('NA','E'):'ね',('NA','O'):'の',
    ('HA','A'):'は',('HA','I'):'ひ',('HA','U'):'ふ',('HA','E'):'へ',('HA','O'):'ほ',
    ('MA','A'):'ま',('MA','I'):'み',('MA','U'):'む',('MA','E'):'め',('MA','O'):'も',
    ('YA','A'):'や',                ('YA','U'):'ゆ',               ('YA','O'):'よ',
    ('RA','A'):'ら',('RA','I'):'り',('RA','U'):'る',('RA','E'):'れ',('RA','O'):'ろ',
    ('WA','A'):'わ',                                               ('WA','O'):'を',
    ('N','A'):'ん',
    ('GA','A'):'が',('GA','I'):'ぎ',('GA','U'):'ぐ',('GA','E'):'げ',('GA','O'):'ご',
    ('ZA','A'):'ざ',('ZA','I'):'じ',('ZA','U'):'ず',('ZA','E'):'ぜ',('ZA','O'):'ぞ',
    ('DA','A'):'だ',('DA','I'):'ぢ',('DA','U'):'づ',('DA','E'):'で',('DA','O'):'ど',
    ('BA','A'):'ば',('BA','I'):'び',('BA','U'):'ぶ',('BA','E'):'べ',('BA','O'):'ぼ',
    ('PA','A'):'ぱ',('PA','I'):'ぴ',('PA','U'):'ぷ',('PA','E'):'ぺ',('PA','O'):'ぽ',
}

ROM = {
    'あ':'a','い':'i','う':'u','え':'e','お':'o',
    'か':'ka','き':'ki','く':'ku','け':'ke','こ':'ko',
    'さ':'sa','し':'shi','す':'su','せ':'se','そ':'so',
    'た':'ta','ち':'chi','つ':'tsu','て':'te','と':'to',
    'な':'na','に':'ni','ぬ':'nu','ね':'ne','の':'no',
    'は':'ha','ひ':'hi','ふ':'fu','へ':'he','ほ':'ho',
    'ま':'ma','み':'mi','む':'mu','め':'me','も':'mo',
    'や':'ya','ゆ':'yu','よ':'yo',
    'ら':'ra','り':'ri','る':'ru','れ':'re','ろ':'ro',
    'わ':'wa','を':'wo','ん':'n',
    'が':'ga','ぎ':'gi','ぐ':'gu','げ':'ge','ご':'go',
    'ざ':'za','じ':'ji','ず':'zu','ぜ':'ze','ぞ':'zo',
    'だ':'da','ぢ':'di','づ':'du','で':'de','ど':'do',
    'ば':'ba','び':'bi','ぶ':'bu','べ':'be','ぼ':'bo',
    'ぱ':'pa','ぴ':'pi','ぷ':'pu','ぺ':'pe','ぽ':'po',
}
BASE_KANA = list(ROM.keys())

img11 = Image.open(IMG11).convert('RGB')
arr11 = np.array(img11)
W11   = img11.width

def extract(row_key, col_key):
    y1, y2 = ROW_CROP[row_key]
    sx     = COL_SX[col_key]
    x1 = max(0, sx - 38); x2 = min(W11, sx + 38)
    gray   = np.array(Image.fromarray(arr11[y1:y2, x1:x2]).convert('L'))
    binary = (255 - gray > 150).astype(np.uint8) * 255
    return normalize(binary)

def normalize(b, pad=5):
    s  = Image.fromarray(b)
    bb = s.getbbox()
    if not bb or bb[2]-bb[0] < 4 or bb[3]-bb[1] < 4:
        return None
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

# Build reverse map: kana -> (row, col)
kana_to_rc = {v: k for k, v in GRID.items()}

print("Extracting all 71 from img1.1...")
sprites = {}
empty = []
for kana in BASE_KANA:
    if kana not in kana_to_rc:
        print(f"  SKIP {kana} (not in GRID)")
        continue
    row, col = kana_to_rc[kana]
    mask = extract(row, col)
    if mask is None:
        print(f"  WARN {ROM[kana]} ({kana}) — empty extraction")
        empty.append(kana)
        mask = np.zeros((CELL,CELL), dtype=np.uint8)
    sprites[kana] = enc(to_rgba(mask))

print(f"  {len(sprites)} extracted, {len(empty)} empty")

print(f"Writing {JS_OUT}...")
with open(JS_OUT,'w',encoding='utf-8') as f:
    f.write('const SPRITES = {\n')
    for kana in BASE_KANA:
        if kana in sprites:
            f.write(f'  {json.dumps(kana,ensure_ascii=False)}: "data:image/png;base64,{sprites[kana]}",\n')
    f.write('};\n')
print("Done.")
