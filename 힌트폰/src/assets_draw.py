# 폰 에셋 — '우주선 콘솔 HUD' 스타일 (모서리 깎은 판 · 눈금 링 · 선 2px 통일 · 글로우 없음)
# 글자 · 숫자 · 시각은 넣지 않음 (앱이 씀) — 틀 · 판 · 아이콘만. 부마다 색만 바꿔 같은 모양으로 뽑음
# SVG + PNG@3x(갤럭시 A13 1080px 폭 기준). 힌트폰 폴더에서: python assets_draw.py 에셋 [--svg-only]
import pathlib, re, subprocess, sys, math
SP = pathlib.Path(__file__).parent
args = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = (pathlib.Path(args[0]) if args else pathlib.Path('에셋')).resolve()
PART = {  # 부 → (기본, 밝게, 어둡게, 카드 바탕, 눌림 바탕)
    '1부': ('#cf86e6', '#e6b6f3', '#9a4fb8', 'rgba(70,46,84,.45)', 'rgba(207,134,230,.35)'),
    '2부': ('#ffae4d', '#ffd29a', '#c9761f', 'rgba(84,56,28,.45)', 'rgba(255,174,77,.32)'),
    '이전': ('#e9e6ee', '#ffffff', '#a9a4b2', 'rgba(60,56,66,.45)', 'rgba(233,230,238,.22)'),
}
INK, ERR = '#f2eef6', '#e5484d'

def defs(p):
    c, l, d = PART[p][:3]
    return (f'<defs><linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2233" stop-opacity=".92"/><stop offset="1" stop-color="#161119" stop-opacity=".92"/></linearGradient>'
            f'<linearGradient id="acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{l}"/><stop offset="1" stop-color="{d}"/></linearGradient>'
            '<linearGradient id="accw" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bdb8c6"/></linearGradient>'
            '<radialGradient id="core" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="#2b2234"/><stop offset="1" stop-color="#0f0c13"/></radialGradient>'
            '<linearGradient id="btn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2f45"/><stop offset="1" stop-color="#241c2c"/></linearGradient></defs>')
def svg(w, h, body, vb=None, p='1부'): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb or f"0 0 {w} {h}"}">{defs(p)}{body}</svg>'
def cham(x, y, w, h, c):  # 모서리 깎은 팔각 판
    return f'M{x+c} {y}H{x+w-c}L{x+w} {y+c}V{y+h-c}L{x+w-c} {y+h}H{x+c}L{x} {y+h-c}V{y+c}Z'
def panel(w, h, c=10, acc=None, fill='url(#panel)', brackets=True):
    s = f'<path d="{cham(1, 1, w-2, h-2, c)}" fill="{fill}" stroke="rgba(255,255,255,.16)" stroke-width="1.5"/>'
    if brackets:  # 왼쪽 위 · 오른쪽 아래 작은 꺾쇠 — 콘솔 창 느낌
        L = 9; s += (f'<path d="M{c+2} 4.5H{c+2+L}M4.5 {c+2}V{c+2+L}" stroke="{acc}" stroke-width="2" stroke-linecap="round" fill="none"/>'
                      f'<path d="M{w-c-2} {h-4.5}H{w-c-2-L}M{w-4.5} {h-c-2}V{h-c-2-L}" stroke="{acc}" stroke-width="2" stroke-linecap="round" fill="none"/>')
    return s
def ln(d, w=2, extra=''): return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
def dot(x, y, r): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="currentColor"/>'

# ── 아이콘 (24 기준 · 선 2px · currentColor) ──
IC = {
 '핀': ln('M12 21.5c-4.5-5.2-7-8.6-7-11.8a7 7 0 0 1 14 0c0 3.2-2.5 6.6-7 11.8Z') + dot(12, 9.7, 2.4),
 '체크': ln('M5 12.5l4.5 4.5L19 7.5', 2.6), '닫기': ln('M6 6l12 12M18 6L6 18', 2.4), '꺾쇠': ln('M9 5l7 7-7 7', 2.4),
 '뒤로': ln('M15 5l-7 7 7 7', 2.4), '보내기': ln('M3.5 12h15M13 6l6 6-6 6', 2.4),
 '지우기': ln('M9 4.5h10.5a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H9L2.5 12Z') + ln('M12 9l6 6M18 9l-6 6'), '시프트': ln('M12 3.5 4 12h4.5v8h7v-8H20Z'),
 '와이파이': '<path d="M12 19.2l2.9-3.4a4.3 4.3 0 0 0-5.8 0ZM12 9.4a10 10 0 0 1 7 2.8l1.6-1.8A12.4 12.4 0 0 0 12 7a12.4 12.4 0 0 0-8.6 3.4l1.6 1.8a10 10 0 0 1 7-2.8Zm0 3.5a6.6 6.6 0 0 1 4.6 1.8l1.5-1.8A9 9 0 0 0 12 10.4a9 9 0 0 0-6.1 2.3l1.5 1.8a6.6 6.6 0 0 1 4.6-1.8Z" fill="currentColor"/>',
 '와이파이_끊김': ln('M3.4 10.4A12.4 12.4 0 0 1 20.6 10.4M6.6 13.6a8 8 0 0 1 10.8 0', 2, ' opacity=".4"') + dot(12, 18, 1.8) + ln('M4 4l16 16', 2.2),
 '배터리': '<rect x="2.5" y="7.5" width="16" height="9" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.6" opacity=".6"/><rect x="4.3" y="9.3" width="11" height="5.4" rx="1.3" fill="currentColor"/><rect x="19.8" y="10" width="1.8" height="4" rx=".9" fill="currentColor" opacity=".6"/>',
}
# 채팅 아이콘 시안 — 운영자(우주선 관제)와 통신하는 느낌
CHAT = {
 'A': ln('M6 4h12l3 3v8l-3 3h-7l-5 4v-4H6l-3-3V7Z') + dot(8.5, 11, 1.3) + dot(12, 11, 1.3) + dot(15.5, 11, 1.3),                       # 각진 말풍선 + 점 3
 'B': ln('M4.5 14v-2a7.5 7.5 0 0 1 15 0v2') + ln('M4.5 13h2.5v6H6a1.5 1.5 0 0 1-1.5-1.5Z M19.5 13H17v6h1a1.5 1.5 0 0 0 1.5-1.5Z') + ln('M18.5 19v.5a2.5 2.5 0 0 1-2.5 2.5h-3'),  # 관제 헤드셋
 'C': ln('M8 8h8a1.5 1.5 0 0 1 1.5 1.5v11A1.5 1.5 0 0 1 16 22H8a1.5 1.5 0 0 1-1.5-1.5v-11A1.5 1.5 0 0 1 8 8Z M9.5 8V2.5') + ln('M9.5 12.5h5M9.5 15.5h5', 1.8) + dot(12, 19, 1.2),  # 무전기
 'D': ln('M4 9.5a9 9 0 0 0 10.5 10.5Z') + ln('M9.3 14.7 14 10') + dot(14.8, 9.2, 1.5) + ln('M16.5 5.5a3 3 0 0 1 2 2M17.5 2.5a6 6 0 0 1 4 4', 1.8) + ln('M7 19.5l-2 2.5h5'),  # 위성 접시 + 신호
 'E': ln('M8 8V5.5L10.5 3h8.5l2.5 2.5V10L19 12.5h-.5v3L16 13', 1.8, ' opacity=".6"')  # 뒤 말풍선 (앞에 가려진 데는 안 그림)
      + ln('M5 8h8.5l2.5 2.5V15l-2.5 2.5H9l-3.5 3v-3H5L2.5 15v-4.5Z'),  # 주고받는 말풍선 2개 (각진 판 모양 · 점 없음) — 기본
 'F': ln('M5 4.5h14a2.5 2.5 0 0 1 2.5 2.5v8a2.5 2.5 0 0 1-2.5 2.5h-8.5L6 21v-3.5H5A2.5 2.5 0 0 1 2.5 15V7A2.5 2.5 0 0 1 5 4.5Z') + '<path d="M12 6.8l1.1 2.9 2.9 1.1-2.9 1.1L12 14.8l-1.1-2.9-2.9-1.1 2.9-1.1Z" fill="currentColor"/>',  # 말풍선 + 별빛
}
IC['채팅'] = CHAT['E']
def ic(body, col, x, y, s): return f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24" color="{col}">{body}</svg>'
def icon(body, col): return svg(48, 48, body.replace('currentColor', col), '0 0 24 24')

A = {}
for k, b in IC.items(): A[f'아이콘_{k}'] = icon(b, INK)
A['아이콘_와이파이_끊김'] = icon(IC['와이파이_끊김'], ERR)
for k, b in CHAT.items(): A[f'아이콘_채팅_시안{k}'] = icon(b, INK)

def ring_frame(dotc, p):  # 타이머 링 틀: 60칸 눈금 · 바탕 · 안쪽 링 · 네 방위 점. 진행 호는 따로
    cx = 130; b = f'<circle cx="{cx}" cy="{cx}" r="100" fill="url(#core)"/>'
    for i in range(60):
        a = math.radians(i * 6 - 90); L = 9 if i % 5 == 0 else 4
        b += f'<line x1="{cx+120*math.cos(a):.1f}" y1="{cx+120*math.sin(a):.1f}" x2="{cx+(120+L)*math.cos(a):.1f}" y2="{cx+(120+L)*math.sin(a):.1f}" stroke="{INK}" stroke-opacity="{.55 if i%5==0 else .22}" stroke-width="{2 if i%5==0 else 1.2}" stroke-linecap="round"/>'
    b += f'<circle cx="{cx}" cy="{cx}" r="110" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="6"/><circle cx="{cx}" cy="{cx}" r="99" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="1"/>'
    for a in (0, 90, 180, 270): r = math.radians(a - 90); b += f'<circle cx="{cx+99*math.cos(r):.1f}" cy="{cx+99*math.sin(r):.1f}" r="2.2" fill="{dotc}"/>'
    return svg(260, 260, b, p=p)
def bt(w, h, fill, stroke, p): return svg(w, h, f'<path d="{cham(1, 1, w-2, h-2, 8)}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>', p=p)
def key(w, fill, p): return svg(w, 42, f'<path d="{cham(1.25, 1.25, w-2.5, 39.5, 5)}" fill="{fill}" stroke="rgba(255,255,255,.14)" stroke-width="1.5"/>', p=p)

for p, (c, l, d, card, press) in PART.items():
    A[f'타이머_링_틀_{p}'] = ring_frame(c, p)
    A[f'타이머_진행호_{p}'] = svg(260, 260, f'<circle cx="130" cy="130" r="110" fill="none" stroke="{c}" stroke-width="6"/>')
    A[f'채팅_칸_틀_{p}'] = svg(76, 76, panel(76, 76, 12, c), p=p)
    for k, b in CHAT.items(): A[f'아이콘_채팅_시안{k}_{p}'] = icon(b, c)
    A[f'아이콘_핀_{p}'] = icon(IC['핀'], c)
    if p == '이전': continue  # 안전 모드 전엔 위 것만 씀
    A[f'목표_칸_틀_{p}'] = svg(246, 76, panel(246, 76, 12, c) + '<rect x="12" y="16" width="3" height="44" rx="1.5" fill="url(#acc)"/>', p=p)
    A[f'판_틀_{p}'] = svg(246, 76, panel(246, 76, 12, c), p=p)  # 늘려 쓰는 빈 판 (팝업 · 지도 · 비아 칸)
    A[f'완료_체크_큰_{p}'] = svg(76, 76, '<circle cx="38" cy="38" r="36" fill="url(#acc)"/>' + ic(IC['체크'], '#1a1220', 18, 18, 40), p=p)
    A[f'완료_체크_작은_{p}'] = svg(32, 32, '<circle cx="16" cy="16" r="16" fill="url(#acc)"/>' + ic(IC['체크'], '#1a1220', 6, 6, 20), p=p)
    A[f'버튼_눌림_{p}'] = bt(84, 54, press, c, p)
    A[f'힌트_카드_틀_{p}'] = svg(308, 70, f'<path d="{cham(1, 1, 306, 68, 10)}" fill="{card}" stroke="{c}" stroke-width="1.5"/><rect x="12" y="16" width="3" height="38" rx="1.5" fill="url(#acc)"/>', p=p)
    A[f'키_눌림_{p}'] = key(30, 'url(#acc)', p)
# 2부만 쓰는 것: 비아 동그라미 틀 · V 마크 · 파형 막대 · 지직 줄무늬
c2, l2, d2 = PART['2부'][:3]
A['비아_동그라미_틀'] = svg(40, 40, f'<circle cx="20" cy="20" r="18.5" fill="#1a1220" stroke="{c2}" stroke-width="1.5"/>', p='2부')
A['비아_V_마크'] = svg(40, 40, f'<circle cx="20" cy="20" r="18.5" fill="#1a1220" stroke="{c2}" stroke-width="1.5"/><path d="M12.5 13 20 28 27.5 13" fill="none" stroke="url(#acc)" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>', p='2부')
A['파형_막대'] = svg(5, 44, f'<rect width="5" height="44" rx="2.5" fill="url(#acc)"/>', p='2부')
A['지직_줄무늬'] = svg(32, 90, f'<rect y="28" width="32" height="6" fill="{c2}" fill-opacity=".55"/>', p='2부')
# 부와 무관한 것
A['안읽음_배지'] = svg(22, 22, f'<circle cx="11" cy="11" r="10" fill="{ERR}" stroke="#1a1220" stroke-width="2"/>')
A['입력_판'] = svg(332, 78, panel(332, 78, 14, brackets=False))
def field(err=False):
    return svg(212, 54, f'<path d="{cham(1, 1, 210, 52, 8)}" fill="#120e16" stroke="{ERR if err else "rgba(255,255,255,.22)"}" stroke-width="1.5"/>')
A['입력_칸'] = field(); A['입력_칸_오류'] = field(True)
A['버튼'] = bt(84, 54, 'url(#btn)', 'rgba(255,255,255,.22)', '1부')
A['버튼_정답'] = bt(308, 52, 'url(#accw)', 'rgba(255,255,255,.5)', '1부')
A['정답_칸_틀'] = svg(308, 70, f'<path d="{cham(1, 1, 306, 68, 10)}" fill="url(#accw)" stroke="rgba(255,255,255,.5)" stroke-width="1.5"/>')
A['덮개_어둡게'] = svg(8, 8, '<rect width="8" height="8" fill="rgba(0,0,0,.55)"/>')
A['키_기본'] = key(30, '#2b2433', '1부'); A['키_숫자줄'] = key(30, '#1f1a25', '1부'); A['키_넓은'] = key(52, '#1f1a25', '1부'); A['키_띄어쓰기'] = key(170, '#2b2433', '1부')
A['키보드_판'] = svg(360, 220, '<path d="M0 20Q0 0 20 0H340Q360 0 360 20V220H0Z" fill="url(#panel)" stroke="rgba(255,255,255,.12)" stroke-width="1.5"/>')

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    keep = {'_조립_미리보기.png'}
    for f in OUT.glob('*'):
        if f.is_file() and f.name not in keep: f.unlink()
    for n, s in A.items(): (OUT / f'{n}.svg').write_text(s, encoding='utf-8')
    if '--svg-only' not in sys.argv:  # PNG@3x: 엣지 헤드리스로 투명 배경 캡처
        E = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'; tmp = SP / 'aout'; tmp.mkdir(exist_ok=True)
        for n, s in A.items():
            w, h = map(int, re.match(r'<svg[^>]*width="(\d+)" height="(\d+)"', s).groups())
            (tmp / f'{n}.html').write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}svg{{display:block}}</style></head><body>{s}</body></html>', encoding='utf-8')
            try: subprocess.run([E, '--headless=new', '--disable-gpu', '--no-first-run', f'--user-data-dir={tmp / ("prof_" + str(abs(hash(n))))}', '--hide-scrollbars', '--force-device-scale-factor=3', '--default-background-color=00000000',
                                 f'--window-size={w},{h}', '--virtual-time-budget=500', f'--screenshot={OUT / (n + "@3x.png")}', (tmp / f'{n}.html').as_uri()], capture_output=True, timeout=60)
            except subprocess.TimeoutExpired: print('timeout', n)
    print('assets', len(A), '→', OUT)
