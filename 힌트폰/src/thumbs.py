import re
# 에셋 목록 카드에 넣을 미리보기 그림 (viewBox 160x90, 논리도 페이지의 svg 클래스를 그대로 씀)
RED = '#E5484D'
import sys as _sys, pathlib as _p0; _sys.path.insert(0, str(_p0.Path(__file__).parent)); from icon import nest
from shipmap import svg_map
def hms(t):  # 105분 방탈출: 예시 'MM:SS'를 시:분:초로 (45분 이상은 0시간대 예시)
    m = re.fullmatch(r'(\d\d):(\d\d)', t)
    return t if not m or t == '00:00' else ('1:' if int(m[1]) < 45 else '0:') + t
def T(x, y, t, fs=12, w=None, anchor='middle', cls=''):
    a = f' font-weight="{w}"' if w else ''; c = f' class="{cls}"' if cls else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}"{a}{c}>{hms(t)}</text>'
def R(x, y, w, h, cls='n', rx=8, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"{extra}/>'
def ph(x, y, w): return R(x, y, w, 6, 'ph', 3)
def ck(x, y, k=1, wdt=2):
    return f'<path d="M{x-4.5*k} {y} L{x-1.5*k} {y+3*k} L{x+4.5*k} {y-3.5*k}" class="ck" stroke-width="{wdt}"/>'
def chaticon(x, y, k=1):
    return (f'<g transform="translate({x} {y + 1}) scale({k})">' + '<path d="M-7 -8 H7 A3 3 0 0 1 10 -5 V2 A3 3 0 0 1 7 5 H-2 L-7 9 V5 A3 3 0 0 1 -10 2 V-5 A3 3 0 0 1 -7 -8 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="-4.5" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="0" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="4.5" cy="-1.5" r="1.4" fill="currentColor"/></g>')
def badge(x, y, n='1'):
    w = 16 if len(n) == 1 else 22
    return f'<rect x="{x-w/2}" y="{y-8}" width="{w}" height="16" rx="8" fill="{RED}"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">{n}</text>'
def pin(x, y, k=1):
    return (f'<g transform="translate({x} {y}) scale({k})"><path d="M0 8 C-7 0 -6 -7 0 -7 C6 -7 7 0 0 8 Z" class="bar"/>'
            '<circle cx="0" cy="-1.5" r="2.4" fill="var(--card)"/></g>')
def phone(x, y, cls, extra=''):
    return R(x, y, 40, 76, cls, 9, extra)
def sig(x, y, k=1):
    return (f'<g transform="translate({x} {y}) scale({k})"><circle cx="0" cy="0" r="4" class="vfill"/>'
            + ''.join(f'<path d="M{-r} {-r*0.6} A{r} {r} 0 0 1 {r} {-r*0.6}" fill="none" class="ln" stroke-width="2" opacity="{1-i*0.25}"/>' for i, r in enumerate((11, 19, 27)))
            + '</g>')
def shield(x, y, k=1, cls='lily'):
    return (f'<path transform="translate({x} {y}) scale({k})" d="M0 -22 L18 -15 V0 C18 12 9 19 0 23 C-9 19 -18 12 -18 0 V-15 Z" class="{cls}" stroke-width="2"/>'
            '')
def note(x, y):
    return f'<path d="M{x} {y} V{y-26} L{x+20} {y-32} V{y-6}" fill="none" class="ln" stroke-width="2.4"/><circle cx="{x-5}" cy="{y+1}" r="6" class="vfill"/><circle cx="{x+15}" cy="{y-5}" r="6" class="vfill"/>'
def wifi_off(x, y):
    return (f'<g transform="translate({x} {y})"><path d="M-22 -4 A31 31 0 0 1 22 -4" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/>'
            '<path d="M-13 5 A18 18 0 0 1 13 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/>'
            '<circle cx="0" cy="14" r="3.5" fill="currentColor"/><path d="M-20 -18 L20 22" stroke="var(--via)" stroke-width="3" stroke-linecap="round"/></g>')
def wave(cx, cy, k=0.6):
    hs = [10, 22, 36, 18, 44, 28, 50, 24, 38, 16, 30, 12]; w = 6 * k; g = 4 * k
    tot = len(hs) * (w + g) - g; x0 = cx - tot / 2
    return ''.join(f'<rect x="{x0+i*(w+g):.1f}" y="{cy-h*k/2:.1f}" width="{w:.1f}" height="{h*k:.1f}" rx="{w/2:.1f}" class="vfill"/>' for i, h in enumerate(hs))
def hexdots(cx, cy, r, path=(), red=False):
    import math
    pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
    out = ''
    if path:
        d = 'M' + ' L'.join(f'{pts[i][0]:.1f} {pts[i][1]:.1f}' for i in path)
        out += f'<path d="{d}" class="vline" stroke-width="3"' + (f' style="stroke:{RED}"' if red else '') + '/>'
    for i, (x, y) in enumerate(pts):
        on = i in path
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if on else 4}" ' + ((f'fill="{RED}"' if red else 'class="vfill"') if on else 'class="soft"') + '/>'
    return out
EMPTY = R(52, 17, 56, 56, 'n dashbox', 14)  # 아직 그리지 않은 에셋 자리

TH = {
    # 배경
    '안전 모드 이전 배경': phone(60, 7, 'soft'),
    '1부 배경': phone(60, 7, 'lily'),
    '2부 배경': phone(60, 7, 'via'),
    '엔딩 배경': phone(32, 7, 'n', ' style="fill:#000;stroke:#000"') + phone(88, 7, 'n') + sig(108, 48, 0.55),
    # 채팅
    '참가자 말풍선': R(46, 14, 100, 30, 'lily', 12) + ph(58, 26, 76) + R(82, 52, 64, 24, 'lily', 12) + ph(94, 61, 40),
    '운영자 말풍선': R(14, 14, 110, 42, 'n', 12) + ph(26, 26, 86) + ph(26, 40, 50) + R(14, 62, 70, 22, 'n', 11) + ph(26, 70, 46),
    '채팅 위 줄': '<path d="M26 38 L19 45 L26 52" class="ln" stroke-width="2"/>' + chaticon(80, 41, 1) + T(140, 50, '38:15', 12, 700, 'end') + '<path d="M14 66 H146" class="ln" opacity=".25"/>',
    '입력 칸': R(14, 26, 132, 38, 'n', 19) + '<path d="M30 36 V54" stroke="currentColor" stroke-width="2"/>',
    '보내기 버튼': '<circle cx="56" cy="45" r="20" class="n"/><path d="M49 45 H63 M57 38 L64 45 L57 52" class="ln" stroke-width="2.2"/>'
                 + '<circle cx="106" cy="45" r="20" class="lily"/><path d="M99 45 H113 M107 38 L114 45 L107 52" class="ln" stroke-width="2.2"/>',
    '안 읽음 숫자': '<circle cx="54" cy="47" r="16" class="n"/>' + chaticon(54, 43, 0.85) + badge(67, 33)
                  + '<circle cx="108" cy="47" r="16" class="n"/>' + chaticon(108, 43, 0.85) + badge(123, 33, '12'),
    # 칸 · 카드
    '타이머 칸': '<circle cx="52" cy="45" r="31" fill="none" stroke="currentColor" stroke-opacity=".15" stroke-width="4"/><circle cx="52" cy="45" r="31" fill="none" stroke="#cf86e6" stroke-width="4" stroke-linecap="round" pathLength="100" stroke-dasharray="45 100" transform="rotate(-90 52 45)"/>' + T(52, 50, '0:47:12', 12, 700, 'middle') + R(110, 30, 42, 22, 'soft', 6) + T(131, 45, '47:12', 10, 700),
    '목표 창': R(10, 10, 66, 70, 'n dashbox', 10) + R(84, 10, 66, 70, 'lily', 10) + T(117, 38, '현재 목표', 8, cls='t-lily') + T(117, 54, '알렉스의 승인', 9, 700),
    '비아 말 칸': '<circle cx="28" cy="27" r="11" class="via"/>' + T(28, 31, '?', 11, 700, cls='t-via') + wave(92, 27, 0.4)
               + '<circle cx="28" cy="64" r="11" class="via"/>' + T(28, 68, 'V', 11, 700, cls='t-via') + wave(92, 64, 0.4),
    '코드 입력 칸': R(8, 8, 144, 22, 'n', 6) + R(8, 34, 144, 22, 'n', 6) + T(18, 50, 'ABCD', 12, 700, 'start')
                 + R(8, 60, 144, 22, 'n', 6, f' style="fill:none;stroke:{RED};stroke-width:2"') + T(18, 76, 'QRST', 12, 700, 'start'),
    '힌트 카드': R(8, 10, 144, 34, 'lily') + T(18, 24, '힌트 1', 9, 700, 'start', 't-lily') + ph(18, 32, 100)
              + R(8, 50, 144, 34, 'via') + T(18, 64, '힌트 1', 9, 700, 'start', 't-via') + ph(18, 72, 90),
    '정답 칸': R(10, 20, 140, 50, 'inv', 10) + T(22, 38, '정답', 9, 700, 'start', 't-inv') + T(22, 60, '끝없는탐구', 15, 700, 'start', 't-inv'),
    '스토리카드 틀': R(10, 12, 42, 66, 'lily', 6) + R(59, 12, 42, 66, 'eva', 6) + R(108, 12, 42, 66, 'n', 6)
                 + ''.join(ph(x + 7, 26 + k * 10, 28) for x in (10, 59, 108) for k in range(3)),
    '패턴 점 · 선': hexdots(44, 45, 28, (0, 6, 5)) + hexdots(116, 45, 28, (0, 1, 2), True),
    # 버튼
    '다음': R(6, 26, 72, 36, 'n') + T(42, 49, '다음', 11, 700, cls='t-lily') + R(82, 26, 72, 36, 'n') + T(118, 49, '다음', 11, 700, cls='t-via'),
    '정답': R(20, 26, 120, 38, 'inv', 10) + T(80, 50, '정답', 13, 700, cls='t-inv'),
    '한글 키보드': ''.join(R(14 + k * 13.4, 14 + j * 13, 11, 10, 'n' if j else 'soft', 2.5) for j in range(4) for k in range(10 if j < 2 else 9 if j == 2 else 9)) + R(40, 66, 80, 10, 'n', 2.5),
    '코드 키보드': ''.join(R(14 + k * 13.4, 18 + j * 15, 11, 12, 'n' if j else 'soft', 2.5) for j in range(4) for k in range(10 if j < 2 else 9 if j == 2 else 8)),
    '상태 표시줄': T(40, 50, '9:41', 12, 700) + '<path d="M104 44 a8 8 0 0 1 12 0 M107 47.5 a4 4 0 0 1 6 0" fill="none" class="ln" stroke-width="1.8"/><circle cx="110" cy="50" r="1.6" fill="currentColor"/>' + R(122, 41, 20, 10, 'n', 3) + R(124, 43, 13, 6, 'soft', 1.5),
    '채팅 판': phone(60, 7, 'n') + R(61, 22, 38, 46, 'soft', 0) + '<path d="M61 22 H99 M61 68 H99" class="ln" opacity=".5"/>' + R(76, 28, 18, 7, 'lily', 3) + R(66, 40, 20, 7, 'n', 3) + R(64, 72, 24, 6, 'n', 3),
    # 아이콘
    '방패': shield(80, 45, 1.3),
    '채팅 칸': R(52, 12, 56, 66, 'soft', 12) + chaticon(80, 45, 1.5),
    '장소 줄': pin(26, 45) + T(38, 50, '알렉스의 방', 13, 700, 'start', 't-lily') + '<path d="M124 40 L130 45 L124 50" class="ln" stroke-width="2" stroke-linecap="round"/>',
    '힌트 사용 횟수': T(80, 50, '힌트 사용 2회', 13, 500),
    '힌트 팝업 틀': R(14, 8, 132, 74, 'soft', 12) + T(26, 28, '문제 3', 11, 700, 'start') + '<path d="M128 18 L136 26 M136 18 L128 26" class="ln" stroke-width="2" stroke-linecap="round"/>' + R(24, 38, 112, 18, 'lily', 6) + R(24, 62, 112, 14, 'n', 6),
    '힌트 보기': R(44, 26, 72, 38, 'n') + T(80, 50, '힌트 보기', 11, 700),
    '체크': '<circle cx="80" cy="45" r="22" class="bar"/>' + ck(80, 45, 2.2, 3.5),
    '채팅 아이콘': chaticon(80, 38, 2.2),
    '뒤로': '<path d="M88 27 L70 45 L88 63" class="ln" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    '보내기': '<path d="M62 45 H98 M84 31 L98 45 L84 59" class="ln" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    '와이파이 끊김': wifi_off(80, 42),
    '연결 끊김 문구': T(80, 52, '연결이 끊겼습니다', 12, 700),
    '송출': sig(80, 58, 1),
    '음표': note(76, 66),
    '장소 핀': pin(80, 45, 2.6),
    '꺾쇠': '<path d="M74 31 L88 45 L74 59" class="ln" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    '닫기': '<path d="M66 31 L94 59 M94 31 L66 59" class="ln" stroke-width="3" stroke-linecap="round"/>',
    '우주선 지도': svg_map(14.5, 4.5, 0.46, '알렉스', fs=9),
    '앱 아이콘': nest('th-appicon', 47, 12, 66),
}

# 움직임 미리보기: 처음 → 끝 두 컷
def two(a, b):
    return f'<g>{a}</g><path d="M74 45 H86" class="ln" marker-end="url(#ahT)"/><g transform="translate(88 0)">{b}</g>'
MOTION_TH = {
    '안전 모드 감지': two(shield(36, 38, 0.6) + R(14, 64, 44, 4, 'soft', 2) + R(14, 64, 12, 4, 'bar', 2), shield(36, 38, 0.6) + R(14, 64, 44, 4, 'soft', 2) + R(14, 64, 40, 4, 'bar', 2)),
    '지도 팝업 열림': two(R(12, 22, 48, 46, 'lily', 8) + pin(30, 45, 1.2) + ph(38, 43, 16), phone(16, 7, 'soft') + svg_map(18, 30, 0.127, '알렉스', label=False)),
    '목표 완료': two('<circle cx="36" cy="45" r="16" class="bar"/>' + ck(36, 45, 1.6, 3), R(12, 22, 48, 46, 'lily', 8) + ph(20, 40, 32) + ph(20, 52, 22)),
    '비아 끼어들기': two(phone(16, 7, 'lily') + R(20, 30, 28, 4, 'vfill', 2) + R(26, 50, 22, 4, 'vfill', 2), phone(16, 7, 'via')),
    '음성 파형': wave(80, 45, 0.9),
    '키보드 올라옴': two(R(14, 60, 52, 22, 'soft', 4), R(14, 38, 52, 44, 'soft', 4)),
    '이름 바뀜': two('<circle cx="36" cy="45" r="16" class="via"/>' + T(36, 51, '?', 16, 700, cls='t-via'), '<circle cx="36" cy="45" r="16" class="via"/>' + T(36, 51, 'V', 15, 700, cls='t-via')),
    'V 옮겨 감': two(R(4, 27, 66, 36, 'n', 6) + '<circle cx="37" cy="45" r="11" class="via"/>' + T(37, 49, 'V', 11, 700, cls='t-via'), R(0, 27, 66, 36, 'n', 6) + '<circle cx="15" cy="45" r="11" class="via"/>' + T(15, 49, 'V', 11, 700, cls='t-via') + ''.join(f'<rect x="{31 + i * 5.5}" y="{45 - h}" width="3" height="{2 * h}" rx="1.5" class="bar"/>' for i, h in enumerate((4, 8, 12, 7, 10, 5)))),
    '다음 힌트 펼침': two(R(6, 34, 64, 22, 'n') + ph(16, 42, 44), R(6, 14, 64, 26, 'lily') + ph(14, 24, 46) + R(6, 48, 64, 22, 'n') + ph(16, 56, 44)),
    '패턴 선 그리기': hexdots(80, 45, 30, (0, 6, 5)),
    '패턴 오답': two(hexdots(36, 45, 24, (0, 1, 2), True), hexdots(36, 45, 24)),
    '안 읽음 숫자 등장': two('<circle cx="36" cy="47" r="15" class="n"/>' + chaticon(36, 43, 0.8), '<circle cx="36" cy="47" r="15" class="n"/>' + chaticon(36, 43, 0.8) + badge(49, 34)),
    '탈출 엔딩 끊김': two(phone(16, 7, 'n') + R(22, 34, 26, 4, 'soft', 2) + R(26, 46, 20, 4, 'soft', 2), phone(16, 7, 'n', ' style="fill:#000;stroke:#000"')),
}

def svg(body):
    return ('<svg class="thumb" viewBox="0 0 160 90" aria-hidden="true">'
            + body + '</svg>')

# 실제 배경 이미지가 있으면 배경 카드 미리보기를 그 이미지로 바꾼다 (bg.py가 만든 thumb_*.jpg)
import base64, pathlib as _pl
_here = _pl.Path(__file__).parent
def _img(name, x, y=5, w=36, h=80):
    f = _here / f'thumb_{name}.jpg'
    if not f.exists(): return None
    b64 = base64.b64encode(f.read_bytes()).decode()
    return (f'<clipPath id="c_{name}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7"/></clipPath>'
            f'<image href="data:image/jpeg;base64,{b64}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#c_{name})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="none" class="ln" opacity=".35"/>')
for key, name in [('안전 모드 이전 배경', 'bg_pre'), ('1부 배경', 'bg_part1'), ('2부 배경', 'bg_part2')]:
    v = _img(name, 62)
    if v: TH[key] = v
_a, _b = _img('bg_end_escape', 38), _img('bg_end_planet', 86)
if _a and _b: TH['엔딩 배경'] = _a + _b
def preview_b64():
    f = _here / 'bg_preview.jpg'
    return base64.b64encode(f.read_bytes()).decode() if f.exists() else None

# 방패 (로고 폴더의 SVG를 카드 미리보기에 그대로)
import re as _re
for _k, _label in (('plain', '방패'),):
    _f = _pl.Path('로고') / f'shield_{_k}.svg'
    if _f.exists():
        _s = _f.read_text(encoding='utf-8').replace('shield_', 'th_shield_')
        _s = _re.sub(r'<svg [^>]*>', '<svg x="45" y="3" width="70" height="84" viewBox="0 0 512 512">', _s, count=1)
        TH[_label] = _s
