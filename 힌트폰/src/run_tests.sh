SP="$(cd "$(dirname "$0")" && pwd)"; cd "$SP"
python -X utf8 - <<'PY'
import pathlib
h = pathlib.Path(r'C:/Users/USER/OneDrive/바탕 화면/projects/학교/대학(KAIST)/Puple/행성탈출/힌트폰/힌트폰_논리도.html').read_text(encoding='utf-8')
t = pathlib.Path('proto_test.js').read_text(encoding='utf-8').replace("press('스토리카드 1 띄우기'); log(has('보안이 아니잖아?'), '스토리카드 1 문구');", "log(!ctl('스토리카드 1 띄우기'), '스토리카드 1 버튼 없음');")
for n, js in [('t_proto', t), ('t_pause', pathlib.Path('pause_test.js').read_text(encoding='utf-8')), ('t_map', pathlib.Path('map_test.js').read_text(encoding='utf-8'))]:
    pathlib.Path(n + '.html').write_text(h.replace('</body>', '<script>(()=>{const s=document.querySelector("#pv-screen");const i=document.getElementById("pv-in");i.value="0000";i.dispatchEvent(new Event("input"));s.querySelector("[data-act=bhint]").click();window.__demo=!!s.querySelector(".hpop .card");s.querySelector("[data-act=hpx]")?.click();i.value="";i.dispatchEvent(new Event("input"));})();document.querySelector("#pv-screen [data-act=start]").click();' + js + '</script></body>'), encoding='utf-8')  # 시험은 재생부터 누르고 시작
PY
# 크롬 대신 엣지로 시험: 사용자 크롬과 무관. 프로필 폴더는 시험이 끝난 뒤에만 지움
E="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
for f in t_proto t_pause t_map; do
  "$E" --headless=new --disable-gpu --no-first-run --user-data-dir="$(cygpath -w "$SP/eprof_$f")" --virtual-time-budget=75000 --dump-dom "file:///$(cygpath -m "$SP")/$f.html" > "$SP/eout_$f.txt" 2>/dev/null
  python -X utf8 parse_out.py "$SP/eout_$f.txt" $f
done
rm -rf "$SP"/eprof_*
