# '공통 규정' 탭: 색 · 글자 · 크기 · 버튼 색 · 문구 규칙을 한곳에
import pathlib, sys, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import CHAR, GUIDE, contrast
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
btn = p.with_name('rules_btn.html').read_text(encoding='utf-8')
btn = re.sub(r'<h2>.*?</h2>', '<h2>버튼 색</h2>', btn, count=1)

def sw(c): return f'<span class="sw" style="background:{c}"></span>'
def tbl(head, rows):
    return ('<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td{" class=scr" if i == len(r) - 1 and len(r) > 2 else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
            + '</tbody></table></div>')
def sec(t, small, inner): return f'<section>\n  <h2>{t} <small>{small}</small></h2>\n  {inner}\n</section>\n'

who = [(n, f'{sw(b)} {b}', f'{sw(t)} <b style="color:{t}">{n}</b> {t}', f'{contrast(t, "#17151b"):.1f} : 1', '') for n, b, t in CHAR]
who = [r[:4] + ('칠 · 점 · 이름표 점' if n != '비아' else '2부 말풍선 · 화자 점',) for r, (n, _, _) in zip(who, CHAR)]
colors = sec('인물 색', '대표색은 칠과 점, 글자색은 어두운 바탕 위 이름 글자',
             tbl(['인물', '대표색 (노션 기준)', '글자색 (밝게)', '바탕 대비', '쓰는 곳'], who)
             + '<p class="note">이름 글자는 대표색 그대로 쓰지 않고 같은 계열의 밝은 색을 쓴다. 대비 4.5 : 1 이상이어야 읽힌다.</p>')

page = [('폰 바탕', f'{sw("#000000")} 검정 + 별 배경', '배경 이미지 위에 카드를 얹는다'),
        ('카드 · 버튼 면', f'{sw("#18151e")} 반투명 어두움 (62%)', '테두리 1.5 px 흰색 12 ~ 20%'),
        ('기본 글자', f'{sw("#f2eef6")} #f2eef6', '흐린 글자는 같은 색 55 ~ 60%'),
        ('1부 강조', f'{sw("#cf86e6")} #cf86e6 (릴리 보라)', '현재 목표 · 다음 힌트 · 진행 막대'),
        ('2부 강조', f'{sw("#ffae4d")} #ffae4d (비아 주황)', '2부 힌트 · 단계 점'),
        ('경고 · 빨강', f'{sw("#E5484D")} #E5484D', '안 읽은 숫자 · 시간 종료 · 패턴 오답'),
        ('시스템 회색', f'{sw("#616161")} #616161', '정답 보기 · 안내')]
screen = sec('화면 색', '폰 화면 기준 · 라이트 / 다크 모드와 상관없이 항상 같다', tbl(['항목', '색', '쓰는 곳'], page))

fonts = [('타이머 숫자', '700 · 36 px', '시안 108 px'), ('현재 목표 · 큰 제목', '700 · 19 px', ''), ('정답 숫자', '700 · 22 px', ''),
         ('위 줄 제목', '700 · 16 px', ''), ('버튼 · 입력 글자', '700 · 15 px', ''), ('본문 · 말풍선', '400 · 15 px', ''),
         ('힌트 코드 입력', '700 · 20 px · 고정폭', 'IBM Plex Mono'), ('작은 글자 · 할 일', '400 · 13 px', ''), ('이름표 · 숫자 배지', '700 · 11 ~ 12 px', '')]
font = sec('글자', '제목 IBM Plex Sans KR · 본문 Noto Sans KR · 코드 IBM Plex Mono', tbl(['쓰는 곳', '굵기 · 크기', '메모'], fonts))
size = sec('크기 · 간격', '갤럭시 A13 기준 · 시안 크기 → 실제 px', tbl(['항목', '크기', '메모'], [list(g) for g in GUIDE]))

text = [('문구', '기획 문서나 시나리오에 있는 글만 쓴다. 정해지지 않은 문구는 \'예시 문구\' 또는 회색 막대로 둔다.'),
        ('1부 · 2부 표시', '폰 화면에는 1부 · 2부 글자를 쓰지 않는다. 구분은 색(보라 · 주황)으로만 한다.'),
        ('힌트 코드', '입력한 코드는 가린 글자 없이 그대로 보인다.'),
        ('도식 설명', '그림 아래에 설명 글을 달지 않는다.'),
        ('화면 모드', '논리도와 폰 화면 모두 항상 어두운 색 하나만 쓴다.')]
rules = sec('문구 · 표시 규칙', '', tbl(['항목', '규칙'], [list(t) for t in text]))

css = '''
#rules { display: grid; gap: 32px; }
#rules h2 { display: flex; gap: 10px; align-items: baseline; margin: 0 0 10px; }
#rules h2 small { font: 500 13px var(--body); color: var(--muted); }
#rules td:first-child { font-weight: 700; white-space: nowrap; }
#rules td.scr { color: var(--muted); font-size: 13px; }
#rules .sw { display: inline-block; width: 14px; height: 14px; border-radius: 4px; vertical-align: -2px; margin-right: 4px; border: 1px solid var(--line); }
#rules .note { margin: 8px 0 0; color: var(--muted); font-size: 13px; }
'''
opts = pathlib.Path(__file__).with_name('rules_opts.html').read_text(encoding='utf-8')  # 시안: 고르면 지움
html = '<section id="rules">\n<h1 class="big" style="font-size:26px;margin:0">공통 규정</h1>\n' + opts + colors + screen + font + size + btn + rules + '</section>\n'
o = '<section id="assets">'; assert s.count(o) == 1
s = s.replace(o, html + o).replace('</style>', css + '</style>', 1)
p.write_text(s, encoding='utf-8'); print('rules tab ok')
