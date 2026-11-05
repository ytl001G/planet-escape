# 배경 시안 (우주 말고): 부마다 색만 바꿔 SVG로 그림 → proto.py가 JS의 BGV로 넣음
import base64, math, json

PART = {'bg_pre': ('#e9e6ee', '#18171c', '#0c0b0f'), 'bg_part1': ('#cf86e6', '#1a1520', '#0b0910'), 'bg_part2': ('#ffae4d', '#1c1611', '#0c0a08')}
W, H = 360, 800

def wrap(body, c0, c1):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
         f'<defs><linearGradient id="b" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>'
         f'<radialGradient id="v" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient></defs>'
         f'<rect width="{W}" height="{H}" fill="url(#b)"/>{body}<rect width="{W}" height="{H}" fill="url(#v)"/></svg>')
    return 'url("data:image/svg+xml;base64,' + base64.b64encode(s.encode()).decode() + '")'

def topo(col):  # 등고선: 오른쪽 위와 왼쪽 아래 두 봉우리에서 퍼지는 물결 곡선
    out = []
    for cx, cy, n, op in ((300, 140, 16, .16), (40, 640, 12, .10)):
        for i in range(n):
            r = 26 + i * 24; pts = []
            for a in range(0, 361, 6):
                t = math.radians(a); rr = r * (1 + .10 * math.sin(3 * t + i * .7) + .05 * math.sin(5 * t - i))
                pts.append(f'{cx + rr * math.cos(t):.1f},{cy + rr * .82 * math.sin(t):.1f}')
            out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-opacity="{op * (1 - i / n * .6):.3f}" stroke-width="1"/>')
    return ''.join(out)

def hexa(col):  # 육각 무늬: 위쪽은 또렷, 아래로 갈수록 사라짐
    s, out = 22, []
    h = s * math.sqrt(3)
    for row in range(int(H / h) + 2):
        for colm in range(int(W / (s * 3)) + 2):
            x = colm * s * 3 + (row % 2) * s * 1.5; y = row * h / 2
            op = max(0, .13 * (1 - y / (H * .85)))
            if op <= .005: continue
            pts = ' '.join(f'{x + s * math.cos(math.radians(60 * k)):.1f},{y + s * math.sin(math.radians(60 * k)):.1f}' for k in range(6))
            out.append(f'<polygon points="{pts}" fill="none" stroke="{col}" stroke-opacity="{op:.3f}" stroke-width="1"/>')
    return ''.join(out)

def grain(col):  # 질감: 고운 노이즈 + 부 색 얼룩 두 개
    return (f'<defs><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .09 0"/></filter>'
            f'<filter id="s"><feGaussianBlur stdDeviation="60"/></filter></defs>'
            f'<g filter="url(#s)"><ellipse cx="290" cy="150" rx="150" ry="120" fill="{col}" opacity=".22"/><ellipse cx="60" cy="620" rx="140" ry="110" fill="{col}" opacity=".12"/></g>'
            f'<rect width="{W}" height="{H}" filter="url(#n)"/>')

import random

def stripe(col):  # 사선 줄무늬: 오른쪽 위에서 흐려지며 내려옴
    return (f'<defs><pattern id="p" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="2" height="14" fill="{col}"/></pattern>'
            f'<linearGradient id="f" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".32"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#f)"/></mask></defs><rect width="{W}" height="{H}" fill="url(#p)" mask="url(#m)"/>')

def dots(col):  # 점 무늬: 왼쪽 위 모서리에서 점이 커졌다 작아짐 (인쇄 망점처럼)
    out = []
    for y in range(0, H + 1, 14):
        for x in range(0, W + 1, 14):
            d = math.hypot(x, y * .7) / 520; r = max(0, 2.6 * (1 - d))
            if r > .25: out.append(f'<circle cx="{x}" cy="{y}" r="{r:.2f}"/>')
    return f'<g fill="{col}" fill-opacity=".26">{"".join(out)}</g>'

def radar(col):  # 동심원: 화면 아래 가운데에서 퍼지는 고리 + 눈금
    out = [f'<circle cx="180" cy="860" r="{r}" fill="none" stroke="{col}" stroke-opacity="{.30 - i * .02:.3f}" stroke-width="1"/>' for i, r in enumerate(range(90, 1000, 70))]
    out += [f'<line x1="180" y1="860" x2="{180 + 900 * math.cos(math.radians(a)):.0f}" y2="{860 - 900 * math.sin(math.radians(a)):.0f}" stroke="{col}" stroke-opacity=".05"/>' for a in range(20, 161, 20)]
    return ''.join(out)

def circuit(col):  # 회로 선: 꺾인 선과 끝점 (정해진 씨앗으로 늘 같은 모양)
    rnd, out = random.Random(7), []
    for _ in range(26):
        x, y = rnd.randrange(0, W, 20), rnd.randrange(0, H, 20); d = f'M{x} {y}'
        for _ in range(rnd.randint(2, 4)):
            if rnd.random() < .5: x += rnd.choice((-1, 1)) * rnd.randrange(40, 120, 20)
            else: y += rnd.choice((-1, 1)) * rnd.randrange(40, 160, 20)
            d += f'L{x} {y}'
        op = .10 + .18 * (1 - y / H if 0 < y < H else 0)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op:.3f}" stroke-width="1.2"/><circle cx="{x}" cy="{y}" r="2.4" fill="none" stroke="{col}" stroke-opacity="{op * 1.6:.3f}"/>')
    return ''.join(out)

def shards(col):  # 큰 조각: 반투명 삼각 · 사각 조각이 겹침
    rnd, out = random.Random(3), []
    for _ in range(9):
        cx, cy, s = rnd.uniform(-40, W + 40), rnd.uniform(-40, H * .75), rnd.uniform(120, 260)
        pts = ' '.join(f'{cx + s * math.cos(a):.0f},{cy + s * math.sin(a):.0f}' for a in sorted(rnd.uniform(0, 6.28) for _ in range(rnd.choice((3, 4)))))
        out.append(f'<polygon points="{pts}" fill="{col}" fill-opacity="{rnd.uniform(.03, .08):.3f}"/>')
    return ''.join(out)

def aurora(col):  # 물결 띠: 흐릿한 곡선 띠 세 줄
    out = [f'<defs><filter id="a"><feGaussianBlur stdDeviation="26"/></filter></defs><g filter="url(#a)">']
    for i, (y, op) in enumerate(((170, .30), (300, .18), (620, .12))):
        out.append(f'<path d="M-60 {y} C 80 {y - 90}, 220 {y + 90}, 420 {y - 30}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{46 - i * 8}"/>')
    return ''.join(out) + '</g>'

def scan(col):  # 화면 줄: 가로 주사선 + 고운 노이즈 + 위쪽 색
    return (f'<defs><pattern id="s" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity=".035"/></pattern>'
            f'<filter id="n"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .06 0"/></filter>'
            f'<radialGradient id="t" cx=".5" cy="0" r=".8"><stop offset="0" stop-color="{col}" stop-opacity=".18"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#t)"/><rect width="{W}" height="{H}" fill="url(#s)"/><rect width="{W}" height="{H}" filter="url(#n)"/>')

def mesh(col):  # 색 얼룩 여러 개: 부 색 + 옆 색을 흐리게 섞음
    alt = {'#cf86e6': '#6f7bf0', '#ffae4d': '#e5484d', '#e9e6ee': '#8a93a6'}[col]
    return (f'<defs><filter id="mb" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="70"/></filter></defs><g filter="url(#mb)">'
            f'<circle cx="300" cy="120" r="140" fill="{col}" opacity=".26"/><circle cx="40" cy="380" r="120" fill="{alt}" opacity=".16"/>'
            f'<circle cx="280" cy="700" r="130" fill="{col}" opacity=".14"/></g>')

def tiles(col):  # 큰 판: 우주선 벽판처럼 이음새 선 + 판마다 살짝 다른 밝기
    rnd, out = random.Random(5), []
    for y in range(0, H, 100):
        for x in range(0, W, 120):
            out.append(f'<rect x="{x + 1}" y="{y + 1}" width="118" height="98" rx="4" fill="#fff" fill-opacity="{rnd.uniform(0, .025):.3f}" stroke="{col}" stroke-opacity=".08"/>')
    return ''.join(out)

KINDS = {'topo': ('등고선', topo), 'hex': ('육각', hexa), 'grain': ('질감', grain), 'stripe': ('사선', stripe), 'dots': ('점', dots),
         'radar': ('동심원', radar), 'circuit': ('회로', circuit), 'shards': ('조각', shards), 'aurora': ('물결 띠', aurora),
         'scan': ('주사선', scan), 'mesh': ('색 얼룩', mesh), 'tiles': ('벽판', tiles)}
BGV = {v: {k: wrap(f(c), c0, c1) for k, (c, c0, c1) in PART.items()} for v, (_, f) in KINDS.items()}
JSDECL = 'const BGV = ' + json.dumps(BGV) + ';\n'
BUTTONS = ''.join(f'<button type="button" data-bgs="{v}" aria-pressed="false">{name}</button>' for v, (name, _) in KINDS.items())
assert all(len(BGV[v]) == 3 for v in BGV)
