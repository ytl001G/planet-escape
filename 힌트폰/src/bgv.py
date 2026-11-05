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

KINDS = {'topo': ('등고선', topo), 'hex': ('육각', hexa), 'grain': ('질감', grain)}
BGV = {v: {k: wrap(f(c), c0, c1) for k, (c, c0, c1) in PART.items()} for v, (_, f) in KINDS.items()}
JSDECL = 'const BGV = ' + json.dumps(BGV) + ';\n'
BUTTONS = ''.join(f'<button type="button" data-bgs="{v}" aria-pressed="false">{name}</button>' for v, (name, _) in KINDS.items())
assert all(len(BGV[v]) == 3 for v in BGV)
