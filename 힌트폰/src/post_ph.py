# 정해지지 않은 문구 자리(회색 막대 rect.ph)를 '예시 문구' 글자로 바꾼다. 붙어 있는 여러 줄 막대는 한 줄로 합친다.
import pathlib, sys, re
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
LABEL = '예시 문구'
RECT = re.compile(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="[\d.]+" class="ph"/>')
num = lambda v: float(v)

out, i, groups = [], 0, 0
ms = list(RECT.finditer(s))
k = 0
while k < len(ms):
    g = [ms[k]]
    while k + 1 < len(ms) and s[g[-1].end():ms[k + 1].start()].strip() == '':
        a, b = g[-1], ms[k + 1]
        ax, ay, aw = num(a[1]), num(a[2]), num(a[3]); bx, by, bw = num(b[1]), num(b[2]), num(b[3])
        same_left = abs(ax - bx) < 1; same_mid = abs((ax + aw / 2) - (bx + bw / 2)) < 1
        if 0 < by - ay <= 20 and (same_left or same_mid): g.append(b); k += 1
        else: break
    x, y, w, h = (num(v) for v in g[0].groups())
    mid = len(g) > 1 and abs(num(g[0][1]) - num(g[1][1])) >= 1     # 가운데 정렬된 막대 묶음
    fs = {6: 10, 7: 11, 8: 12}.get(round(h), 11)
    tx, anchor = (x + w / 2, 'middle') if mid else (x, 'start')
    out.append(s[i:g[0].start()])
    out.append(f'<text x="{tx:g}" y="{y + h / 2 + fs * 0.36:.1f}" font-size="{fs}" text-anchor="{anchor}" class="t-mute">{LABEL}</text>')
    i = g[-1].end(); k += 1; groups += 1
out.append(s[i:]); s = ''.join(out)
left = len(re.findall(r'class="ph"', s))
assert left == 0, f'못 바꾼 막대 {left}개'
s = s.replace('회색 막대는 아직 정해지지 않은 문구 자리', "'예시 문구'는 아직 정해지지 않은 문구 자리").replace('회색 막대', "'예시 문구'")
p.write_text(s, encoding='utf-8'); print('placeholders ->', groups)
