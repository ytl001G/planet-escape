# 힌트폰_에셋목록.html 생성 (post_assets.py가 이 파일의 <main> 안쪽을 논리도 페이지 아래에 붙인다)
import pathlib, sys
OK, TODO, WAIT = 'ok', 'todo', 'wait'
LABEL = {OK: '시안 있음', TODO: '만들 것', WAIT: '받아야 함'}

SCREENS = [
    ('시작 전 (설명용)', OK, '링 자리에 Start · 가짜 코드 0000으로 힌트 팝업 보여 주기 · 채팅 써 보기'),
    ('메인 · 안전 모드 이전', OK, '상태 표시줄 · 가운데 큰 흰 링 타이머 · 왼쪽 위 채팅 칸 · 아래 힌트코드 입력 창'),
    ('안전 모드 가동', OK, '감지·로딩 한 화면 → 진행 가이드, 2컷'),
    ('메인 · 1부', OK, '오른쪽 위 목표 칸(현재 목표 · 방 이름) · 링 보라 · 링 안 진행도 % 글 (막대 없음)'),
    ('메인 · 2부', OK, '오른쪽 위 칸에 V만 가운데 · 비아(VEA)가 말하면 V가 왼쪽으로 가고 음성 파형 (대사 글은 PC) · 링 주황'),
    ('지도 팝업', OK, '목표 칸 누르면 · 갈 방 인물 색 · 지나온 길 · 아직 못 가는 방 회색 · 실측 배치도 나오면 다시 맞춤'),
    ('목표 완료 → 다음 목표', OK, '1부만 · 목표 칸에 체크 원 + 목표 이름'),
    ('전환부 (ALONE 입력 뒤)', OK, '보라 그대로 · 진행도 50 고정 · 채팅 · 힌트 입력 막힘 · 목표 칸 문구 미정'),
    ('비아가 처음 나오는 순간', OK, '레버 내림 → 지직거림 → 주황 · 동그라미 ? → V · 버튼 막힘 이어짐'),
    ('코드 입력', OK, '메인 아래 입력 칸 · 힌트 보기 → 힌트 팝업'),
    ('진행도 %', OK, '타이머 링 안 글(막대 없음) · 서버에서 실시간으로 받음'),
    ('힌트 팝업 (1부 · 2부)', OK, '제목 문제 N · 힌트 보기 → 다음 → 정답 · 지금 부 코드만'),
    ('정답 보기 전 · 후', OK, '같은 자리에서 버튼 → 정답 칸'),
    ('보너스 패턴 → 카드 13.5', OK, '점 배치를 보너스 문제 담당과 맞춰야 함'),
    ('보너스 패턴 오답', OK, '빨간 선 → 초기화'),
    ('운영자 채팅', OK, '2부 말풍선 색 미정'),
    ('연결 끊김', OK, '전체 화면 덮개 · 타이머만 위에 보임 · 와이파이 아이콘 + 연결이 끊겼습니다'),
    ('탈출 엔딩', OK, '끊김 → 꺼짐 · 폰도 꺼지는지 확인 필요'),
    ('행성 엔딩', OK, '송출 화면 반복 · 보너스 후일담 반영 미정'),
    ('시간 종료', OK, '따로 페이지 없음 · 지금 화면에서 타이머 0:00:00 글자만 빨강 · 그 뒤 진행 미정'),
    ('정체 공개 뒤', WAIT, '폰에서 무엇을 보여 줄지 문서에 없음'),
]

# (묶음, 설명, [(에셋, 만들 것, 쓰는 화면, 상태, 메모)])
GROUPS = [
    ('배경', '1080 × 2408 PNG (갤럭시 A13) · 힌트폰/배경 폴더', [
        ('안전 모드 이전 배경', '무채색 성운 · 옅은 주사선 (bg_pre)', '메인(이전)', OK, ''),
        ('1부 배경', '릴리 보라 성운 (bg_part1)', '1부 전체', OK, ''),
        ('2부 배경', '비아 주황 성운 · 주사선 · 글리치 띠 (bg_part2)', '2부 전체', OK, ''),
        ('엔딩 배경', '탈출: 검정 (bg_end_escape) · 행성: 지평선 (bg_end_planet)', '엔딩', OK, ''),
    ]),
    ('채팅', '운영자 채팅 창 조각', [
        ('참가자 말풍선', '1줄 · 여러 줄', '운영자 채팅', OK, '2부 색 미정'),
        ('운영자 말풍선', '1줄 · 여러 줄', '운영자 채팅', OK, ''),
        ('채팅 위 줄', '뒤로 · 채팅 아이콘 · 타이머 + 아래 구분선', '운영자 채팅', OK, ''),
        ('채팅 판', '메시지가 오가는 어두운 판 · 입력 줄 위 구분선', '운영자 채팅', OK, ''),
        ('입력 칸', '빈 칸 · 입력 중', '운영자 채팅', OK, ''),
        ('보내기 버튼', '기본 · 눌림', '운영자 채팅', OK, ''),
        ('안 읽음 숫자', '1자리 · 2자리', '왼쪽 위 채팅 칸', OK, ''),
    ]),
    ('칸 · 카드', '화면 안에 놓이는 상자', [
        ('타이머 칸', '둥근 링(남은 시간만큼, 이전 흰색 · 1부 보라 · 2부 주황) · Start · 안에 진행도 글 · 시간 종료 땐 글자 빨강 · 채팅 위 줄용 작은 알약', '전체', OK, ''),
        ('목표 창', '오른쪽 위 칸 · 1부 목표 · 완료 체크 · 2부엔 V + 파형 · 누르면 지도', '메인 · 목표 완료', OK, ''),
        ('장소 줄', '핀 + 방 이름(인물 색) + 꺾쇠', '1부 메인', OK, ''),
        ('우주선 지도', '바닥 윤곽 하나 · 구역 이름 5개 · 갈 구역 인물 색 · 지나온 길 곡선 · 못 가는 방 회색 (벽 · 문 없음)', '지도 팝업', OK, '노션 공통 기준의 기존 배치 그림 기준'),
        ('비아 말 칸', '동그라미 ? / V + 음성 파형 (글 없음)', '2부 메인 · 비아 등장', OK, ''),
        ('코드 입력 칸', '빈 칸 · 입력됨(글자 그대로) · 오류(빨강)', '코드 입력', OK, ''),
        ('힌트 팝업 틀', '제목 문제 N · 닫기', '힌트 팝업', OK, ''),
        ('힌트 카드', '1부 · 2부 × 1~3줄 높이', '힌트 팝업', OK, ''),
        ('힌트 사용 횟수', '입력 칸 바로 위 · 코드 하나당 1회', '메인', OK, ''),
        ('정답 칸', '시스템 회색', '힌트', OK, ''),
        ('스토리카드 틀', '릴리 보라 · 에바 파랑 · 서명 없음', '스토리카드', TODO, '릴리 · 에바만 시안'),
        ('패턴 점 · 선', '점 기본 · 지남 · 선 · 오답(빨강)', '보너스 패턴', WAIT, '점 배치'),
    ]),
    ('버튼', '색은 위쪽 버튼 색 규칙을 따름', [
        ('한글 키보드', '숫자 줄 + 두벌식 3줄 + 시프트(쌍자음 · ㅒㅖ) · 지우기 · 한/영 · ? · 띄어쓰기 · . · 입력 칸을 눌러야 올라옴', '운영자 채팅', OK, '자음 · 모음을 누르면 글자로 조합 · 키 모양 A~E 고르는 중'),
        ('코드 키보드', '숫자 1줄 + 영문 3줄 + 지우기(P 줄 오른쪽 끝에 맞춤) · 입력 칸을 눌러야 올라오고, 맞는 코드를 확인하거나 밖을 누르면 내려감', '메인 아래 입력', OK, '폰 기본 키보드 대신 · 키 모양 A~E 고르는 중'),
        ('상태 표시줄', '시각 · 와이파이(끊기면 빨간 사선) · 배터리', '모든 화면', OK, ''),
        ('채팅 칸', '왼쪽 위 · 아이콘만 (채팅 글자 없음) · 안 읽음 숫자 · 막히면 흐림', '메인', OK, ''),
        ('힌트 보기', '입력 칸 옆 · 막히면 흐림', '메인', OK, ''),
        ('다음', '1부 · 2부', '힌트', OK, ''),
        ('정답', '버튼 → 정답 칸', '힌트', OK, ''),
    ]),
    ('아이콘', '', [
        ('방패', '', '안전 모드 감지 · 로딩', OK, '무늬 없음'),
        ('장소 핀', '', '목표 창', OK, ''),
        ('꺾쇠', '', '목표 칸 방 이름 옆', OK, ''),
        ('닫기', '', '지도 · 힌트 팝업', OK, ''),
        ('체크', '', '목표 완료', OK, ''),
        ('채팅 아이콘', '선으로 그린 말풍선 + 점 3개', '채팅 칸 · 채팅 위 줄', OK, '새 에셋 기본은 시안 E (주고받는 말풍선) · A~F 다 남겨 둠'),
        ('뒤로', '', '채팅', OK, ''),
        ('보내기', '', '채팅 입력', OK, ''),
        ('와이파이 끊김', '', '연결 끊김', OK, ''),
        ('연결 끊김 문구', '연결이 끊겼습니다', '연결 끊김', OK, ''),
        ('송출', '', '행성 엔딩', OK, ''),
        ('음표', '', '행성 엔딩', OK, ''),
        ('앱 아이콘', '행성탈출 로고 · 릴리 보라판 + 회색판 · 1024 / 512 / 192 / 144 PNG + SVG', '폰 바탕 화면', OK, '로고 폴더 app_icon · app_icon_gray'),
    ]),
]

MOTIONS = [
    ('안전 모드 감지', '방패가 커지며 나타남 + 아래 로딩 막대 → 메인으로 스르륵', '길이 · 자동 넘김'),
    ('목표 완료', '체크 → 다음 목표', '길이'),
    ('지도 팝업 열림', '화면 어두워짐 + 지도 떠오름', '길이'),
    ('비아 끼어들기', '보라 화면 지직거림 → 주황 덮기', '길이 · 진동 여부'),
    ('음성 파형', '비아가 말하는 동안', '실제 음성에 맞출지, 반복 움직임일지'),
    ('V 옮겨 감', '비아가 말할 때 V가 왼쪽으로 · 다 말하면 가운데로 돌아옴', '길이'),
    ('이름 바뀜', '? → V', '바뀌는 시점(대사 1002)'),
    ('다음 힌트 펼침', '팝업 안에 힌트 카드 추가 · 팝업은 처음 열 때만 떠오름', ''),
    ('키보드 올라옴', '입력 칸 누르면 아래에서 올라옴', '길이'),
    ('패턴 선 그리기', '보너스 패턴', ''),
    ('패턴 오답', '빨간 선 → 지워짐', '길이'),
    ('안 읽음 숫자 등장', '채팅 칸', '진동 · 소리 여부'),
    ('탈출 엔딩 끊김', '글자 지직거림 → 검은 화면', '길이'),
]



ASK = [
    ('전환부 목표 칸 문구', '기획', 'ALONE 입력 뒤 목표 칸 (지금 예시 문구)'),
    ('운영자 안내 문구', '기획', '채팅 첫 화면'),
    ('힌트 코드 · 스토리 코드 글자 수', '기획', '입력 칸 길이 (글자는 영문 대문자 + 숫자로 정함)'),
    ('진행도 값', '서버', '무엇을 기준으로 몇 %인지 · 2부는 50 이상인지 · 얼마나 자주 바뀌는지'),
    ('보너스 점 배치', '보너스 문제 담당', '인쇄물 그림과 폰 점이 같아야 함'),
    ('엔딩 때 폰', '총괄', '탈출 엔딩 셧다운 때 폰도 꺼지는지'),
    ('비아 음성 파일', '녹음', '파형 · 재생 길이'),
]

chip = lambda st, extra='': f'<span class="chip {st}">{LABEL[st]}</span>' + (f' {extra}' if extra else '')
def table(head, rows):
    h = ''.join(f'<th>{x}</th>' for x in head)
    b = ''.join('      <tr>' + ''.join(f'<td{c}>{v}</td>' for c, v in r) + '</tr>\n' for r in rows)
    return f'  <div class="tbl"><table>\n    <thead><tr>{h}</tr></thead>\n    <tbody>\n{b}    </tbody>\n  </table></div>\n'
def sec(title, small, inner):
    sm = f' <small>{small}</small>' if small else ''
    return f'<section>\n  <h2>{title}{sm}</h2>\n{inner}</section>\n\n'

all_assets = [a for _, _, rows in GROUPS for a in rows]
n_todo = sum(a[3] == TODO for a in all_assets) + sum(s[1] == TODO for s in SCREENS)
n_wait = sum(a[3] == WAIT for a in all_assets) + sum(s[1] == WAIT for s in SCREENS)
tally = [(len(SCREENS), '화면'), (len(all_assets), '에셋 조각'), (n_todo, '만들 것'), (n_wait, '받아야 함'), (len(ASK), '요청할 것')]

out = ['<header>\n  <h1>힌트폰 에셋 목록</h1>\n  <div class="legend">\n'
       + ''.join(f'    <span>{chip(k)} {d}</span>\n' for k, d in [(OK, '논리도에 그려 둠'), (TODO, '아직 안 그림'), (WAIT, '문구 · 값 · 결정이 먼저 필요')])
       + '  </div>\n</header>\n\n',
       '<section class="tally" aria-label="개수">\n' + ''.join(f'  <div><b>{n}</b><span>{t}</span></div>\n' for n, t in tally) + '</section>\n\n']
out.append(sec('화면', '실제 폰 크기로 완성본이 필요한 화면',
               table(['화면', '상태', '메모'], [[('', n), ('', chip(st)), (' class="scr"', m)] for n, st, m in SCREENS])))
# 에셋은 표 대신 실제 그림 카드로
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from thumbs import TH, MOTION_TH, svg as thumb, preview_b64
out.append('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><marker id="ahT" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="currentColor"/></marker></defs></svg>\n')
def card(name, sub, use, status_html, th):
    return ('    <article class="acard">' + thumb(th) + f'<b>{name}</b>'
            + (f'<span class="sub">{sub}</span>' if sub else '') + (f'<span class="use">{use}</span>' if use else '')
            + (f'<span class="st">{status_html}</span>' if status_html else '') + '</article>\n')
for title, small, rows in GROUPS:
    missing = [n for n, *_ in rows if n not in TH]; assert not missing, missing
    pre = ''
    if title == '배경' and preview_b64():
        pre = f'  <img class="bgprev" src="data:image/jpeg;base64,{preview_b64()}" alt="배경 5장 위에 메인 화면 UI를 얹은 미리보기: 안전 모드 이전, 1부, 2부, 행성 엔딩, 탈출 엔딩">\n'
    out.append(sec(title, small, pre + '  <div class="agrid">\n' + ''.join(card(n, w, u, chip(st, m), TH[n]) for n, w, u, st, m in rows) + '  </div>\n'))
missing = [m[0] for m in MOTIONS if m[0] not in MOTION_TH]; assert not missing, missing
out.append(sec('움직임', '개발팀에 길이 · 순서와 함께 넘길 것', '  <div class="agrid">\n'
    + ''.join(card(a, b, '', f'<span class="ask">정할 것: {c}</span>' if c else '', MOTION_TH[a]) for a, b, c in MOTIONS) + '  </div>\n'))
from asset_files import section as files_sec
fb, fn = files_sec()
if fn: out.append(sec('에셋 파일', f'힌트폰/에셋 폴더 · SVG + PNG@3x {fn}개 · 글자 없는 조각 · 1부 보라 · 2부 주황 · 이전(안전 모드 전) 흰색 · 시험해 보기에서 에셋 적용으로 입혀 볼 수 있음', fb))
out.append(sec('받아야 할 것', '디자인 전에 다른 담당에게 요청',
               table(['항목', '누구에게', '왜'], [[('', a), ('', f'<span class="who">{b}</span>'), (' class="scr"', c)] for a, b, c in ASK])))

assert len(SCREENS) == 21 and all(len(r) == 5 for r in all_assets)
html = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<title>힌트폰 에셋 목록</title>\n</head>\n<body>\n<main>\n'
        + ''.join(out) + '</main>\n</body>\n</html>\n')
pathlib.Path(sys.argv[1]).write_text(html, encoding='utf-8')
print('assets', tally)
