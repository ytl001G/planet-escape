# 1부까지 쓰는 폰 에셋을 새로 그림 — '우주선 콘솔 HUD' 스타일 (모서리 깎은 판 · 눈금 링 · 선 2px 통일 · 글로우 없음)
# 글자 · 숫자 · 시각은 넣지 않음 (앱이 씀) — 틀 · 판 · 아이콘만
# SVG + PNG@3x(갤럭시 A13 1080px 폭 기준). 힌트폰 폴더에서: python assets_draw.py 에셋
import pathlib, re, subprocess, sys, html, math
SP = pathlib.Path(__file__).parent
OUT = (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('에셋')).resolve()
P, PL, PD = '#cf86e6', '#e6b6f3', '#9a4fb8'      # 1부 보라 (기본 · 밝게 · 어둡게)
W0 = '#e9e6ee'                                    # 안전 모드 전 흰 링
INK, MUTE, ERR, ALEX = '#f2eef6', 'rgba(242,238,246,.62)', '#e5484d', '#E57373'
FD, FB, FM = "'IBM Plex Sans KR','Malgun Gothic',sans-serif", "'Noto Sans KR','Malgun Gothic',sans-serif", "'IBM Plex Mono',monospace"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@500;700&family=Noto+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">'

DEFS = f'''<defs>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2233" stop-opacity=".92"/><stop offset="1" stop-color="#161119" stop-opacity=".92"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{PL}"/><stop offset="1" stop-color="{PD}"/></linearGradient>
<linearGradient id="accw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bdb8c6"/></linearGradient>
<radialGradient id="core" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#2b2234"/><stop offset="1" stop-color="#0f0c13"/></radialGradient>
<linearGradient id="btn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2f45"/><stop offset="1" stop-color="#241c2c"/></linearGradient>
</defs>'''
def svg(w, h, body, vb=None): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb or f"0 0 {w} {h}"}">{DEFS}{body}</svg>'
def T(x, y, t, size, weight=700, fam=FB, fill=INK, anchor='start', ls=0):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{html.escape(t)}</text>'
def cham(x, y, w, h, c):  # 모서리 깎은 팔각 판
    return f'M{x+c} {y}H{x+w-c}L{x+w} {y+c}V{y+h-c}L{x+w-c} {y+h}H{x+c}L{x} {y+h-c}V{y+c}Z'
def panel(w, h, c=10, acc=P, x=0, y=0, fill='url(#panel)', brackets=True, stroke='rgba(255,255,255,.16)'):
    s = f'<path d="{cham(x+1, y+1, w-2, h-2, c)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    if brackets:  # 왼쪽 위 · 오른쪽 아래 작은 꺾쇠 — 콘솔 창 느낌
        L = 9; s += (f'<path d="M{x+c+2} {y+4.5}H{x+c+2+L}M{x+4.5} {y+c+2}V{y+c+2+L}" stroke="{acc}" stroke-width="2" stroke-linecap="round" fill="none"/>'
                      f'<path d="M{x+w-c-2} {y+h-4.5}H{x+w-c-2-L}M{x+w-4.5} {y+h-c-2}V{y+h-c-2-L}" stroke="{acc}" stroke-width="2" stroke-linecap="round" fill="none"/>')
    return s
def ln(d, col='currentColor', w=2, extra=''):  # 아이콘 선은 currentColor → 내보낼 때 색을 바꿔 끼움
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

# ── 아이콘 (24 기준 · 선 2px) ──
IC = {
 '채팅': ln('M5 4.5h14a2.5 2.5 0 0 1 2.5 2.5v8a2.5 2.5 0 0 1-2.5 2.5h-8.5L6 21v-3.5H5A2.5 2.5 0 0 1 2.5 15V7A2.5 2.5 0 0 1 5 4.5Z') + '<circle cx="8.2" cy="11" r="1.5" fill="currentColor"/>' + ln('M11.6 8.6a3.4 3.4 0 0 1 0 4.8M14.4 6.3a6.6 6.6 0 0 1 0 9.4', w=1.8),  # 말풍선 + 송신 파동
 '핀': ln('M12 21.5c-4.5-5.2-7-8.6-7-11.8a7 7 0 0 1 14 0c0 3.2-2.5 6.6-7 11.8Z') + '<circle cx="12" cy="9.7" r="2.4" fill="currentColor"/>',
 '체크': ln('M5 12.5l4.5 4.5L19 7.5', w=2.6),
 '닫기': ln('M6 6l12 12M18 6L6 18', w=2.4),
 '꺾쇠': ln('M9 5l7 7-7 7', w=2.4),
 '뒤로': ln('M15 5l-7 7 7 7', w=2.4),
 '보내기': ln('M3.5 12h15M13 6l6 6-6 6', w=2.4),
 '지우기': ln('M9 4.5h10.5a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H9L2.5 12Z') + ln('M12 9l6 6M18 9l-6 6'),
 '시프트': ln('M12 3.5 4 12h4.5v8h7v-8H20Z'),
 '와이파이': '<path d="M12 19.2l2.9-3.4a4.3 4.3 0 0 0-5.8 0ZM12 9.4a10 10 0 0 1 7 2.8l1.6-1.8A12.4 12.4 0 0 0 12 7a12.4 12.4 0 0 0-8.6 3.4l1.6 1.8a10 10 0 0 1 7-2.8Zm0 3.5a6.6 6.6 0 0 1 4.6 1.8l1.5-1.8A9 9 0 0 0 12 10.4a9 9 0 0 0-6.1 2.3l1.5 1.8a6.6 6.6 0 0 1 4.6-1.8Z" fill="currentColor"/>',
 '와이파이_끊김': ln('M3.4 10.4A12.4 12.4 0 0 1 20.6 10.4M6.6 13.6a8 8 0 0 1 10.8 0', w=2, extra=' opacity=".4"') + '<circle cx="12" cy="18" r="1.8" fill="currentColor"/>' + ln('M4 4l16 16', w=2.2),
 '배터리': '<rect x="2.5" y="7.5" width="16" height="9" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6" opacity=".6"/><rect x="4.3" y="9.3" width="11" height="5.4" rx="1.3" fill="currentColor"/><rect x="19.8" y="10" width="1.8" height="4" rx=".9" fill="currentColor" opacity=".6"/>',
}
def ic(k, col, x=0, y=0, s=24): return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24" color="{col}">{IC[k]}</svg>'

A = {}
# ── 아이콘: 흰색(앱에서 색 입힘) · 1부에서 보라로 쓰는 건 보라판도 ──
for k, b in IC.items(): A[f'아이콘_{k}'] = svg(48, 48, b.replace('currentColor', INK), '0 0 24 24')
for k in ('채팅', '핀'): A[f'아이콘_{k}_1부'] = svg(48, 48, IC[k].replace('currentColor', P), '0 0 24 24'); A[f'아이콘_{k}_이전'] = svg(48, 48, IC[k].replace('currentColor', W0), '0 0 24 24')
A['아이콘_와이파이_끊김'] = svg(48, 48, IC['와이파이_끊김'].replace('currentColor', ERR), '0 0 24 24')

# ── 타이머 링: 틀(눈금 · 바탕 · 안쪽 링) + 진행 호(한 바퀴 · 앱이 남은 만큼만 그림) ── 글자는 앱이 씀
def ring_frame(dot):
    cx = 130; b = f'<circle cx="{cx}" cy="{cx}" r="100" fill="url(#core)"/>'
    for i in range(60):
        a = math.radians(i * 6 - 90); L = 9 if i % 5 == 0 else 4
        b += f'<line x1="{cx+120*math.cos(a):.1f}" y1="{cx+120*math.sin(a):.1f}" x2="{cx+(120+L)*math.cos(a):.1f}" y2="{cx+(120+L)*math.sin(a):.1f}" stroke="{INK}" stroke-opacity="{.55 if i%5==0 else .22}" stroke-width="{2 if i%5==0 else 1.2}" stroke-linecap="round"/>'
    b += f'<circle cx="{cx}" cy="{cx}" r="110" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="6"/><circle cx="{cx}" cy="{cx}" r="99" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1"/>'
    for a in (0, 90, 180, 270): r = math.radians(a - 90); b += f'<circle cx="{cx+99*math.cos(r):.1f}" cy="{cx+99*math.sin(r):.1f}" r="2.2" fill="{dot}"/>'
    return svg(260, 260, b)
A['타이머_링_틀_1부'] = ring_frame(P); A['타이머_링_틀_이전'] = ring_frame(W0)
for n, col in (('1부', P), ('이전', W0)): A[f'타이머_진행호_{n}'] = svg(260, 260, f'<circle cx="130" cy="130" r="110" fill="none" stroke="{col}" stroke-width="6"/>')
A['진행도_칸_빈'] = svg(8, 5, '<rect width="8" height="5" rx="1.5" fill="rgba(255,255,255,.14)"/>')
A['진행도_칸_1부'] = svg(8, 5, f'<rect width="8" height="5" rx="1.5" fill="{P}"/>'); A['진행도_칸_이전'] = svg(8, 5, f'<rect width="8" height="5" rx="1.5" fill="{W0}"/>')

# ── 판 · 칸 (글자 없음) ──
A['채팅_칸_틀_1부'] = svg(76, 76, panel(76, 76, 12)); A['채팅_칸_틀_이전'] = svg(76, 76, panel(76, 76, 12, W0))
A['목표_칸_틀_1부'] = svg(246, 76, panel(246, 76, 12) + '<rect x="12" y="16" width="3" height="44" rx="1.5" fill="url(#acc)"/>')
A['목표_칸_틀_빈'] = svg(246, 76, panel(246, 76, 12))
A['완료_체크_큰'] = svg(76, 76, '<circle cx="38" cy="38" r="36" fill="url(#acc)"/><circle cx="38" cy="38" r="30" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.5"/>' + ic('체크', '#1a1220', 18, 18, 40))
A['완료_체크_작은'] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="url(#acc)"/>' + ic('체크', '#1a1220', 6, 6, 20))
A['안읽음_배지'] = svg(22, 22, f'<circle cx="11" cy="11" r="10" fill="{ERR}" stroke="#1a1220" stroke-width="2"/>')
A['입력_판'] = svg(332, 78, panel(332, 78, 14, brackets=False))
def field(err=False):
    return svg(212, 54, f'<path d="{cham(1, 1, 210, 52, 8)}" fill="#120e16" stroke="{ERR if err else "rgba(255,255,255,.22)"}" stroke-width="1.5"/><path d="M12 45H200" stroke="{ERR if err else "rgba(255,255,255,.14)"}" stroke-width="1" stroke-dasharray="6 5"/>')
A['입력_칸'] = field(); A['입력_칸_오류'] = field(True)
def bt(w, h, fill='url(#btn)', stroke='rgba(255,255,255,.22)'): return svg(w, h, f'<path d="{cham(1, 1, w-2, h-2, 8)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
A['버튼_작은'] = bt(84, 54); A['버튼_작은_눌림'] = bt(84, 54, 'rgba(207,134,230,.35)', P)
A['버튼_넓은'] = bt(308, 52); A['버튼_넓은_눌림'] = bt(308, 52, 'rgba(207,134,230,.35)', P)
A['버튼_정답'] = bt(308, 52, 'url(#accw)', 'rgba(255,255,255,.5)')
A['힌트_카드_틀_1부'] = svg(308, 70, f'<path d="{cham(1, 1, 306, 68, 10)}" fill="rgba(70,46,84,.45)" stroke="{P}" stroke-width="1.5"/><rect x="12" y="16" width="3" height="38" rx="1.5" fill="url(#acc)"/>')
A['정답_칸_틀'] = svg(308, 70, f'<path d="{cham(1, 1, 306, 68, 10)}" fill="url(#accw)" stroke="rgba(255,255,255,.5)" stroke-width="1.5"/>')
A['팝업_틀'] = svg(348, 220, panel(348, 220, 16, fill='#1a151f') + '<path d="M22 60H326" stroke="rgba(255,255,255,.12)" stroke-width="1"/>')
A['덮개_어둡게'] = svg(8, 8, '<rect width="8" height="8" fill="rgba(0,0,0,.55)"/>')

# ── 키보드 (글자 없음) ──
def k(w, fill='#2b2433'): return svg(w, 42, f'<path d="{cham(.75, .75, w-1.5, 40.5, 5)}" fill="{fill}" stroke="rgba(255,255,255,.14)" stroke-width="1.5"/>')
A['키_기본'] = k(30); A['키_숫자줄'] = k(30, '#1f1a25'); A['키_눌림_1부'] = k(30, 'url(#acc)'); A['키_넓은'] = k(52, '#1f1a25'); A['키_띄어쓰기'] = k(170)
A['키보드_판'] = svg(360, 220, '<path d="M0 20Q0 0 20 0H340Q360 0 360 20V220H0Z" fill="url(#panel)" stroke="rgba(255,255,255,.12)" stroke-width="1.5"/>')

OUT.mkdir(parents=True, exist_ok=True)
for f in OUT.glob('*'): f.unlink()
for n, s in A.items(): (OUT / f'{n}.svg').write_text(s, encoding='utf-8')
E = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'; tmp = SP / 'aout'; tmp.mkdir(exist_ok=True)
for n, s in A.items():
    w, h = map(int, re.match(r'<svg[^>]*width="(\d+)" height="(\d+)"', s).groups())
    (tmp / f'{n}.html').write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}svg{{display:block}}</style></head><body>{s}</body></html>', encoding='utf-8')
    try: subprocess.run([E, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={tmp / ("prof_" + str(abs(hash(n))))}', '--hide-scrollbars', '--force-device-scale-factor=3', '--default-background-color=00000000',
                         f'--window-size={w},{h}', '--virtual-time-budget=500', f'--screenshot={OUT / (n + "@3x.png")}', (tmp / f'{n}.html').as_uri()], capture_output=True, timeout=60)
    except subprocess.TimeoutExpired: print('timeout', n)
print('assets', len(A), '→', OUT)
