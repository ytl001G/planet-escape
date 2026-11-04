# 편집 패널: 문구 · 색 · 글자 크기를 시험판에서 바로 바꿈 (브라우저에 저장, 내보내기로 원본에 반영)
# + 시험판 색을 CSS 변수로 (--c1 1부, --c2 2부, --err 오류, --c0 안전 모드 전 링, 인물 색) + 채팅 위 줄 제목을 글자로
import pathlib, re
p = pathlib.Path('proto.py'); c = p.read_text(encoding='utf-8')
def rp(o, n, cnt=1):
    global c; assert c.count(o) == cnt, (o[:70], c.count(o)); c = c.replace(o, n)

# ── 1. 색 → 변수 (CSS 부분과 JS 부분) ──
a = c.index("CSS = r'''"); b = c.index("'''", a + 10)
j = c.index("JS = r'''"); k = c.index("'''", j + 10)
def mix(v, amt, to): return f'color-mix(in srgb, var({v}), {to} {amt}%)'
def alpha(base, a): return f'color-mix(in srgb, {base} {float(a)*100:g}%, transparent)'
FAM = {'#cf86e6': 'var(--c1)', '#d99cf0': mix('--c1', 15, 'white'), '#a24bc4': mix('--c1', 25, 'black'), '#5a1f78': mix('--c1', 60, 'black'),
       '#ffae4d': 'var(--c2)', '#ffb460': mix('--c2', 8, 'white'), '#ffa53d': 'var(--c2)', '#a85a00': mix('--c2', 40, 'black'),
       '#e5484d': 'var(--err)', '#e9e6ee': 'var(--c0)'}
RGBA = {(207, 134, 230): 'var(--c1)', (142, 36, 170): mix('--c1', 35, 'black'), (60, 18, 76): mix('--c1', 72, 'black'),
        (255, 174, 77): 'var(--c2)', (196, 106, 0): mix('--c2', 30, 'black')}
def recolor(t, js=False):
    t = re.sub(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', lambda m: alpha(RGBA[tuple(map(int, m.groups()[:3]))], m[4]) if tuple(map(int, m.groups()[:3])) in RGBA else m[0], t)
    return re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: FAM.get(m[0].lower(), m[0]), t)
css = recolor(c[a:b])
css = css.replace("CSS = r'''", "CSS = r'''\n#proto { --c1: #cf86e6; --c2: #ffae4d; --err: #e5484d; --c0: #e9e6ee; }  /* 편집 패널에서 바꾸는 색 */\n", 1)
js = c[j:k]
# SVG 속성(fill="#..")은 변수를 못 읽으니 style로
js = re.sub(r'(fill|stroke)="(#cf86e6|#ffae4d)"', lambda m: f'style="{m[1]}:{FAM[m[2]]}"', js)
js = js.replace('stroke="${col}"', 'style="stroke:${col}"').replace("fill=\"${path.includes(i) ? col : 'rgba(255,255,255,.22)'}\"", "style=\"fill:${path.includes(i) ? col : 'rgba(255,255,255,.22)'}\"")
CH = [('알렉스', 'alex', '#E53935', '#E57373'), ('오펠리아', 'ophelia', '#FDD835', '#FFF176'), ('노아', 'noah', '#43A047', '#81C784'), ('에바', 'eva', '#1E88E5', '#64B5F6'), ('릴리', 'lily', '#8E24AA', '#BA68C8')]
for nm, en, m1, m2 in CH:
    js = js.replace(f"{nm}: '{m1}'", f"{nm}: 'var(--ch-{en})'", 1).replace(f"{nm}: '{m2}'", f"{nm}: 'var(--cht-{en})'", 1)
js = js.replace("비아: '#FB8C00'", "비아: 'var(--ch-bia)'")
js = recolor(js)
css = css.replace("#proto { --c1:", "#proto { " + ' '.join(f'--ch-{en}: {m1}; --cht-{en}: {m2};' for _, en, m1, m2 in CH) + " --ch-bia: #FB8C00; --c1:", 1)
c = c[:a] + css + c[b:j] + js + c[k:]
left = re.findall(r'#(?:cf86e6|ffae4d|e5484d)\b', c[c.index("JS = r'''"):c.index("'''", c.index("JS = r'''") + 10)], re.I)
assert not left, left

# ── 2. 채팅 위 줄: 아이콘 대신 '채팅' 글자 (힌트코드 앱과 같게) ──
c, n = re.subn(r'<div class="ttl" style="display:grid;place-items:center">\$\{ICON\.head\}</div>', '<div class="ttl">채팅</div>', c); assert n == 1

# ── 3. 편집 패널 ──
rp("""      <span>그 밖의 코드는 오류로 처리돼요. 코드와 패턴 정답은 시험용이에요.</span>
    </div>""", """      <span>그 밖의 코드는 오류로 처리돼요. 코드와 패턴 정답은 시험용이에요.</span>
    </div>
    <details class="ed" id="pv-ed"><summary>편집 패널 · 문구 · 색 · 글자 크기</summary>
      <p class="state">바꾸면 폰에 바로 보여요. 이 브라우저에 저장되고, 원본에 넣으려면 ‘내보내기’로 복사해서 전해 주세요.</p>
      <div class="ed-tabs" role="tablist"><button type="button" data-ed="text" aria-selected="true">문구</button><button type="button" data-ed="color" aria-selected="false">색</button><button type="button" data-ed="size" aria-selected="false">글자 크기</button></div>
      <div class="ed-pane" data-pane="text"><input type="search" id="pv-ed-q" placeholder="문구 찾기" aria-label="문구 찾기"><p class="state">폰 화면에 한 번 나온 문구가 여기 쌓여요. 진행을 바꿔 가며 화면을 띄워 보세요.</p><div id="pv-ed-text" class="ed-list"></div></div>
      <div class="ed-pane" data-pane="color" hidden><div id="pv-ed-color" class="ed-list"></div></div>
      <div class="ed-pane" data-pane="size" hidden><div id="pv-ed-size" class="ed-list"></div></div>
      <div class="grp"><button type="button" id="pv-ed-out">내보내기 (복사)</button><button type="button" id="pv-ed-reset">모두 되돌리기</button></div>
      <textarea id="pv-ed-io" rows="3" placeholder="내보낸 내용을 여기 붙여 넣고 ‘불러오기’" aria-label="편집 내용 붙여 넣기"></textarea>
      <div class="grp"><button type="button" id="pv-ed-in">불러오기</button><span class="state" id="pv-ed-msg" role="status"></span></div>
    </details>""")
rp("#proto .panel .state { font-size: 13px; color: var(--muted); }", """#proto .panel .state { font-size: 13px; color: var(--muted); }
#proto .ed { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; display: grid; gap: 10px; }
#proto .ed summary { font: 700 15px var(--display); cursor: pointer; }
#proto .ed[open] { gap: 10px; } #proto .ed[open] > * + * { margin-top: 10px; }
#proto .ed-tabs { display: flex; gap: 6px; } #proto .ed-tabs button[aria-selected="true"] { border-color: var(--lily); color: var(--lily); }
#proto .ed-list { display: grid; gap: 8px; max-height: 420px; overflow: auto; padding-right: 4px; }
#proto .ed-row { display: grid; gap: 3px; } #proto .ed-row small { font-size: 11px; color: var(--muted); }
#proto .ed-row.on small::after { content: ' · 바꿈'; color: var(--lily); }
#proto .ed-row input[type=text], #proto .ed input[type=search], #proto .ed textarea { width: 100%; box-sizing: border-box; font: 400 14px var(--body); color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 7px 9px; }
#proto .ed-row.inl { grid-template-columns: 1fr auto; align-items: center; } #proto .ed-row input[type=color] { width: 48px; height: 30px; border: 0; background: none; padding: 0; }
#proto .ed-row input[type=number] { width: 72px; font: 400 14px var(--body); color: var(--ink); background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 6px 8px; }""")

ED_JS = r"""
// ── 편집 패널: 문구 · 색 · 글자 크기 (이 브라우저에 저장) ──
const ED_KEY = 'hintphone-edit-v1';
let ED = { text: {}, color: {}, size: {} };
try { Object.assign(ED, JSON.parse(localStorage.getItem(ED_KEY) || '{}')); } catch (e) {}
const edSave = () => { try { localStorage.setItem(ED_KEY, JSON.stringify(ED)); } catch (e) {} };
const SEEN = [];  // 폰에 나온 원래 문구 (처음 나온 순서)
const COLORS = [['--c1', '1부 색 (릴리 안내)', '#cf86e6'], ['--c2', '2부 색 (비아 안내)', '#ffae4d'], ['--err', '오류 · 시간 종료 빨강', '#e5484d'], ['--c0', '안전 모드 전 링', '#e9e6ee'],
  ['--ch-alex', '알렉스 (지도 구역)', '#E53935'], ['--ch-ophelia', '오펠리아 (지도 구역)', '#FDD835'], ['--ch-noah', '노아 (지도 구역)', '#43A047'], ['--ch-eva', '에바 (지도 구역)', '#1E88E5'], ['--ch-lily', '릴리 (지도 구역)', '#8E24AA'], ['--ch-bia', '비아 (말하는 사람 점)', '#FB8C00'],
  ['--cht-alex', '알렉스 이름 글자', '#E57373'], ['--cht-ophelia', '오펠리아 이름 글자', '#FFF176'], ['--cht-noah', '노아 이름 글자', '#81C784'], ['--cht-eva', '에바 이름 글자', '#64B5F6'], ['--cht-lily', '릴리 이름 글자', '#BA68C8']];
const SIZES = [['#proto .idle .timer', '안전 모드 전 링 숫자', 50], ['#proto .timer', '링 타이머 숫자', 30], ['#proto .goal', '목표 제목', 19], ['#proto .room', '목표 방 이름', 14], ['#proto .lbl', '‘현재 목표’ 같은 작은 제목', 12],
  ['#proto .btn', '버튼 글자', 15], ['#proto .head .ttl', '위 줄 제목', 16], ['#proto .input', '코드 입력 칸', 20], ['#proto .card', '힌트 카드 글', 14], ['#proto .bia .say', '비아 대사', 14], ['#proto .msg', '채팅 말풍선', 14],
  ['#proto .app', '독 앱 이름', 11], ['#proto .key', '키보드 글자', 16], ['#proto .offmsg', '연결 끊김 문구', 17], ['#proto .toast b', '알림 배너 제목', 13]];
const edCss = document.createElement('style'); document.head.append(edCss);
function edApplyStyle() {
  const root = document.getElementById('proto');
  COLORS.forEach(([v]) => ED.color[v] ? root.style.setProperty(v, ED.color[v]) : root.style.removeProperty(v));
  edCss.textContent = SIZES.filter(([sel]) => ED.size[sel]).map(([sel]) => `${sel} { font-size: ${+ED.size[sel]}px !important; }`).join('\n');
}
function edText() {  // 화면 글자를 바꾼 문구로 갈아 끼우고, 새로 나온 문구는 목록에 쌓음
  const w = document.createTreeWalker(scr, NodeFilter.SHOW_TEXT); let n, grew = false;
  while ((n = w.nextNode())) {
    const el = n.parentElement; if (!el || el.closest('.kbd, [data-time], [data-tm], .ed')) continue;
    const raw = n.nodeValue, t = raw.trim(); if (!t || /^[\d\s:%.,·\-−+→]+$/.test(t)) continue;
    const orig = n.__orig || t; n.__orig = orig;
    if (!SEEN.includes(orig)) { SEEN.push(orig); grew = true; }
    if (ED.text[orig] != null) n.nodeValue = raw.replace(t, ED.text[orig]);
  }
  if (grew && $('pv-ed').open) edList();
}
function edList() {
  const q = ($('pv-ed-q').value || '').trim(), box = $('pv-ed-text');
  const rows = SEEN.filter(t => !q || t.includes(q) || (ED.text[t] || '').includes(q));
  box.innerHTML = rows.length ? '' : '<p class="state">아직 없음</p>';
  rows.forEach(t => {
    const r = document.createElement('label'); r.className = 'ed-row' + (ED.text[t] != null ? ' on' : '');
    r.innerHTML = '<small></small><input type="text">'; r.querySelector('small').textContent = t;
    const i = r.querySelector('input'); i.value = ED.text[t] ?? t;
    i.oninput = () => { if (i.value === t) delete ED.text[t]; else ED.text[t] = i.value; r.classList.toggle('on', ED.text[t] != null); edSave(); render(); };
    box.append(r);
  });
}
function edBuild() {
  $('pv-ed-color').innerHTML = ''; $('pv-ed-size').innerHTML = '';
  COLORS.forEach(([v, l, d]) => {
    const r = document.createElement('label'); r.className = 'ed-row inl' + (ED.color[v] ? ' on' : ''); r.innerHTML = '<small></small><input type="color">';
    r.querySelector('small').textContent = l; const i = r.querySelector('input'); i.value = ED.color[v] || d;
    i.oninput = () => { if (i.value.toLowerCase() === d.toLowerCase()) delete ED.color[v]; else ED.color[v] = i.value; r.classList.toggle('on', !!ED.color[v]); edSave(); edApplyStyle(); };
    $('pv-ed-color').append(r);
  });
  SIZES.forEach(([sel, l, d]) => {
    const r = document.createElement('label'); r.className = 'ed-row inl' + (ED.size[sel] ? ' on' : ''); r.innerHTML = '<small></small><input type="number" min="6" max="120" step="1">';
    r.querySelector('small').textContent = l + ' (기본 ' + d + ')'; const i = r.querySelector('input'); i.value = ED.size[sel] || d;
    i.oninput = () => { const v = +i.value; if (!v || v === d) delete ED.size[sel]; else ED.size[sel] = v; r.classList.toggle('on', !!ED.size[sel]); edSave(); edApplyStyle(); };
    $('pv-ed-size').append(r);
  });
  edList();
}
document.querySelectorAll('#pv-ed [data-ed]').forEach(b => b.onclick = () => {
  document.querySelectorAll('#pv-ed [data-ed]').forEach(x => x.setAttribute('aria-selected', String(x === b)));
  document.querySelectorAll('#pv-ed [data-pane]').forEach(p => p.hidden = p.dataset.pane !== b.dataset.ed);
});
$('pv-ed').addEventListener('toggle', () => { if ($('pv-ed').open) edBuild(); });
$('pv-ed-q').oninput = edList;
const edMsg = t => { $('pv-ed-msg').textContent = t; };
$('pv-ed-out').onclick = () => {
  const s = JSON.stringify(ED, null, 1); $('pv-ed-io').value = s; $('pv-ed-io').select();
  (navigator.clipboard ? navigator.clipboard.writeText(s) : Promise.reject()).then(() => edMsg('복사했어요'), () => { try { document.execCommand('copy'); edMsg('복사했어요'); } catch (e) { edMsg('아래 칸 내용을 직접 복사해 주세요'); } });
};
$('pv-ed-in').onclick = () => {
  try { const v = JSON.parse($('pv-ed-io').value); ED = { text: v.text || {}, color: v.color || {}, size: v.size || {} }; edSave(); edApplyStyle(); edBuild(); render(); edMsg('불러왔어요'); }
  catch (e) { edMsg('내용을 읽을 수 없어요'); }
};
$('pv-ed-reset').onclick = () => { ED = { text: {}, color: {}, size: {} }; edSave(); edApplyStyle(); edBuild(); render(); edMsg('모두 되돌렸어요'); };
edApplyStyle();
"""
rp("\nreset(); setPause(true);", ED_JS + "\nreset(); setPause(true);")
rp("  scr.innerHTML = h; sbar();", "  scr.innerHTML = h; sbar(); edText();")
compile(c, 'proto.py', 'exec'); p.write_text(c, encoding='utf-8'); print('patched proto.py')
