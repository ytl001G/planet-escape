import re
import pathlib, sys, math
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')

def rep(o, n, c=1):
    global s
    assert s.count(o) == c, (o, s.count(o)); s = s.replace(o, n)

# 에바 색 토큰과 보조 클래스
rep('  --via-soft: #fdebd6;\n', '  --via-soft: #fdebd6;\n  --eva: #1e88e5;\n  --eva-soft: #e3effc;\n  --ans: #616161;\n  --ans-ink: #ffffff;\n')
rep('--sys-soft: #2b2830;', '--sys-soft: #2b2830; --eva: #64b5f6; --eva-soft: #1c2a3a; --ans: #a7a3ad; --ans-ink: #17151b;', 2)
rep('svg .bar {', 'svg .nm-al { fill: #E57373; }\nsvg .nm-op { fill: #FFF176; }\nsvg .nm-no { fill: #81C784; }\nsvg .nm-ev { fill: #64B5F6; }\nsvg .nm-li { fill: #BA68C8; }\nsvg .bar {')
rep('svg .bar {', 'svg .eva { fill: var(--eva-soft); stroke: var(--eva); stroke-width: 1.5; }\n'
    'svg .efill { fill: var(--eva); }\n'
    'svg .vline { fill: none; stroke: var(--via); stroke-width: 4; stroke-linecap: round; stroke-linejoin: round; }\n'
    'svg .ph { fill: var(--line); }\nsvg .inv { fill: var(--ans); stroke: var(--ans); stroke-width: 1.5; }\nsvg .t-inv { fill: var(--ans-ink); }\nsvg .bar {')

def hms(t):  # 105분 방탈출: 예시 'MM:SS'를 시:분:초로 (45분 이상은 0시간대 예시)
    m = re.fullmatch(r'(\d\d):(\d\d)', t)
    return t if not m or t == '00:00' else ('1:' if int(m[1]) < 45 else '0:') + t
def T(x, y, t, fs=12, w=None, anchor='start', cls=''):
    a = f' font-weight="{w}"' if w else ''; c = f' class="{cls}"' if cls else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}"{a}{c}>{hms(t)}</text>'
def R(x, y, w, h, cls='n', rx=8, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"{extra}/>'
def lines(x, y0, ts, fs=12, step=17, cls=''):
    return ''.join(T(x, y0 + i * step, t, fs, cls=cls) for i, t in enumerate(ts))
def wave(cx, cy, k):
    hs = [10, 22, 36, 18, 44, 28, 50, 24, 38, 16, 30, 12]; w = 6 * k; g = 4 * k
    tot = len(hs) * (w + g) - g; x0 = cx - tot / 2
    return ''.join(f'<rect x="{x0+i*(w+g):.1f}" y="{cy-h*k/2:.1f}" width="{w:.1f}" height="{h*k:.1f}" rx="{w/2:.1f}" class="vfill"/>' for i, h in enumerate(hs))
def ck(x, y, k=1, wdt=2):
    return f'<path d="M{x-4.5*k} {y} L{x-1.5*k} {y+3*k} L{x+4.5*k} {y-3.5*k}" class="ck" stroke-width="{wdt}"/>'

# 메인 화면형 (250x440)
def M(o, time, guide_cls='lily', badge=False):
    return (R(20+o, 10, 250, 440, 'n', 30) + sbar(o + 10) + R(40+o, 52, 210, 58, 'soft', 10) + T(145+o, 99, time, 24, 700, 'middle')
            + R(40+o, 124, 210, 220, guide_cls, 12) + dock(o, guide_cls, badge) + R(115+o, 440, 60, 3, 'soft', 1.5))
def sbar(o):  # 상태 표시줄: 시각 · 와이파이 · 배터리
    return (T(34+o, 29, '9:41', 9, 700) + f'<path d="M{o+228} 24 a6 6 0 0 1 9 0 M{o+230} 26.5 a3.2 3.2 0 0 1 5 0" fill="none" class="ln" stroke-width="1.4"/><circle cx="{o+232.5}" cy="28.5" r="1.2" fill="currentColor"/>'
            + R(o+242, 22.5, 14, 7.5, 'n', 2) + R(o+243.5, 24, 9, 4.5, 'soft', 1))
def dock(o, cls, badge=False):  # 아래 독: 힌트코드 · 스토리코드 · 운영자 호출 앱 아이콘
    k = 'via' if cls == 'via' else 'n' if cls.startswith('n') else 'lily'
    out = R(36+o, 352, 218, 80, 'soft', 20)
    for i, (x, l) in enumerate(((80, '힌트코드'), (145, '스토리코드'), (210, '운영자 호출'))):
        out += R(x-19+o, 361, 38, 38, k, 10) + T(x+o, 420, l, 9, 500, 'middle')
        if i == 0: out += f'<circle cx="{x+o}" cy="377" r="6" fill="none" class="ln" stroke-width="1.6"/><path d="M{x-3+o} 387 H{x+3+o}" class="ln" stroke-width="1.6"/>'
        if i == 1: out += f'<path d="M{x-8+o} 372 Q{x+o} 368 {x+o} 373 Q{x+o} 368 {x+8+o} 372 V388 Q{x+o} 384 {x+o} 389 Q{x+o} 384 {x-8+o} 388 Z" fill="none" class="ln" stroke-width="1.5"/>'
        if i == 2:
            out += f'<path d="M{x-8+o} 372 H{x+8+o} Q{x+10+o} 372 {x+10+o} 374 V382 Q{x+10+o} 384 {x+8+o} 384 H{x-2+o} L{x-6+o} 388 V384 H{x-8+o} Q{x-10+o} 384 {x-10+o} 382 V374 Q{x-10+o} 372 {x-8+o} 372 Z" fill="none" class="ln" stroke-width="1.5"/>'
            if badge: out += f'<circle cx="{x+17+o}" cy="362" r="7" fill="#E5484D"/><text x="{x+17+o}" y="365.5" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">1</text>'
    return out
ROOMS = [('알렉스', 56, 272), ('오펠리아', 117, 272), ('노아', 178, 272), ('에바', 86, 308), ('릴리', 148, 308)]
def mapx(o, hi, done=()):
    return ''  # 목표 창에는 현재 목표만 (인물 방 목록 뺌)
    out = ''
    for i, (n, x, y) in enumerate(ROOMS):
        out += R(x+o, y, 56, 30, 'lily' if i == hi else 'n', 4, ' stroke-width="2.5"' if i == hi else '')
        out += T(x+28+o, y+19, n, 10, 700 if i == hi else None, 'middle', '' if i == hi else 't-mute')
        if i in done:
            out += f'<circle cx="{x+50+o}" cy="{y+5}" r="6" class="bar"/>' + ck(x+50+o, y+5, 0.7, 1.6)
    return out

# 코드 화면형 (270x500). 버튼은 입력 칸 아래 [힌트 보기] [진행도]
def C(o, time, title=''):
    return (R(10+o, 10, 270, 500, 'n', 30) + sbar(o) + (T(145+o, 48, title, 14, 700, 'middle') if title else '')
            + R(188+o, 33, 82, 24, 'soft', 12) + f'<circle cx="{201+o}" cy="45" r="5.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".75"/><path d="M{201+o} 42 V45 L{203+o} 46.5" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".75"/>' + T(262+o, 49, time, 12, 700, 'end')
            + f'<path d="M{10+o} 66 H{280+o}" class="ln" opacity=".45"/>')  # 위 줄 아래 구분선
def entry(o, typed=False, pct=None, code='ABCD', open_=False, acc='lily'):
    bar = 'bar' if acc == 'lily' else 'vfill'
    out = R(30+o, 90, 230, 44, 'n')
    if typed:
        out += f'<text x="{46+o}" y="118" font-size="16" font-weight="700" font-family="IBM Plex Mono, monospace" letter-spacing="2">{code}</text>'  # 코드는 가리지 않고 글자 그대로
    # 버튼은 평소 회색, 눌러서 내용이 펼쳐진 쪽만 보라
    out += R(30+o, 146, 111, 44, acc if open_ else 'n') + T(85.5+o, 173, '힌트 보기', 13, 700, 'middle')
    if pct is None:
        out += R(149+o, 146, 111, 44, 'n') + T(204.5+o, 173, '진행도', 13, 700, 'middle')
    else:
        out += (R(149+o, 146, 111, 44, acc) + T(204.5+o, 166, pct, 14, 700, 'middle')
                + R(161+o, 175, 87, 5, 'soft', 2.5) + R(161+o, 175, 87 * int(pct[:-1]) / 100, 5, bar, 2.5))
    return out
D = 136  # 힌트는 코드 입력 화면의 버튼 줄 아래로 펼쳐진다
def hint(o, y, h, label, ts, cls='lily', lcls='t-lily'):
    y += D
    return R(30+o, y, 230, h, cls) + T(44+o, y+18, label, 11, 700, cls=lcls) + lines(44+o, y+36, ts, step=16)
def H(o, time, code='ABCD', pct=None, acc='lily'):
    # 힌트 화면 = 코드 입력 화면 그대로(제목·입력한 코드·버튼 줄) + 아래로 힌트가 펼쳐짐
    return C(o, time, '힌트코드') + entry(o, typed=True, pct=pct, code=code, open_=True, acc=acc)
def svg(w, h, aria, body, maxw):
    return (f'    <svg style="max-width:{maxw}px;margin:0 auto" viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">\n'
            '      <defs><marker id="ah5" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="currentColor"/></marker></defs>\n      '
            + body + '\n    </svg>\n')
arrow = lambda x, y=230: f'<path d="M{x} {y} H{x+24}" class="ln" marker-end="url(#ah5)"/>'
def section(title, sv):
    return f'<section>\n  <h2>{title}</h2>\n  <figure>\n{sv}  </figure>\n</section>\n'
def replace_section(h2, new):
    global s
    a = s.index(f'<section>\n  <h2>{h2}</h2>'); b = s.index('</section>\n', a) + len('</section>\n')
    s = s[:a] + new + s[b:]

# 6. 코드 입력 화면: A 입력 전, B 힌트 보기 누른 뒤
hintB = (hint(290, 70, 60, '힌트 1', ['특정 동작을 통해 숨겨진', '것을 알아내자.']) + hint(290, 138, 60, '힌트 2', ['드래그했을 때 뭔가', '보이는 것 같다.'])
         + R(320, 206+D, 230, 46, 'n') + T(435, 234+D, '다음 힌트', 13, 700, 'middle', 't-lily'))
body = C(0, '47:12', '힌트코드') + entry(0) + H(290, '47:12') + hintB
replace_section('6. 코드 입력 화면', section('6. 코드 입력 화면', svg(580, 520,
    '코드 입력 화면 두 가지 상태. 왼쪽은 입력 칸 아래 힌트 보기 버튼과 진행도 버튼. 오른쪽은 힌트 보기를 누른 뒤 힌트 1과 2가 열려 있고 다음 힌트 버튼. 정답 보기는 힌트를 다 본 뒤에만 나타난다.', body, 600)))
# 7. 진행도 버튼: 코드를 넣고 누르면 버튼 자리에 %
body = C(0, '44:20', '힌트코드') + entry(0, typed=True, pct='38%')
replace_section('7. 진행도 버튼을 눌렀을 때', section('7. 진행도 버튼을 눌렀을 때', svg(290, 520,
    '코드를 입력한 뒤 진행도 버튼을 누르면 버튼 자리에 퍼센트와 진행률 막대가 표시된다.', body, 300)))

RED = '#E5484D'
def pin(x, y):
    return (f'<path d="M{x} {y+8} C{x-7} {y} {x-6} {y-7} {x} {y-7} C{x+6} {y-7} {x+7} {y} {x} {y+8} Z" class="bar"/>'
            f'<circle cx="{x}" cy="{y-1.5}" r="2.4" fill="var(--card)"/>')
NM = {'알렉스': 'al', '오펠리아': 'op', '노아': 'no', '에바': 'ev', '릴리': 'li'}
def tint(room):  # '알렉스의 방' → 이름만 그 사람 대표색
    n = next((n for n in NM if room.startswith(n)), None)
    return f'<tspan class="nm-{NM[n]}">{n}</tspan>{room[len(n):]}' if n else room
def chev(x, y):  # 방 이름을 누르면 지도가 뜬다는 표시
    return f'<path d="M{x} {y-4} L{x+3.5} {y} L{x} {y+4}" class="ln" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
def place(x, y, room, w=170, anchor='start'):
    # 장소(핀 + 방 이름) + 할 일 자리(회색 막대, 문구 미정)
    if anchor == 'middle':
        tw = len(room) * 12
        return (pin(x - tw / 2 - 8, y) + T(x + 6, y + 5, tint(room), 12, 700, 'middle', 't-lily') + chev(x + 6 + tw / 2 + 5, y)
                + R(x - w / 2, y + 22, w, 7, 'ph', 3.5) + R(x - w * 0.35, y + 36, w * 0.7, 7, 'ph', 3.5))
    return (pin(x + 6, y) + T(x + 18, y + 5, tint(room), 12, 700, cls='t-lily') + chev(x + 18 + len(room) * 12 + 5, y)
            + R(x, y + 22, w, 7, 'ph', 3.5) + R(x, y + 36, w * 0.7, 7, 'ph', 3.5))
def listicon(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="14" class="n"/>'
            + ''.join(f'<path d="M{x-6} {y-5+i*5} H{x+6}" class="ln" stroke-width="1.8"/>' for i in range(3)))

S = []
# 8. 진행도와 힌트를 같이 볼 때: 두 경로 모두 같은 화면으로 모인다
hints2 = (hint(0, 70, 60, '힌트 1', ['특정 동작을 통해 숨겨진', '것을 알아내자.']) + hint(0, 138, 60, '힌트 2', ['드래그했을 때 뭔가', '보이는 것 같다.'])
          + R(30, 206+D, 230, 46, 'n') + T(145, 234+D, '다음 힌트', 13, 700, 'middle', 't-lily'))
g = lambda x, y, b: f'<g transform="translate({x} {y})">{b}</g>'
body = (g(0, 0, C(0, '44:20', '힌트코드') + entry(0, typed=True, pct='38%'))
        + g(320, 0, H(0, '44:20') + hints2)
        + g(160, 560, H(0, '44:20', pct='38%') + hints2)
        + '<path d="M145 516 V540 H290 V556" class="ln" marker-end="url(#ah5)"/>' + T(153, 534, '힌트 보기', 12, 700)
        + '<path d="M465 516 V540 H320 V556" class="ln" marker-end="url(#ah5)"/>' + T(457, 534, '진행도', 12, 700, 'end'))
S.append(section('8. 진행도와 힌트를 같이 볼 때', svg(610, 1080,
    '진행도를 먼저 보고 힌트 보기를 누른 경우와, 힌트를 보다가 진행도를 누른 경우 모두 같은 화면이 된다. 위에 입력한 코드, 가운데 힌트, 아래 진행도 버튼 자리에 퍼센트가 남아 있다.', body, 600)))
# 8. 목표 완료 → 다음 목표
body = (M(0, '50:02') + '<circle cx="145" cy="196" r="26" class="bar"/>' + ck(145, 196, 2.6, 4)
        + T(145, 248, '알렉스의 승인 확보', 14, 700, 'middle') + mapx(0, -1, (0,))
        + arrow(276)
        + M(310, '50:00') + T(455, 228, '현재 목표', 11, None, 'middle', 't-lily') + T(455, 252, '오펠리아의 승인 확보', 14, 700, 'middle') + place(455, 286, '오펠리아의 방', 160, 'middle') + mapx(310, 1, (0,)))
S.append(section('9. 목표를 끝냈을 때', svg(580, 460,
    '목표 완료 화면: 끝낸 목표에 큰 체크 표시가 뜨고, 이어서 다음 현재 목표로 바뀐다.', body, 600)))
# 9. 정답 보기 누르기 전 · 후
hints3 = (hint(0, 70, 56, '힌트 1', ['특정 동작을 통해 숨겨진', '것을 알아내자.']) + hint(0, 132, 56, '힌트 2', ['드래그했을 때 뭔가', '보이는 것 같다.'])
          + hint(0, 194, 76, '힌트 3', ['각 행성일마다 한 글자씩', '하이라이트되며, 이를 합쳐', '답을 알 수 있다.']))
before = H(0, '46:31') + hints3 + R(30, 276+D, 230, 46, 'inv') + T(145, 304+D, '정답 보기', 13, 700, 'middle', 't-inv')
after = H(0, '46:20') + hints3 + R(30, 276+D, 230, 64, 'inv') + T(44, 294+D, '정답 보기', 11, 700, cls='t-inv') + T(44, 324+D, '끝없는탐구', 18, 700, cls='t-inv')
body = before + arrow(286, 260) + g(320, 0, after)
S.append(section('10. 정답 보기를 누르기 전 · 후', svg(600, 520,
    '문제 3 힌트 1, 2, 3이 모두 열린 화면. 왼쪽은 맨 아래 정답 보기 버튼만 있는 상태, 오른쪽은 버튼을 눌러 같은 자리에 정답 끝없는탐구가 열린 상태. 정답 칸은 시스템 회색.', body, 620)))
# 10. 2부 힌트
body = (H(0, '21:12', 'KLMN', acc='via') + hint(0, 70, 60, '힌트 1', ['별자리 필름이 다시', '필요해 보이네.'], 'via', 't-via')
        + R(30, 138+D, 230, 46, 'n') + T(145, 166+D, '다음 힌트', 13, 700, 'middle', 't-via'))
S.append(section('11. 2부 힌트', svg(290, 520,
    '2부 힌트 화면: 구성은 1부와 같고 강조색만 주황. 문제 10 힌트 1이 열려 있고 다음 힌트 버튼.', body, 300)))
# 문제 16 힌트: 레버 장면 선택 대기 6단계 (대사집 1707~1714). 넣을 때마다 다음 단계, 6단계 뒤엔 심장 소리만
def dots6(o, n):
    return ''.join(f'<circle cx="{105+o+i*16}" cy="{420}" r="5" class="{"vfill" if i < n else "soft"}"/>' for i in range(6))
def spk(o, y, who, col):
    return f'<circle cx="{48+o}" cy="{y-4}" r="4" style="fill:{col}"/>' + T(58+o, y, who, 11, 700)
HEART = 'M27 45 C10 32 2 23 2 13 C2 6 8 1 15 1 C20 1 24 4 27 8 C30 4 34 1 39 1 C46 1 52 6 52 13 C52 23 44 32 27 45 Z'
body = (H(0, '04:48', 'WXYZ', acc='via') + R(30, 70+D, 230, 240, 'via', 12)
        + spk(0, 232, '에바', '#1E88E5') + lines(44, 252, ['근데 만약 이게 실패하면?', '그때를 대비해서 계획을', '하나 더 만들어 둬야겠어.'], step=17)
        + spk(0, 318, '비아', '#FB8C00') + lines(44, 338, ['…방금 그거 뭐였지?'])
        + wave(145, 382, 0.6) + dots6(0, 2)
        + arrow(288, 330) + T(300, 318, '6단계 뒤', 10, 700, 'middle')
        + H(310, '03:10', 'WXYZ', acc='via') + R(340, 70+D, 230, 240, 'via', 12)
        + f'<path transform="translate(428 290)" d="{HEART}" class="vfill"/>' + dots6(310, 6))
S.append(section('12. 문제 16 힌트 (대기 연출 6단계)', svg(600, 520,
    '문제 16 힌트 화면: 같은 코드를 넣을 때마다 레버 장면의 선택 대기 연출이 한 단계씩 나온다. 왼쪽은 2단계로 에바의 메모 회상과 비아의 반응이 화자 이름과 함께 뜨고 음성 파형, 여섯 칸 중 두 칸이 채워진 점. 오른쪽은 6단계 뒤로, 글 없이 뛰는 심장만 남고 여섯 칸이 다 채워진다. 정답 보기는 없다.', body, 620)))
# 12. 보너스 패턴 입력 → 스토리카드 13.5 (기존 도안의 육각 7칸 배치)
cx, cy, r = 145, 250, 72
pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in (-90, -30, 30, 90, 150, 210)]
path = [pts[0], pts[6], pts[5]]  # 도장(가운데) → 레몬(왼쪽 위) → 미로(왼쪽 아래)까지 그린 상태
pl = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in path)
dotsvg = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if (x, y) in path else 7}" class="{"vfill" if (x, y) in path else "soft"}"/>' for x, y in pts)
card = ['소규모 실험에서 추진에', '이용할 수 있는 반응을 확인했다.', '하지만 반응을 오래 유지하지', '못했고, 현재 추진 장치에', '적용하는 방법도 해결하지',
        '못했다.', '실험 조건과 실패 기록을', '함께 남긴다.', '당장 돌아갈 방법은 아니지만,', '연구를 이어 갈 가치는 있다.']
body = (C(0, '17:40') + f'<path d="{pl}" class="vline"/>' + dotsvg
        + arrow(286, 250)
        + C(320, '17:22') + R(350, 70, 230, 350, 'eva', 12) + T(366, 98, '제온 추진 연료 전환 실험', 13, 700) + T(366, 117, '— 에바 펠로노르', 11, cls='t-mute')
        + lines(366, 148, card, 11, 18))
S.append(section('13. 보너스 패턴 입력 → 스토리카드 13.5', svg(610, 520,
    '보너스 패턴 입력 화면: 기존 도안과 같은 육각 배치의 점 일곱 개에 가운데에서 시작한 선이 그려지는 중. 정답이면 에바의 파란 카드로 스토리카드 13.5 원문이 뜬다.', body, 620)))
# 13. 운영자 호출 (문구 자리는 회색 막대)
def chaticon(x, y, k=1):
    return (f'<g transform="translate({x} {y + 1}) scale({k})">' + '<path d="M-7 -8 H7 A3 3 0 0 1 10 -5 V2 A3 3 0 0 1 7 5 H-2 L-7 9 V5 A3 3 0 0 1 -10 2 V-5 A3 3 0 0 1 -7 -8 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="-4.5" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="0" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="4.5" cy="-1.5" r="1.4" fill="currentColor"/></g>')
body = (M(0, '38:15', badge=True) + T(56, 236, '현재 목표', 11, cls='t-lily') + T(56, 256, '에바의 승인 확보', 14, 700) + place(56, 282, '에바의 방', 170)
        + R(30, 16, 230, 34, 'soft', 12) + R(40, 24, 18, 18, 'lily', 5) + T(66, 31, '운영자 호출', 9, 700) + R(66, 37, 90, 5, 'ph', 2.5)  # 위에서 내려온 알림 배너
        + arrow(276, 230))
# 채팅 창 (270x500 화면, 말풍선 안 회색 막대는 실제 대화가 들어갈 자리)
def bubble(x, y, w, n, cls, tail_right):
    h = 18 + n * 14
    out = R(x, y, w, h, cls, 14)
    for i in range(n):
        out += R(x + 14, y + 12 + i * 14, (w - 28) * (0.55 if i == n - 1 and n > 1 else 1), 6, 'ph', 3)
    return out
chat = (g(320, 0, R(10, 10, 270, 500, 'n', 30)
          + '<path d="M50 37 L43 44 L50 51" class="ln" stroke-width="2"/>' + chaticon(145, 40, 1)
          + T(256, 48, '38:15', 12, 700, 'end')
          + R(10, 66, 270, 364, 'soft', 0)  # 메시지가 오가는 판
          + '<path d="M10 66 H280" class="ln" opacity=".45"/>' + '<path d="M10 430 H280" class="ln" opacity=".45"/>'  # 위·아래 구분선
          + bubble(110, 84, 150, 2, 'lily', True)
          + bubble(30, 142, 170, 3, 'n', False)
          + bubble(130, 214, 130, 1, 'lily', True)
          + bubble(30, 258, 150, 2, 'n', False)
          + R(30, 444, 182, 44, 'n', 22)
          + '<circle cx="238" cy="466" r="22" class="lily"/><path d="M231 466 H245 M239 459 L246 466 L239 473" class="ln" stroke-width="2.2"/>'))
body = body + chat
S.append(section('14. 운영자 호출 (채팅)', svg(600, 520,
    '운영자 호출: 메인 화면 아래 독의 운영자 호출 앱 아이콘에 안 읽은 답장 수가 빨간 숫자로 뜨고, 답장이 오면 위에서 알림 배너가 내려온다. 누르면 채팅 창이 열린다. 위 줄(뒤로 · 채팅 아이콘 · 타이머) 아래와 입력 줄 위에 구분선이 있고, 그 사이 어두운 판에서 대화가 오간다. 참가자 말풍선은 오른쪽 보라, 운영자 말풍선은 왼쪽 회색. 말풍선 안 회색 막대는 대화 내용 자리.', body, 620)))
# 14. 연결이 끊겼을 때
wifi = ('<g transform="translate(145 214)"><path d="M-22 -4 A31 31 0 0 1 22 -4" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/>'
        '<path d="M-13 5 A18 18 0 0 1 13 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/>'
        '<circle cx="0" cy="14" r="3.5" fill="currentColor"/><path d="M-20 -18 L20 22" stroke="var(--via)" stroke-width="3" stroke-linecap="round"/></g>')
body = M(0, '33:40', 'soft') + wifi + T(145, 268, '연결이 끊겼습니다', 15, 700, 'middle')
S.append(section('15. 연결이 끊겼을 때', svg(290, 460,
    '연결이 끊겼을 때: 가운데 영역에 끊긴 와이파이 아이콘과 "연결이 끊겼습니다" 문구만 뜬다. 로딩 표시는 없다. 타이머는 그대로, 아래 독 아이콘은 흐려져 눌리지 않는다. 상태 표시줄 와이파이도 끊김 표시.', body, 300)))


# ---- 새 화면 6개 ----
# 목표 창: 장소와 할 일
body = (M(0, '56:10') + T(56, 160, '현재 목표', 11, cls='t-lily') + T(56, 182, '알렉스의 승인 확보', 15, 700)
        + '<path d="M56 202 H234" class="ln" opacity=".2"/>' + place(56, 226, '알렉스의 방', 170))
S.append(section('목표 창: 장소와 할 일', svg(290, 460,
    '1부 목표 창: 위에 현재 목표, 그 아래 장소 핀과 방 이름, 맨 아래 해야 할 일 자리(회색 막대, 문구 미정).', body, 300)))

# 지도 팝업: 방 이름을 누르면 우주선 지도에서 갈 방이 그 사람 색으로
from shipmap import svg_map
goalwin = lambda o: (T(56+o, 160, '현재 목표', 11, cls='t-lily') + T(56+o, 182, '알렉스의 승인 확보', 15, 700)
                     + f'<path d="M{56+o} 202 H{234+o}" class="ln" opacity=".2"/>' + place(56+o, 226, '알렉스의 방', 170))
body = (M(0, '56:10') + goalwin(0) + arrow(276, 230)
        + M(310, '56:10') + goalwin(310) + R(330, 10, 250, 440, 'soft', 30, ' opacity=".88"')
        + R(342, 140, 226, 186, 'n', 12) + '<circle cx="548" cy="162" r="11" class="n"/>'
        + '<path d="M543.5 157.5 L552.5 166.5 M552.5 157.5 L543.5 166.5" class="ln" stroke-width="1.8" stroke-linecap="round"/>'
        + svg_map(354, 188, 0.712, '알렉스'))
S.append(section('지도 팝업', svg(600, 460,
    '지도 팝업: 목표 창의 방 이름(옆에 꺾쇠)을 누르면 화면이 어두워지고 우주선 지도가 뜬다. 벽이나 문 없이 우주선 바닥 윤곽 하나 안에 위 줄 알렉스·릴리·에바, 아래 줄 오펠리아·노아 구역 이름이 놓이고, 지금 가야 할 알렉스 구역만 은은한 빨간색으로 칠해진다. 오른쪽 위 X나 바깥을 누르면 닫힌다.', body, 620)))

# 완료 목표 다시 보기
rows = ['알렉스의 승인 확보', '오펠리아의 승인 확보', '노아의 승인 확보', '오펠리아 재방문']
lst = ''
for i, t in enumerate(rows):
    y = 80 + i * 54
    lst += R(30, y, 230, 44, 'n') + f'<circle cx="52" cy="{y+22}" r="10" class="bar"/>' + ck(52, y + 22, 0.9, 2) + T(72, y + 27, t, 13, 700)
lst += (R(30, 80 + 4 * 54 + 8, 230, 64, 'lily', 10) + T(46, 80 + 4 * 54 + 32, '현재 목표', 11, cls='t-lily')
        + T(46, 80 + 4 * 54 + 54, '에바의 승인 확보', 14, 700))
body = (M(0, '38:15') + T(56, 160, '현재 목표', 11, cls='t-lily') + T(56, 182, '에바의 승인 확보', 15, 700) + place(56, 216, '에바의 방', 170)
        + listicon(228, 148)
        + arrow(276, 230)
        + g(320, -10, R(10, 10, 270, 500, 'n', 30) + '<path d="M50 37 L43 44 L50 51" class="ln" stroke-width="2"/>'
            + T(145, 49, '완료 목표', 14, 700, 'middle') + T(256, 48, '38:15', 12, 700, 'end') + lst))
S.append(section('완료 목표 다시 보기', svg(600, 510,
    '완료 목표 다시 보기: 목표 창 오른쪽 위 목록 버튼을 누르면 끝낸 목표가 체크와 함께 순서대로 나오고, 맨 아래에 현재 목표가 보라색으로 표시된다.', body, 620)))

# 보너스 패턴 오답
wrong = [pts[0], pts[1], pts[2]]
wl = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in wrong)
wdots = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if (x, y) in wrong else 7}" '
                + (f'fill="{RED}"' if (x, y) in wrong else 'class="soft"') + '/>' for x, y in pts)
clear = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="soft"/>' for x, y in pts)
body = (C(0, '17:40') + f'<path d="{wl}" class="vline" style="stroke:{RED}"/>' + wdots
        + arrow(286, 250) + g(320, 0, C(0, '17:39') + clear))
S.append(section('보너스 패턴 오답', svg(600, 520,
    '보너스 패턴 오답: 틀린 선과 지난 점이 빨갛게 바뀐 뒤, 선이 지워지고 점 일곱 개가 처음 상태로 돌아간다. 문구는 없다.', body, 620)))

# 16·17. 엔딩 (문구는 시나리오 엔딩 연출의 시스템 음성 그대로)
frame = lambda: R(10, 10, 270, 500, 'n', 30)
def sig(x, y):  # 송출 아이콘: 점 + 퍼지는 호
    return (f'<circle cx="{x}" cy="{y}" r="5" class="vfill"/>'
            + ''.join(f'<path d="M{x-r} {y-r*0.6} A{r} {r} 0 0 1 {x+r} {y-r*0.6}" fill="none" class="ln" stroke-width="2" opacity="{1-i*0.25}"/>' for i, r in enumerate((14, 24, 34))))
glitch = ''.join(R(40 + (i * 37) % 120, 300 + i * 22, min(90 + (i * 53) % 80, 250 - (40 + (i * 37) % 120)), 6, 'soft', 3) for i in range(5))
esc = (frame() + T(145, 250, '탈출 절차를 시—', 15, 700, 'middle') + glitch
       + arrow(286, 260) + g(320, 0, R(10, 10, 270, 500, 'n', 30, ' style="fill:#000;stroke:#000"')))
S.append(section('16. 탈출 엔딩', svg(600, 520,
    '탈출 엔딩: 레버를 내리면 화면에 시스템 음성 탈출 절차를 시— 가 뜨다가 지직거리며 끊기고, 다음 화면은 완전히 꺼진 검은 화면.', esc, 620)))
note = '<path d="M150 230 V196 L170 190 V224" fill="none" class="ln" stroke-width="2.4"/><circle cx="145" cy="231" r="6" class="vfill"/><circle cx="165" cy="225" r="6" class="vfill"/>'
p1 = frame() + sig(145, 220) + T(145, 290, '행성 프로젝트를 실행합니다.', 14, 700, 'middle')
p2 = frame() + sig(145, 200) + note.replace('M150', 'M210').replace('cx="145"', 'cx="205"').replace('cx="165"', 'cx="225"').replace('V196 L170 190', 'V196 L230 190') + T(145, 290, '공개 구조 신호 송출을', 14, 700, 'middle') + T(145, 312, '시작합니다.', 14, 700, 'middle')
p3 = (frame() + sig(145, 170)
      + ''.join(T(145, 250 + i * 30, t, 14, 700, 'middle', 't-via' if i == 3 else '') for i, t in enumerate(['공개 구조 신호 송출 중.', '좌표 전송 중.', '생체 반응 전송 중.', '여기는 알파. 여기는 알파…'])))
planet = p1 + arrow(286, 260) + g(320, 0, p2) + arrow(606, 260) + g(640, 0, p3)
S.append(section('17. 행성 엔딩', svg(920, 520,
    '행성 엔딩: 레버를 올리면 송출 아이콘과 행성 프로젝트를 실행합니다, 이어서 노래 표시와 공개 구조 신호 송출을 시작합니다, 마지막은 송출 중 · 좌표 전송 중 · 생체 반응 전송 중 · 여기는 알파 화면이 반복된다.', planet, 640)))

# 시간 종료: 타이머 00:00 → 숫자 빨강 → 전체 화면 (문구와 그 뒤 진행은 정하지 않음)
red00 = lambda x, y, fs: f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{fs}" font-weight="700" style="fill:{RED}">0:00:00</text>'
tz1 = (M(0, '') + R(40, 52, 210, 58, 'n', 10, f' style="fill:none;stroke:{RED};stroke-width:2"') + red00(145, 99, 24)
       + T(56, 160, '현재 목표', 11, cls='t-lily') + T(56, 182, '릴리의 승인', 15, 700))
tz2 = R(20, 10, 250, 440, 'n', 30) + red00(145, 228, 46) + R(85, 262, 120, 8, 'ph', 4) + R(100, 278, 90, 8, 'ph', 4)
S.append(section('시간 종료', svg(580, 460,
    '시간 종료: 타이머가 0:00:00이 되면 숫자와 타이머 칸이 빨갛게 바뀌고, 이어서 화면 전체에 빨간 0:00:00과 안내 문구 자리가 뜬다. 문구와 그 뒤 진행은 아직 정하지 않았다.', tz1 + arrow(276, 230) + g(310, 0, tz2), 600)))

# 버튼 색 규칙 (화면 제안 맨 위)
rows = [('기본', '평소 모든 버튼', ('n', ''), ('n', ''), '진행도'),
        ('켜짐', '눌러서 내용이 펼쳐진 버튼', ('lily', ''), ('via', ''), '힌트 보기'),
        ('다음 단계', '다음 힌트', ('n', 't-lily'), ('n', 't-via'), '다음 힌트'),
        ('정답', '1부 · 2부 같은 색, 힌트와 구별', ('inv', 't-inv'), ('inv', 't-inv'), '정답 보기')]
body = T(290, 34, '1부', 12, 700, 'middle', 't-lily') + T(470, 34, '2부', 12, 700, 'middle', 't-via')
for i, (name, sub, a, b, txt) in enumerate(rows):
    y = 50 + i * 62
    body += T(20, y + 20, name, 14, 700) + T(20, y + 38, sub, 11, cls='t-mute')
    for x, (cls, tc) in ((210, a), (390, b)):
        body += R(x, y, 160, 44, cls, 10) + T(x + 80, y + 27, txt, 13, 700, 'middle', tc)
rule_sec = section('버튼 색 규칙', svg(580, 300, '버튼 색 규칙. 기본 버튼은 회색. 눌러서 내용이 펼쳐진 버튼은 1부 보라, 2부 주황으로 채움. 다음 힌트 버튼은 회색 바탕에 강조색 글씨. 정답 보기는 1부와 2부 모두 시스템 회색으로 채움.', body, 600))
mark = '<p class="coltitle">화면 제안</p>' + chr(10)
k0 = s.index(mark) + len(mark)
s = s[:k0] + rule_sec + s[k0:]
k = s.index('</div>\n<div class="col">\n<p class="coltitle">순서도</p>')
s = s[:k] + ''.join(S) + s[k:]
p.write_text(s, encoding='utf-8'); print('ok')
