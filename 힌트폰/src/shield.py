# 보라 방패 로고 3안 (512x512 SVG). 릴리의 안전 모드 프로그램 상징.
import pathlib, sys
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(exist_ok=True)

SHIELD = 'M256 40 L432 104 V236 C432 352 356 432 256 472 C156 432 80 352 80 236 V104 Z'
def inner(k=0.84, cx=256, cy=256):
    return f'<path d="{SHIELD}" transform="translate({cx*(1-k)} {cy*(1-k)+6}) scale({k})" fill="none" stroke="#f3dcfa" stroke-opacity=".38" stroke-width="{4/k:.1f}"/>'

def base(uid, glow=True):
    g = (f'<filter id="{uid}-glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="18"/></filter>'
         if glow else '')
    defs = (f'<defs><linearGradient id="{uid}-fill" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#a646c8"/><stop offset=".55" stop-color="#6a2286"/><stop offset="1" stop-color="#3a1248"/></linearGradient>'
            f'<linearGradient id="{uid}-edge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1c9fb"/><stop offset="1" stop-color="#b864d6"/></linearGradient>'
            f'<linearGradient id="{uid}-shine" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'{g}</defs>')
    body = ''
    if glow:
        body += f'<path d="{SHIELD}" fill="#cf86e6" opacity=".55" filter="url(#{uid}-glow)"/>'
    body += (f'<path d="{SHIELD}" fill="url(#{uid}-fill)" stroke="url(#{uid}-edge)" stroke-width="12" stroke-linejoin="round"/>'
             + inner()
             + f'<path d="M256 52 L420 112 V236 C420 250 419 263 417 276 C340 220 256 196 92 196 V112 Z" fill="url(#{uid}-shine)"/>')
    return defs, body

WHITE = '#fbf3fe'
# A. 백합: 릴리(Lily) 이름에서 — 꽃잎 세 장
lily = (f'<path d="M256 150 C226 196 224 262 256 310 C288 262 286 196 256 150 Z" fill="{WHITE}"/>'
        f'<path d="M250 304 C204 296 162 256 156 200 C194 216 234 254 250 304 Z" fill="{WHITE}" opacity=".92"/>'
        f'<path d="M262 304 C308 296 350 256 356 200 C318 216 278 254 262 304 Z" fill="{WHITE}" opacity=".92"/>'
        f'<path d="M256 308 V380" stroke="{WHITE}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M256 360 C236 344 214 342 198 350 C214 366 236 370 256 360 Z" fill="{WHITE}" opacity=".85"/>')
# B. 회로: 안전 모드 '프로그램'
def node(x, y, r=11): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}"/>'
circ = (f'<g fill="none" stroke="{WHITE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M256 214 V150"/><path d="M234 262 H190 L170 242 V196"/><path d="M278 262 H322 L342 242 V196"/>'
        '<path d="M240 286 L210 316 V356"/><path d="M272 286 L302 316 V356"/><path d="M256 290 V392"/></g>'
        + f'<circle cx="256" cy="256" r="40" fill="none" stroke="{WHITE}" stroke-width="10"/>' + node(256, 256, 14)
        + node(256, 146) + node(170, 192) + node(342, 192) + node(210, 360) + node(302, 360) + node(256, 396, 9))
# C. 잠금: 안전 모드로 '잠긴' 우주선
lock = (f'<circle cx="256" cy="226" r="46" fill="{WHITE}"/>'
        f'<path d="M232 254 L216 352 H296 L280 254 Z" fill="{WHITE}"/>'
        f'<circle cx="256" cy="226" r="16" fill="#4a1a5e" opacity=".9"/>')

VARIANTS = {'shield_plain': ('무늬 없음', '')}  # 백합·회로·열쇠 구멍 안은 사용자 요청으로 지움

def svg(uid, mark, glow=True, size=512):
    d, b = base(uid, glow)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{size}" height="{size}">' + d + b + mark + '</svg>')

for name, (label, mark) in VARIANTS.items():
    (OUT / f'{name}.svg').write_text(svg(name, mark), encoding='utf-8')
    (OUT / f'{name}_flat.svg').write_text(svg(name + 'f', mark, glow=False), encoding='utf-8')  # 빛 번짐 없는 판 (작은 크기용)

# 확인용: 어두운/밝은 바탕 × 큰/작은 크기
rows = ''
for name, (label, mark) in VARIANTS.items():
    cells = ''
    for bg in ('#17151b', '#2a1733', '#f7f6f9'):
        cells += (f'<div style="background:{bg};padding:18px;border-radius:14px;display:flex;gap:18px;align-items:center">'
                  + svg(name + bg[1:] + 'a', mark, True, 180) + svg(name + bg[1:] + 'b', mark, False, 64) + svg(name + bg[1:] + 'c', mark, False, 32) + '</div>')
    rows += f'<div style="display:flex;gap:14px;align-items:center"><b style="width:110px;color:#ece9f1;font:700 18px Malgun Gothic">{label}</b>{cells}</div>'
pathlib.Path(sys.argv[2]).write_text(f'<!DOCTYPE html><html><body style="margin:0;padding:20px;background:#0f0d12;display:grid;gap:16px">{rows}</body></html>', encoding='utf-8')
print('ok', sorted(p.name for p in OUT.iterdir()))
