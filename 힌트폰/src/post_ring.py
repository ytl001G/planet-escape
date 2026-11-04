# 예전 손그림 화면의 네모 타이머 칸 → 둥근 링 (남은 시간만큼, 1:45:00 기준). 아래 안내 칸은 링 높이만큼 내림
import pathlib, re, sys
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
COL = {'lily': '#cf86e6', 'via': '#ffae4d'}
def ring(cx, cy, r, w, f, col):
    return (f'<circle cx="{cx:g}" cy="{cy}" r="{r}" fill="rgba(12,10,16,.35)" stroke="currentColor" stroke-opacity=".15" stroke-width="{w}"/>'
            f'<circle cx="{cx:g}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" pathLength="100" stroke-dasharray="{100*f:.1f} 100" transform="rotate(-90 {cx:g} {cy})"/>')
def frac(t):
    m = re.fullmatch(r'(\d+):(\d\d):(\d\d)', t); return min(1, (int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])) / 6300) if m else 1
# (큰 그림 y52 h58 → 링 r40, 작은 그림 y30 h44 → 링 r30) · 바로 뒤 안내 칸 시작을 링 아래로
SIZES = {('52', '210'): (86, 34, 4, 12.5, 90.5, None), ('30', '168'): (54, 24, 3, 9, 57, None)}  # 안내 칸은 그대로 (안의 글자 위치가 고정이라)
pat = re.compile(r'<rect x="(\d+)" y="(52|30)" width="(210|168)" height="(?:58|44)" rx="(?:10|8)" class="soft"/>(\s*)<text x="[\d.]+" y="[\d.]+" text-anchor="middle" font-size="\d+" font-weight="700">([^<]*)</text>(\s*)<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" rx="(\d+)" class="(lily|via)"/>')
def rep(m):
    x, y, w, sp1, t, sp2, gx, gy, gw, gh, grx, cls = m.groups()
    cy, r, sw, fs, ty, ny = SIZES[(y, w)]; ny = int(gy); cx = int(x) + int(w) / 2
    return (ring(cx, cy, r, sw, frac(t), COL[cls]) + sp1 + f'<text x="{cx:g}" y="{ty}" text-anchor="middle" font-size="{fs}" font-weight="700">{t}</text>' + sp2
            + f'<rect x="{gx}" y="{ny}" width="{gw}" height="{int(gh) - (ny - int(gy))}" rx="{grx}" class="{cls}"/>')
print([m.group(1, 2, 6) for m in pat.finditer(s)]); s, n = pat.subn(rep, s); assert n == 6, n
p.write_text(s, encoding='utf-8'); print('timer rings', n)
