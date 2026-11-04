# 순서도: Graphviz(dot)로 자동 배치한 하나의 연결된 그림. 가운데 세로 줄 = 게임 진행, 화면 · 기능은 생기는 단계에서 옆으로 뻗음
import pathlib, sys, subprocess, re, html
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
DOT = r'C:\Program Files\Graphviz\bin\dot.exe'
ST = {'n': ('#211e26', '#4a4452', '#ece9f1'), 'lily': ('#33213b', '#cf86e6', '#ece9f1'), 'via': ('#36261a', '#ffae4d', '#ece9f1'),
      'inv': ('#d9d4e0', '#d9d4e0', '#17151b'), 'phase': ('#17151b', '#17151b', '#a39eab')}
N, Ed = [], []
def node(k, t, sub='', cls='n', shape='box'):
    f, c, fc = ST[cls]; e = html.escape
    lab = f'<<b>{e(t)}</b>' + (f'<br/><font point-size="10" color="#a39eab">{e(sub)}</font>' if sub else '') + '>'
    if cls == 'inv': lab = f'<<b>{e(t)}</b>>'
    N.append(f'"{k}" [label={lab} shape={shape} style="rounded,filled" fillcolor="{f}" color="{c}" fontcolor="{fc}"];')
def edge(a, b, lab='', dash=False, **kw):
    at = ''.join(f' {k}="{v}"' for k, v in kw.items())
    Ed.append(f'"{a}" -> "{b}" [label="{lab}"{" style=dashed" if dash else ""}{at}];')

# ── 게임 진행 (세로 줄) ──
SP = [('안전 모드 이전', 'n', [('게임 시작', '앱을 켜면 바로 홈 화면 · 1:45:00 시작'), ('문제 0 이름 입력', '메인 컴퓨터 · 힌트 3단계'), ('스토리카드 1', '실물 카드 · 폰에 안 뜸'), ('문제 1 본인 확인 질문', '메인 컴퓨터 · 힌트 없음')]),
      ('1부 릴리 안내', 'lily', [('안전 모드 알림', '방패가 커지며 등장 + 로딩 막대 · 전체 화면'), ('진행 가이드 시작', '현재 목표 · 장소 · 할 일'), ('알렉스의 승인 확보', '문제 2 · 태블릿'), ('오펠리아의 승인 확보', '문제 3 · 태블릿'), ('노아의 승인 확보', '문제 4 · 태블릿'), ('오펠리아 재방문', '문제 5 · 오펠리아 태블릿'), ('에바의 승인 확보', '문제 6 · 태블릿 · 카드 6'), ('릴리의 승인', '문제 7 · 메인 컴퓨터 · 카드 7')]),
      ('전환부', 'n', [('실행자 신원 확인', '문제 8 · 메인 컴퓨터 · 카드 8'), ('ALONE 입력 · 레버 하강', '문제 9 · 메인 컴퓨터 · 카드 9')]),
      ('2부 비아 안내', 'via', [('비아 등장', '안내자 교체 · 보라 → 주황 · 대사 1001'), ('알렉스의 방 2차', '문제 10 · 비아 대사 1008'), ('오펠리아의 방 2차', '문제 11 · 비아 대사 1137'), ('노아의 방 2차', '문제 12 · 비아 대사 1209'), ('에바의 방 2차', '문제 13 · 비아 대사 1322'), ('릴리의 방 2차', '문제 14 · 비아 대사 1432'), ('LOVE 입력', '문제 15 · 비아 정체 공개 · 카드 15'), ('레버 선택', '문제 16 · 카드 16')])]
EL = {('문제 1 본인 확인 질문', '안전 모드 알림'): '실패', ('안전 모드 알림', '진행 가이드 시작'): '로딩 끝나면 자동', ('릴리의 승인', '실행자 신원 확인'): '안전 모드 해제'}
spine = []
for ph, cls, nodes in SP:
    for t, sub in nodes: node(t, t, sub, cls if t != '비아 등장' else 'via'); spine.append(t)
for a, b in zip(spine, spine[1:]): edge(a, b, EL.get((a, b), ''), weight=20)
node('탈출 엔딩', '탈출 엔딩', '레버 아래 · 폰 꺼짐'); node('행성 엔딩', '행성 엔딩', '레버 위 · 송출 화면 반복', 'via')
edge('레버 선택', '탈출 엔딩', '레버 아래'); edge('레버 선택', '행성 엔딩', '레버 위')

# ── 홈 · 채팅 (게임 시작에서) ──
node('홈', '홈 화면 (안전 모드 전)', '상태 표시줄 · 가운데 큰 링 타이머 · 독')
node('채팅', '운영자 채팅', '독 말풍선 아이콘 · 위 줄 아래 구분선')
node('한글kb', '한글 키보드', '두벌식 · 시프트 · 한/영 · 띄어쓰기')
node('배너', '알림 배너', '채팅 밖에서 답장 오면 위에 3.5초')
edge('게임 시작', '홈'); edge('홈', '채팅', '독: 운영자 호출'); edge('채팅', '한글kb', '입력 칸 누름'); edge('한글kb', '채팅', '대화 쪽 누르면 내림', True)
edge('채팅', '배너', '답장 (채팅 밖일 때)'); edge('배너', '채팅', '누르면', True)
# ── 힌트코드 앱 → 코드 키보드 → 코드 판별 ──
node('힌트앱', '힌트코드 앱', '위 줄: 뒤로 · 제목 · 알약 타이머')
node('코드kb', '코드 키보드', '입력 칸 누름 · 숫자 + 영문 + ⌫')
node('스토리앱', '스토리코드 앱', '독에 톡 생김', 'via')
node('판별', '코드 판별', '지금 부와 앱에 맞는 코드만', shape='diamond')
edge('홈', '힌트앱', '독: 힌트코드'); edge('힌트앱', '코드kb', '입력 칸 누름'); edge('코드kb', '판별', '힌트 보기 · 진행도')
edge("비아 등장", "스토리앱", "독에 생김", True, constraint="false"); edge('스토리앱', '판별', '확인')
ROWS = [('없는', '없는 코드', '', [('반응 없음', '펼쳐 둔 앞 코드 힌트만 걷힘', 'n')]),
        ('1부', '1부 코드', '비아 등장 전 문제', 'lily'),
        ('2부전', '2부 코드', '비아 등장 전에 넣으면', [('반응 없음', '1부엔 비아 힌트 없음', 'n')]),
        ('2부', '2부 코드', '비아 등장 후 · 문제 10 ~ 15', 'via'),
        ('16', '문제 16 코드', '비아 등장 후', [('대기 1 ~ 6', '넣을 때마다 다음 단계', 'via'), ('심장 소리', '6단계 뒤 반복', 'n')]),
        ('스토리', '스토리 코드', '스토리코드 앱 · 보너스', [('패턴 입력', '오답: 빨간 선 → 초기화', 'n'), ('카드 13.5', '패턴 정답', 'via')])]
for k, t, sub, res in ROWS:
    node('r' + k, t, sub); edge('판별', 'r' + k)
    if isinstance(res, str): res = [(f'힌트 {i}', '', res) for i in (1, 2, 3)] + [('정답', '정답 보기는 힌트를 다 본 뒤', 'inv')]
    prev = 'r' + k
    for i, (t2, s2, c2) in enumerate(res):
        nk = f'r{k}_{i}'; node(nk, t2, s2, c2); edge(prev, nk, '다음 힌트' if i and len(res) == 4 else ''); prev = nk
node('힌트규칙', '힌트 펼침', '버튼 줄 아래로 · 연 단계는 다시 볼 수 있음 · 맞는 코드면 키보드 내림')
node('진행도', '진행도', '맞는 코드면 버튼 자리에 % · 힌트를 펼쳐도 남음')
edge('r1부', '힌트규칙', '', True); edge('판별', '진행도', '진행도 (같은 판별)')
# ── 진행 가이드 시작 → 메인 화면 ──
node('메인', '메인 화면 (안전 모드 뒤)', '링 타이머(남은 시간만큼) · 목표 창 · 독', 'lily')
node('지도', '지도 팝업', '갈 방만 인물 색 · X · 바깥 · Esc로 닫힘', 'lily')
node('다시보기', '완료 목표 다시 보기', '목표 창 목록 버튼 · 끝낸 목표 체크', 'lily')
node('완료', '목표 완료 화면', '승인될 때마다 체크 표시 → 다음 목표', 'lily')
node('끊김', '연결 끊김', '와이파이 아이콘 + 연결이 끊겼습니다'); node('재연결', '다시 연결', '원래 화면으로')
node('종료', '시간 종료', '0:00:00 → 전체 화면 · 이후 미정')
edge('진행 가이드 시작', '메인'); edge('메인', '지도', '방 이름 누름'); edge('메인', '다시보기', '목록 버튼')
edge('알렉스의 승인 확보', '완료', '문제 2 ~ 7 승인마다', True)
edge('메인', '끊김', '어느 화면에서든'); edge('끊김', '재연결'); edge('메인', '종료', '타이머 0:00:00')
edge('메인', '힌트앱', '독 (홈과 같음)', True, constraint='false')

dot = ('digraph G {\n graph [rankdir=TB bgcolor="transparent" nodesep=0.35 ranksep=0.42 fontname="Malgun Gothic" newrank=true];\n'
       ' node [fontname="Malgun Gothic" fontsize=12 margin="0.26,0.08" penwidth=1.4];\n'
       ' edge [fontname="Malgun Gothic" fontsize=10 color="#8a8494" fontcolor="#a39eab" arrowsize=0.7 penwidth=1.2];\n '
       + '\n '.join(N + Ed)
       + '\n { rank=same; "게임 시작"; "홈"; }\n { rank=same; "진행 가이드 시작"; "메인"; }\n}\n')
pathlib.Path(__file__).with_name('flow.dot').write_text(dot, encoding='utf-8')
out = subprocess.run([DOT, '-Tsvg'], input=dot.encode('utf-8'), capture_output=True, check=True).stdout.decode('utf-8')
svg = out[out.index('<svg'):]
import re as _re; WPT = float(_re.search(r'<svg width="([\d.]+)pt"', svg)[1])  # 실제 크기로 보이게 (글자가 작아지지 않게)
svg = re.sub(r'<svg width="[^"]*" height="[^"]*"', '<svg role="img" aria-label="힌트폰 전체 순서도 하나. 가운데 세로 줄은 게임 진행 순서이고, 홈 화면 · 채팅 · 힌트코드 앱 · 코드 판별 · 메인 화면 · 지도 같은 화면과 기능이 생기는 단계에서 화살표로 이어진다." style="width:' + f'{WPT*1.25:.0f}' + 'px;max-width:none;height:auto;display:block"', svg, count=1)
svg = re.sub(r'<!--.*?-->\n?', '', svg, flags=re.S).replace('<title>G</title>', '')
svg = re.sub(r'<polygon fill="white" stroke="none"[^>]*/>', '', svg, count=1)  # dot 배경 흰 판 지움
svg = re.sub(r'<text ([^>]*?)fill="([^"]+)"', r'<text \1style="fill:\2"', svg)  # 페이지 CSS가 글자 색을 덮지 않게
svg = svg.replace('font-family="Malgun Gothic,', 'font-family="Malgun Gothic, Apple SD Gothic Neo,').replace('font-family="Malgun Gothic"', 'font-family="Malgun Gothic, Apple SD Gothic Neo, sans-serif"')
a = s.index('<svg', s.index('<p class="coltitle">순서도</p>')); b = s.index('</svg>', a) + 6
s = s[:a] + '<div style="overflow-x:auto">' + svg.strip() + '</div>' + s[b:]
p.write_text(s, encoding='utf-8'); print('ok dot', len(N), 'nodes', len(Ed), 'edges')
