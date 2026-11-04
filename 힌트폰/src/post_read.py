# 가독성 정리: 화면 제안을 묶음별로 재배치·재번호, 위쪽 목차, 순서도 열 고정
import pathlib, sys, re
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')

L0 = s.index('<p class="coltitle">화면 제안</p>\n') + len('<p class="coltitle">화면 제안</p>\n')
L1 = s.index('</div>\n<div class="col">\n<p class="coltitle">순서도</p>')
left = s[L0:L1]
secs = re.findall(r'<section>\n  <h2>.*?</section>\n', left, re.S)
assert ''.join(secs).strip() == left.strip(), '화면 제안 열에 section 밖 내용이 있음'
by = {}
for sec in secs:
    t = re.search(r'<h2>(.*?)</h2>', sec).group(1)
    by[re.sub(r'^\d+\.\s*', '', t)] = sec
DROP = {'스토리카드가 뜰 때'}  # 스토리카드 1은 오프라인 물체로 정함
for t in DROP: by.pop(t)
assert len(by) == 22, len(by)

GROUPS = [
    ('main', '메인 화면과 진행', ['메인 화면 (안전 모드 이전)', '안전 모드 가동', '메인 화면 (안전 모드 이후)',
                          '목표 창: 장소와 할 일', '지도 팝업', '목표를 끝냈을 때', '완료 목표 다시 보기', '비아가 처음 나오는 순간']),
    ('hint', '힌트', ['코드 입력 화면', '진행도 버튼을 눌렀을 때', '진행도와 힌트를 같이 볼 때', '정답 보기를 누르기 전 · 후',
                    '2부 힌트', '문제 16 힌트 (대기 연출 6단계)']),
    ('etc', '그 밖의 화면', ['보너스 패턴 입력 → 스토리카드 13.5', '보너스 패턴 오답', '운영자 채팅', '연결이 끊겼을 때']),
    ('end', '엔딩', ['탈출 엔딩', '행성 엔딩', '시간 종료']),
]
pathlib.Path(sys.argv[1]).with_name('rules_btn.html').write_text(by.pop('버튼 색 규칙'), encoding='utf-8')  # 공통 규정 탭으로
used = [t for _, _, ts in GROUPS for t in ts]
assert sorted(used) == sorted(by), set(by) ^ set(used)

n = 0; out = ''
for gid, gname, titles in GROUPS:
    out += f'<div class="grp" id="g-{gid}">\n<h2 class="grp-title">{gname}</h2>\n'
    for t in titles:
        sec = by[t]
        if gid != 'rule':
            n += 1; label = f'<span class="num">{n}</span>{t}'
        else:
            label = t
        out += re.sub(r'<h2>.*?</h2>', f'<h3>{label}</h3>', sec, count=1)
    out += '</div>\n'
s = s[:L0] + out + s[L1:]

# 순서도 열: 넓은 화면에서 화면 제안을 내려도 옆에 고정
s = s.replace('<div class="col">\n<p class="coltitle">순서도</p>', '<div class="col flowcol" id="flow">\n<p class="coltitle">순서도</p>', 1)
s = s.replace('<div class="col">\n<p class="coltitle">화면 제안</p>', '<div class="col" id="screens">\n<p class="coltitle">화면 제안</p>', 1)

nav = ('<nav class="toc" aria-label="목차">'
       + ''.join(f'<a href="#g-{gid}">{gname}</a>' for gid, gname, _ in GROUPS)
       + '<a href="#flow">순서도</a><a href="#assets">에셋 목록</a></nav>\n')
assert s.count('<h1>힌트폰 논리도</h1>\n</header>') == 1
s = s.replace('<h1>힌트폰 논리도</h1>\n</header>', '<h1>힌트폰 논리도</h1>\n' + nav + '</header>')

css = '''
/* 가독성 정리 */
html { scroll-behavior: smooth; }
.toc { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.toc a { font-size: 14px; font-weight: 700; color: var(--ink); text-decoration: none; padding: 6px 12px; border: 1px solid var(--line); border-radius: 99px; background: var(--card); }
.toc a:hover, .toc a:focus-visible { border-color: var(--lily); color: var(--lily); }
.grp { display: grid; gap: 28px; scroll-margin-top: 16px; }
.grp + .grp { border-top: 1px solid var(--line); padding-top: 28px; }
.grp-title { font-size: 22px; margin: 0; color: var(--lily); }
#screens h3 { font: 700 17px/1.35 var(--display); margin: 0 0 10px; display: flex; gap: 8px; align-items: center; }
#screens h3 .num { display: inline-grid; place-items: center; min-width: 26px; height: 26px; padding: 0 6px; border-radius: 99px; background: var(--sys-soft); color: var(--muted); font-size: 13px; font-variant-numeric: tabular-nums; }
#screens figure { padding: 24px; }
#screens .col, #screens { gap: 36px; }
#assets { scroll-margin-top: 16px; }
@media (min-width: 1001px) {
  .flowcol { position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow-y: auto; overscroll-behavior: contain; scroll-margin-top: 12px; }
}
'''
assert s.count('</style>') == 1
s = s.replace('</style>', css + '</style>')
p.write_text(s, encoding='utf-8'); print('readability ok', n)
