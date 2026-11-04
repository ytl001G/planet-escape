import pathlib, sys, re
# 에셋 목록(힌트폰_에셋목록.html)의 본문을 논리도 페이지 맨 아래 전체 폭 구역으로 붙인다
page = pathlib.Path(sys.argv[1]); src = pathlib.Path(sys.argv[2])
s = page.read_text(encoding='utf-8'); a = src.read_text(encoding='utf-8')
body = a[a.index('<main>') + 6:a.index('</main>')]
body = body.replace('<header>\n  <h1>힌트폰 에셋 목록</h1>', '<header>\n  <h2 class="big">에셋 목록</h2>')
css = '''
#assets { display: grid; gap: 32px; border-top: 1px solid var(--line); padding-top: 36px;
  --ok: #2e7d32; --ok-soft: #e3f1e4; --todo: #b26a00; --todo-soft: #fdf0dc; --wait: #5c6bc0; --wait-soft: #e8eaf8; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) #assets {
  --ok: #81c784; --ok-soft: #1f3121; --todo: #ffb74d; --todo-soft: #3a2c16; --wait: #9fa8da; --wait-soft: #252a45; } }
:root[data-theme="dark"] #assets { --ok: #81c784; --ok-soft: #1f3121; --todo: #ffb74d; --todo-soft: #3a2c16; --wait: #9fa8da; --wait-soft: #252a45; }
#assets h2.big { font-size: 26px; margin: 0; }
#assets h2 { display: flex; gap: 10px; align-items: baseline; }
#assets h2 small { font: 500 13px var(--body); color: var(--muted); }
#assets .legend { display: flex; flex-wrap: wrap; gap: 8px 16px; font-size: 13px; color: var(--muted); margin-top: 10px; }
#assets .tally { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
#assets .tally div { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; }
#assets .tally b { display: block; font: 700 26px var(--display); font-variant-numeric: tabular-nums; }
#assets .tally span { font-size: 13px; color: var(--muted); }
#assets td:first-child { font-weight: 700; white-space: nowrap; }
#assets td.scr { color: var(--muted); font-size: 13px; }
#assets .chip { display: inline-block; font-size: 12px; font-weight: 700; padding: 1px 8px; border-radius: 99px; white-space: nowrap; }
#assets .ok { background: var(--ok-soft); color: var(--ok); }
#assets .todo { background: var(--todo-soft); color: var(--todo); }
#assets .wait { background: var(--wait-soft); color: var(--wait); }
#assets .who { display: inline-block; font-size: 12px; padding: 1px 8px; border-radius: 99px; border: 1px solid var(--line); color: var(--muted); white-space: nowrap; }
#assets .agrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 12px; }
#assets .acard { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px; display: grid; gap: 4px; align-content: start; }
#assets .acard .thumb { width: 100%; height: auto; aspect-ratio: 16 / 9; background: var(--paper); border-radius: 8px; margin-bottom: 6px; color: var(--ink); }
#assets .acard b { font-size: 15px; }
#assets .acard .sub { font-size: 13px; }
#assets .acard .use { font-size: 12px; color: var(--muted); }
#assets .acard .st { margin-top: 4px; font-size: 12px; color: var(--muted); }
#assets .acard .ask { font-size: 12px; color: var(--muted); }
#assets .bgprev { display: block; width: 100%; max-width: 980px; height: auto; border-radius: 12px; border: 1px solid var(--line); margin-bottom: 12px; }
#assets .who.me { border-color: var(--lily); color: var(--lily); }
'''
assert s.count('</style>') == 1 and s.count('</main>') == 1 and 'id="assets"' not in s
s = s.replace('</style>', css + '</style>')
s = s.replace('</main>', '<section id="assets">' + body + '</section>\n</main>')
page.write_text(s, encoding='utf-8'); print('assets inserted')
