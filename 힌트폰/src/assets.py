# 힌트폰_에셋목록.html 생성 (post_assets.py가 이 파일의 <main> 안쪽을 논리도 페이지 아래에 붙인다)
import pathlib, sys
OK, TODO, WAIT = 'ok', 'todo', 'wait'
LABEL = {OK: '시안 있음', TODO: '만들 것', WAIT: '받아야 함'}

SCREENS = [
    ('메인 · 안전 모드 이전', OK, '타이머 · 빈 진행 가이드 · 힌트 버튼'),
    ('안전 모드 가동', OK, '감지·로딩 한 화면 → 진행 가이드, 2컷'),
    ('메인 · 1부', OK, '현재 목표 · 장소 · 할 일'),
    ('목표 창: 장소와 할 일', OK, '할 일 문구 받아야 함'),
    ('메인 · 2부', OK, '비아 말 · 2부 목표 문구는 받아야 함'),
    ('지도 팝업', OK, '방 이름 누르면 · 갈 방 하이라이트 · 실측 배치도 나오면 다시 맞춤'),
    ('목표 완료 → 다음 목표', OK, '1부만 그림'),
    ('완료 목표 다시 보기', OK, '목록 버튼 · 끝낸 목표 체크 · 현재 목표'),
    ('비아가 처음 나오는 순간', OK, '지직거림 → 주황 덮기 · 이름 ? → 비아'),
    ('코드 입력', OK, '입력 칸 · 힌트 보기 · 진행도'),
    ('진행도 %', OK, '% 기준(전체 / 문제별) 미정'),
    ('힌트 펼침 (1부 · 2부)', OK, '다음 힌트 · 다 보면 정답 보기'),
    ('정답 보기 전 · 후', OK, '같은 자리에서 버튼 → 정답 칸'),
    ('문제 16 힌트', OK, '레버 대기 6단계 · 화자 여럿 · 6칸 점 · 6단계 뒤 심장 소리 · 정답 보기 없음'),
    ('보너스 패턴 → 카드 13.5', OK, '점 배치를 보너스 문제 담당과 맞춰야 함'),
    ('보너스 패턴 오답', OK, '빨간 선 → 초기화'),
    ('운영자 채팅', OK, '2부 말풍선 색 미정'),
    ('연결 끊김', OK, '와이파이 아이콘 + 연결이 끊겼습니다 · 로딩 표시 없음'),
    ('탈출 엔딩', OK, '끊김 → 꺼짐 · 폰도 꺼지는지 확인 필요'),
    ('행성 엔딩', OK, '송출 화면 반복 · 보너스 후일담 반영 미정'),
    ('시간 종료', OK, '0:00:00 빨간 숫자 → 전체 화면 · 문구와 그 뒤 진행 미정'),
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
        ('안 읽음 숫자', '1자리 · 2자리', '메인', OK, ''),
    ]),
    ('칸 · 카드', '화면 안에 놓이는 상자', [
        ('타이머 칸', '메인용 큰 것 · 위 줄용 작은 것', '전체', OK, ''),
        ('목표 창', '비어 있음 · 1부 · 2부 · 완료 체크', '메인 · 목표 완료', OK, ''),
        ('장소 · 할 일 줄', '핀 + 방 이름 · 할 일 1~2줄', '1부 메인', OK, '할 일 문구 미정'),
        ('우주선 지도', '바닥 윤곽 하나 · 구역 이름 5개 · 갈 구역만 인물 색 (벽 · 문 없음)', '지도 팝업', OK, '노션 공통 기준의 기존 배치 그림 기준'),
        ('완료 목표 줄', '끝냄(체크) · 현재(보라)', '완료 목표 다시 보기', OK, ''),
        ('비아 말 칸', '지금 말 · 지난 말(흐림) · 이름표 ? / 비아', '2부 메인 · 비아 등장 · 문제 16', OK, ''),
        ('코드 입력 칸', '빈 칸 · 입력됨(글자 그대로) · 오류(빨강)', '코드 입력', OK, ''),
        ('힌트 카드', '1부 · 2부 × 1~3줄 높이', '힌트', OK, ''),
        ('정답 칸', '시스템 회색', '힌트', OK, ''),
        ('단계 점', '6칸 · 지나감 / 아직', '문제 16', OK, ''),
        ('화자 이름표', '인물 색 점 + 이름', '문제 16', OK, ''),
        ('스토리카드 틀', '릴리 보라 · 에바 파랑 · 서명 없음', '스토리카드', TODO, '릴리 · 에바만 시안'),
        ('패턴 점 · 선', '점 기본 · 지남 · 선 · 오답(빨강)', '보너스 패턴', WAIT, '점 배치'),
    ]),
    ('버튼', '색은 위쪽 버튼 색 규칙을 따름', [
        ('메인 힌트 버튼', '기본 · 눌림', '메인', OK, ''),
        ('힌트 보기 · 진행도', '기본 · 켜짐 × 1부 · 2부', '코드 입력 · 힌트', OK, ''),
        ('진행도 % 버튼', '막대 포함 × 1부 · 2부', '코드 입력 · 힌트', OK, ''),
        ('다음 힌트', '1부 · 2부', '힌트', OK, ''),
        ('정답 보기', '버튼 → 정답 칸', '힌트', OK, ''),
        ('운영자 버튼', '말풍선 원 · 숫자 붙음', '메인', OK, ''),
    ]),
    ('아이콘', '', [
        ('방패', '', '안전 모드 감지 · 로딩', OK, '무늬 없음'),
        ('장소 핀', '', '목표 창', OK, ''),
        ('목록', '', '목표 창 → 완료 목표', OK, ''),
        ('꺾쇠', '', '목표 창 방 이름 옆 (누르면 지도)', OK, ''),
        ('닫기', '', '지도 팝업', OK, ''),
        ('체크', '', '목표 완료', OK, ''),
        ('채팅 아이콘', '말풍선', '운영자 버튼 · 채팅 위 줄', OK, ''),
        ('뒤로', '', '채팅', OK, ''),
        ('보내기', '', '채팅 입력', OK, ''),
        ('와이파이 끊김', '', '연결 끊김', OK, ''),
        ('연결 끊김 문구', '연결이 끊겼습니다', '연결 끊김', OK, ''),
        ('송출', '', '행성 엔딩', OK, ''),
        ('음표', '', '행성 엔딩', OK, ''),
        ('앱 아이콘', '행성탈출 로고 · 1024 / 512 / 192 / 144 PNG + SVG', '폰 바탕 화면', OK, ''),
        ('심장', '', '문제 16 · 6단계 뒤', OK, ''),
        ('음성 재생 중', '', '비아가 말할 때 (파형과 따로 쓸 경우)', TODO, ''),
    ]),
]

MOTIONS = [
    ('안전 모드 감지', '방패가 커지며 나타남 + 아래 로딩 막대 → 메인으로 스르륵', '길이 · 자동 넘김'),
    ('목표 완료', '체크 → 다음 목표', '길이'),
    ('지도 팝업 열림', '화면 어두워짐 + 지도 떠오름', '길이'),
    ('비아 끼어들기', '보라 화면 지직거림 → 주황 덮기', '길이 · 진동 여부'),
    ('심장 박동', '6단계 뒤 계속 뜀', '심장 소리에 맞출지'),
    ('음성 파형', '비아가 말하는 동안', '실제 음성에 맞출지, 반복 움직임일지'),
    ('이름 바뀜', '? → 비아', '바뀌는 시점(대사 1002)'),
    ('진행도 차오름', '진행도 버튼 자리', ''),
    ('다음 힌트 펼침', '힌트 카드 추가', ''),
    ('패턴 선 그리기', '보너스 패턴', ''),
    ('패턴 오답', '빨간 선 → 지워짐', '길이'),
    ('안 읽음 숫자 등장', '채팅 아이콘', '진동 · 소리 여부'),
    ('탈출 엔딩 끊김', '글자 지직거림 → 검은 화면', '길이'),
]



ASK = [
    ('2부 목표 문구', '기획', '2부 메인 · 목표 완료 화면'),
    ('1부 목표별 할 일 문구', '기획', '목표 창 할 일 줄'),
    ('운영자 안내 문구', '기획', '채팅 첫 화면'),
    ('힌트 코드 · 스토리 코드 형식', '기획', '입력 칸 길이 · 글자 종류'),
    ('진행도 % 기준', '기획', '코드마다 바뀌는지'),
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
out.append(sec('받아야 할 것', '디자인 전에 다른 담당에게 요청',
               table(['항목', '누구에게', '왜'], [[('', a), ('', f'<span class="who">{b}</span>'), (' class="scr"', c)] for a, b, c in ASK])))

assert len(SCREENS) == 22 and all(len(r) == 5 for r in all_assets)
html = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<title>힌트폰 에셋 목록</title>\n</head>\n<body>\n<main>\n'
        + ''.join(out) + '</main>\n</body>\n</html>\n')
pathlib.Path(sys.argv[1]).write_text(html, encoding='utf-8')
print('assets', tally)
