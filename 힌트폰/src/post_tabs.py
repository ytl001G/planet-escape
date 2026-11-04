# 위쪽 탭: 시험해 보기 / 화면 제안 / 순서도 / 에셋 목록 — 한 번에 한 묶음만 보인다
import pathlib, sys, re
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
m = re.search(r'<nav class="toc" aria-label="목차">.*?</nav>\n?', s); assert m
subs = re.findall(r'<a href="#(g-[a-z]+)">([^<]+)</a>', m.group(0)); assert len(subs) == 4, subs
s = s.replace(m.group(0), '')
TABS = [('proto', '시험해 보기'), ('screens', '화면 제안'), ('flow', '순서도'), ('assets', '에셋 목록'), ('rules', '공통 규정')]
nav = ('<nav class="tabs" role="tablist" aria-label="보기 바꾸기">'
       + ''.join(f'<button type="button" role="tab" id="tab-{k}" aria-controls="{k}" aria-selected="false" data-tab="{k}">{l}</button>' for k, l in TABS)
       + '</nav>\n')
assert s.count('</header>') >= 1
s = s.replace('</header>', '</header>\n' + nav, 1)
sub = '<nav class="toc" aria-label="화면 제안 묶음">' + ''.join(f'<a href="#{k}">{l}</a>' for k, l in subs) + '</nav>\n'
o = '<div class="col" id="screens">'; assert s.count(o) == 1
s = s.replace(o, o + '\n' + sub)
CSS = '''
.tabs { position: sticky; top: 0; z-index: 20; display: flex; gap: 6px; flex-wrap: wrap; padding: 10px 0; margin: 6px 0 18px; background: var(--paper); border-bottom: 1px solid var(--line); }
.tabs button { font: 700 15px var(--body); color: var(--muted); background: none; border: 1px solid transparent; border-radius: 10px; padding: 8px 16px; cursor: pointer; }
.tabs button:hover, .tabs button:focus-visible { color: var(--ink); border-color: var(--line); }
.tabs button[aria-selected="true"] { color: var(--lily); background: var(--lily-soft); border-color: var(--lily); }
.tab-off { display: none !important; }
.split.one { grid-template-columns: minmax(0, 1fr) !important; }
.split.one .flowcol { position: static !important; max-height: none !important; overflow: visible !important; }
#screens > .toc { margin: 0 0 4px; }
[id^="g-"], #screens section { scroll-margin-top: 70px; }
'''
s = s.replace('</style>', CSS + '</style>', 1)
JS = '''<script>
(() => {
  const ids = ['proto', 'screens', 'flow', 'assets', 'rules'], split = document.querySelector('.split');
  const btn = k => document.getElementById('tab-' + k);
  function show(k, push) {
    ids.forEach(id => { document.getElementById(id).classList.toggle('tab-off', id !== k); btn(id).setAttribute('aria-selected', String(id === k)); btn(id).tabIndex = id === k ? 0 : -1; });
    split.classList.toggle('tab-off', k !== 'screens' && k !== 'flow'); split.classList.add('one');
    if (push) history.replaceState(null, '', '#' + k);
    dispatchEvent(new Event('resize'));  // 시제품 폰 크기 다시 맞추기
  }
  document.querySelector('.tabs').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) { show(b.dataset.tab, true); scrollTo(0, 0); } });
  document.querySelector('.tabs').addEventListener('keydown', e => {
    const i = ids.findIndex(id => btn(id).getAttribute('aria-selected') === 'true'), d = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
    if (d) { const k = ids[(i + d + ids.length) % ids.length]; show(k, true); btn(k).focus(); }
  });
  const h = location.hash.slice(1);
  show(ids.includes(h) ? h : h.startsWith('g-') ? 'screens' : 'proto', false);
  // 주소의 #으로 브라우저가 먼저 스크롤해 버리므로, 다 읽힌 뒤 위치를 다시 맞춘다
  addEventListener('load', () => setTimeout(() => { if (h.startsWith('g-')) document.getElementById(h)?.scrollIntoView(); else scrollTo(0, 0); }));
  document.getElementById('screens').addEventListener('click', e => { const a = e.target.closest('a[href^="#g-"]'); if (a) { e.preventDefault(); document.getElementById(a.getAttribute('href').slice(1)).scrollIntoView({ behavior: 'smooth' }); } });
})();
</script>
'''
s = s.replace('</body>', JS + '</body>', 1)
p.write_text(s, encoding='utf-8'); print('tabs ok')
