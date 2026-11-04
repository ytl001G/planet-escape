# 순서도 2개 (Graphviz dot 자동 배치): ① 게임 진행에 따른 폰 화면 (세로) ② 폰 화면 이동 (가로). 폰 화면에 영향 주는 것만 씀
import pathlib, sys, subprocess, re, html
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
DOT = r'C:\Program Files\Graphviz\bin\dot.exe'
ST = {'n': ('#211e26', '#4a4452', '#ece9f1'), 'lily': ('#33213b', '#cf86e6', '#ece9f1'), 'via': ('#36261a', '#ffae4d', '#ece9f1'), 'inv': ('#d9d4e0', '#d9d4e0', '#17151b')}

class G:
    def __init__(self): self.N, self.E = [], []
    def node(self, k, t, sub='', cls='n', shape='box', group=''):
        f, c, fc = ST[cls]; e = html.escape
        lab = f'<<b>{e(t)}</b>' + (f'<br/><font point-size="10" color="#a39eab">{e(sub)}</font>' if sub else '') + '>'
        g = f' group="{group}"' if group else ''
        self.N.append(f'"{k}" [label={lab}{g} shape={shape} style="rounded,filled" fillcolor="{f}" color="{c}" fontcolor="{fc}"];')
    def edge(self, a, b, lab='', dash=False, **kw):
        at = ''.join(f' {k}="{v}"' for k, v in kw.items())
        self.E.append(f'"{a}" -> "{b}" [label="{lab}"{" style=dashed" if dash else ""}{at}];')
    def svg(self, rankdir, aria):
        dot = (f'digraph G {{\n graph [rankdir={rankdir} bgcolor="transparent" nodesep=0.3 ranksep=0.45 fontname="Malgun Gothic" newrank=true];\n'
               ' node [fontname="Malgun Gothic" fontsize=12 margin="0.26,0.08" penwidth=1.4];\n'
               ' edge [fontname="Malgun Gothic" fontsize=10 color="#8a8494" fontcolor="#a39eab" arrowsize=0.7 penwidth=1.2];\n '
               + '\n '.join(self.N + self.E) + '\n}\n')
        out = subprocess.run([DOT, '-Tsvg'], input=dot.encode('utf-8'), capture_output=True, check=True).stdout.decode('utf-8')
        v = out[out.index('<svg'):]
        w = float(re.search(r'<svg width="([\d.]+)pt"', v)[1])  # 실제 크기로 (글자가 작아지지 않게)
        v = re.sub(r'<svg width="[^"]*" height="[^"]*"', f'<svg role="img" aria-label="{aria}" style="width:{w*1.25:.0f}px;max-width:none;height:auto;display:block"', v, count=1)
        v = re.sub(r'<!--.*?-->\n?', '', v, flags=re.S).replace('<title>G</title>', '')
        v = re.sub(r'<polygon fill="white" stroke="none"[^>]*/>', '', v, count=1)  # dot 배경 흰 판 지움
        v = re.sub(r'<text ([^>]*?)fill="([^"]+)"', r'<text \1style="fill:\2"', v)  # 페이지 CSS가 글자 색을 덮지 않게
        v = v.replace('font-family="Malgun Gothic,', 'font-family="Malgun Gothic, Apple SD Gothic Neo,').replace('font-family="Malgun Gothic"', 'font-family="Malgun Gothic, Apple SD Gothic Neo, sans-serif"')
        return dot, '<div style="overflow-x:auto">' + v.strip() + '</div>'

# ① 게임 진행에 따른 폰 화면: 화면이 바뀌는 때만
A = G()
SP = [('시작', '홈 화면', '앱을 켜면 바로 · 가운데 큰 링 타이머(흰색) 1:45:00 · 독: 힌트코드 · 채팅', 'n'),
      ('안전', '안전 모드 알림', '방패가 커지며 등장 + 로딩 막대 · 전체 화면', 'lily'),
      ('메인', '메인 화면 (1부)', '링 타이머 보라 · 목표 창 · 릴리 안내', 'lily'),
      ('g1', '목표: 알렉스의 승인 확보', '문제 2', 'lily'), ('g2', '목표: 오펠리아의 승인 확보', '문제 3', 'lily'), ('g3', '목표: 노아의 승인 확보', '문제 4', 'lily'),
      ('g4', '목표: 오펠리아 재방문', '문제 5', 'lily'), ('g5', '목표: 에바의 승인 확보', '문제 6', 'lily'), ('g6', '목표: 릴리의 승인', '문제 7', 'lily'),
      ('비아', '비아 등장', '보라 → 주황 · 독에 스토리코드 앱 톡 생김 · 대사 1001', 'via'),
      ('b1', '비아 안내: 알렉스의 방', '문제 10 · 대사 1008', 'via'), ('b2', '비아 안내: 오펠리아의 방', '문제 11 · 대사 1137', 'via'), ('b3', '비아 안내: 노아의 방', '문제 12 · 대사 1209', 'via'),
      ('b4', '비아 안내: 에바의 방', '문제 13 · 대사 1322', 'via'), ('b5', '비아 안내: 릴리의 방', '문제 14 · 대사 1432', 'via'), ('b6', '비아 정체 공개', '문제 15 LOVE 입력 뒤', 'via'),
      ('레버', '레버 선택', '문제 16 · 폰은 힌트 코드로 레버 대기 연출', 'via')]
EL = {('시작', '안전'): '문제 1 실패', ('안전', '메인'): '로딩 끝나면 자동', ('메인', 'g1'): '', ('g6', '비아'): '문제 8 · 9 뒤'}
for k, t, sub, cls in SP: A.node(k, t, sub, cls, group='spine')
ks = [k for k, *_ in SP]
for a, b in zip(ks, ks[1:]):
    A.edge(a, b, EL.get((a, b), '승인 → 목표 완료 체크' if a.startswith('g') else ''), weight=50)
A.node('탈출', '탈출 엔딩', '레버 아래 · 폰 꺼짐'); A.node('행성', '행성 엔딩', '레버 위 · 송출 화면 반복', 'via')
A.edge('레버', '탈출', '레버 아래'); A.edge('레버', '행성', '레버 위')
dot1, svg1 = A.svg('TB', '순서도 1 게임 진행에 따른 폰 화면. 홈 화면, 문제 1 실패 뒤 안전 모드 알림, 1부 메인 화면과 목표 6개, 비아 등장, 비아 안내 6단계, 레버 선택, 엔딩 두 가지.')

# ② 폰 화면 이동: 왼쪽에서 오른쪽으로
B = G()
B.node('홈', '홈 · 메인 화면', '독: 힌트코드 · 채팅 (+ 2부엔 스토리코드)')
B.node('힌트앱', '힌트코드 앱', '위 줄: 뒤로 · 제목 · 알약 타이머')
B.node('스토리앱', '스토리코드 앱', '비아 등장 뒤에만 독에 있음', 'via')
B.node('코드kb', '코드 키보드', '입력 칸 누르면 · 숫자 + 영문 + ⌫')
B.node('판별', '코드 판별', '지금 부와 앱에 맞는 코드만', shape='diamond')
B.edge('홈', '힌트앱', '독'); B.edge('홈', '스토리앱', '독 (2부)'); B.edge('힌트앱', '코드kb', '입력 칸'); B.edge('스토리앱', '코드kb', '입력 칸')
B.edge('코드kb', '판별', '힌트 보기 · 진행도 · 확인')
ROWS = [('없는', '없는 코드', '', [('반응 없음', '펼쳐 둔 앞 코드 힌트만 걷힘', 'n')]),
        ('1부', '1부 코드', '비아 등장 전 문제', 'lily'),
        ('2부전', '2부 코드 (비아 등장 전)', '', [('반응 없음', '1부엔 비아 힌트 없음', 'n')]),
        ('2부', '2부 코드', '비아 등장 후 · 문제 10 ~ 15', 'via'),
        ('16', '문제 16 코드', '비아 등장 후', [('대기 1 ~ 6', '같은 코드 넣을 때마다 다음 단계', 'via'), ('심장 소리', '6단계 뒤 반복', 'n')]),
        ('스토리', '스토리 코드', '스토리코드 앱 · 보너스', [('패턴 입력', '오답: 빨간 선 → 초기화', 'n'), ('카드 13.5', '패턴 정답', 'via')]),
        ('진행도', '진행도 버튼', '맞는 코드일 때', [('% 표시', '버튼 자리에 · 힌트를 펼쳐도 남음', 'n')])]
for k, t, sub, res in ROWS:
    B.node('r' + k, t, sub); B.edge('판별', 'r' + k)
    if isinstance(res, str): res = [(f'힌트 {i}', '버튼 줄 아래로 펼침' if i == 1 else '', res) for i in (1, 2, 3)] + [('정답', '', 'inv')]
    prev = 'r' + k
    for i, (t2, s2, c2) in enumerate(res):
        nk = f'r{k}_{i}'; B.node(nk, t2, s2, c2)
        B.edge(prev, nk, ('다음 힌트' if i < 3 else '정답 보기') if len(res) == 4 and i else ''); prev = nk
B.node('채팅', '운영자 채팅', '위 줄 아래 구분선'); B.node('한글kb', '한글 키보드', '두벌식 · 시프트 · 한/영 · 띄어쓰기')
B.node('배너', '알림 배너', '채팅 밖에서 답장 오면 위에 3.5초')
B.edge('홈', '채팅', '독'); B.edge('채팅', '한글kb', '입력 칸'); B.edge('배너', '채팅', '누르면')
B.node('지도', '지도 팝업', '1부 · 갈 방만 인물 색 · X · 바깥 · Esc로 닫힘', 'lily'); B.node('다시보기', '완료 목표 다시 보기', '1부 · 끝낸 목표 체크', 'lily')
B.edge('홈', '지도', '목표 창 방 이름'); B.edge('홈', '다시보기', '목표 창 목록 버튼')
B.node('어디서든', '어느 화면에서든')
B.node('끊김', '연결 끊김', '와이파이 아이콘 + 연결이 끊겼습니다'); B.node('재연결', '다시 연결', '원래 화면으로')
B.node('종료', '시간 종료', '0:00:00 → 전체 화면 · 이후 미정')
B.edge('어디서든', '끊김', '와이파이 끊김'); B.edge('끊김', '재연결'); B.edge('어디서든', '종료', '타이머 0:00:00'); B.edge('어디서든', '배너', '답장 옴')
dot2, svg2 = B.svg('LR', '순서도 2 폰 화면 이동. 홈과 메인 화면에서 힌트코드 앱이나 스토리코드 앱, 코드 키보드, 코드 판별을 거쳐 힌트와 정답으로 간다. 채팅과 한글 키보드, 알림 배너, 지도 팝업, 연결 끊김, 시간 종료도 있다.')

pathlib.Path(__file__).with_name('flow.dot').write_text(dot1 + '\n' + dot2, encoding='utf-8')
h3 = lambda t, top: f'<h3 style="font:700 16px var(--display);margin:{top}px 0 10px">{t}</h3>'
block = h3('1. 게임 진행에 따른 폰 화면', 6) + svg1 + h3('2. 폰 화면 이동', 28) + svg2
a = s.index('<svg', s.index('<p class="coltitle">순서도</p>')); b = s.index('</svg>', a) + 6
s = s[:a] + block + s[b:]
p.write_text(s, encoding='utf-8'); print('ok dot 2 charts', len(A.N), len(B.N))
