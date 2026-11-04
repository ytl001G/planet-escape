SP="$(dirname "$0")"; cd "$SP"
python -X utf8 - <<'PY'
import pathlib
h = pathlib.Path(r'C:/Users/USER/OneDrive/바탕 화면/projects/학교/대학(KAIST)/Puple/행성탈출/힌트폰/힌트폰_논리도.html').read_text(encoding='utf-8')
t = pathlib.Path('proto_test.js').read_text(encoding='utf-8').replace("press('스토리카드 1 띄우기'); log(has('보안이 아니잖아?'), '스토리카드 1 문구');", "log(!ctl('스토리카드 1 띄우기'), '스토리카드 1 버튼 없음');")
for n, js in [('t_proto', t), ('t_pause', pathlib.Path('pause_test.js').read_text(encoding='utf-8')), ('t_map', pathlib.Path('map_test.js').read_text(encoding='utf-8'))]:
    pathlib.Path(n + '.html').write_text(h.replace('</body>', '<script>' + js + '</script></body>'), encoding='utf-8')
PY
C="/c/Program Files/Google/Chrome/Application/chrome.exe"; i=$(( (RANDOM % 9000) + 1000 ))
for f in t_proto t_pause t_map; do i=$((i+1)); "$C" --headless=new --disable-gpu --user-data-dir="$(cygpath -w "$SP/cprof$i")" --virtual-time-budget=75000 --dump-dom "file:///$(cygpath -m "$SP")/$f.html" 2>/dev/null | python -X utf8 -c "import sys,re;d=sys.stdin.read();m=re.search(r'<pre id=\"testout\">(.*?)</pre>',d,re.S);t=m.group(1) if m else 'NO OUTPUT';print('\n'.join(l for l in t.split('\n') if not l.startswith('PASS')));print('$f',t.count('PASS'),'pass',t.count('FAIL'),'fail')"; done
