# 우주선 지도: 노션 '공통 기준'의 기존 방 배치(위 알렉스·릴리·에바, 아래 오펠리아·노아)를 벽·문 없이 한 공간 안 구역으로
# (노션 '공간 분리의 방법': 파티션 대신 소품·조명 색으로 구역을 나눔)
# shortcut: 실측 공간 배치도가 아니라 기존 그림 기준, 실측 배치도가 나오면 좌표만 바꾸기
ROOMS = [  # 구역 이름, x, y, w, h  (전체 284 x 176)
    ('알렉스', 0, 0, 92, 88), ('릴리', 96, 0, 92, 88), ('에바', 192, 0, 92, 88),
    ('오펠리아', 54, 92, 92, 84), ('노아', 150, 92, 92, 84)]
COLOR = {'알렉스': '#E53935', '오펠리아': '#FDD835', '노아': '#43A047', '에바': '#1E88E5', '릴리': '#8E24AA'}
HULL_PTS = [(-6, -6), (290, -6), (290, 94), (248, 94), (248, 182), (48, 182), (48, 94), (-6, 94)]  # 바깥 윤곽 하나

def _round(pts, r=12):  # 꼭짓점마다 둥글린 닫힌 경로
    n = len(pts); out = []
    for i in range(n):
        (px, py), (x, y), (nx, ny) = pts[i - 1], pts[i], pts[(i + 1) % n]
        def toward(ax, ay, d):
            L = ((ax - x) ** 2 + (ay - y) ** 2) ** .5; k = min(d, L / 2) / L
            return x + (ax - x) * k, y + (ay - y) * k
        a, b = toward(px, py, r), toward(nx, ny, r)
        out.append(f'{"M" if i == 0 else "L"}{a[0]:g} {a[1]:g} Q{x:g} {y:g} {b[0]:g} {b[1]:g}')
    return ' '.join(out) + ' Z'
HULL = _round(HULL_PTS)
INSET, RX = 6, 16   # 갈 구역 표시: 구역 안쪽으로 살짝 들인 둥근 칠

def svg_map(x0, y0, k, hi, label=True, fs=11):
    """논리도 페이지용 지도. hi = 칠할 구역 이름"""
    out = (f'<path transform="translate({x0} {y0}) scale({k})" d="{HULL}" '
           f'style="fill:var(--sys-soft);stroke:var(--line);stroke-width:{1.5/k:.2f}"/>')
    for n, x, y, w, h in ROOMS:
        X, Y, W, Hh = x0 + x * k, y0 + y * k, w * k, h * k
        if n == hi:
            i = INSET * k
            out += (f'<rect x="{X+i:.1f}" y="{Y+i:.1f}" width="{W-2*i:.1f}" height="{Hh-2*i:.1f}" rx="{RX*k:.1f}" '
                    f'style="fill:{COLOR[n]};fill-opacity:.34"/>')
        if label:
            attr = ' font-weight="700"' if n == hi else ' class="t-mute"'
            out += f'<text x="{X+W/2:.1f}" y="{Y+Hh/2+fs*0.35:.1f}" text-anchor="middle" font-size="{fs}"{attr}>{n}</text>'
    return out

if __name__ == '__main__':  # 구역끼리 안 겹치고 모두 윤곽 안에 있어야 함
    def ov(a, b): return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]
    R = [r[1:] for r in ROOMS]
    assert not any(ov(R[i], R[j]) for i in range(5) for j in range(i + 1, 5))
    xs, ys = [p[0] for p in HULL_PTS], [p[1] for p in HULL_PTS]
    assert all(min(xs) <= x and x + w <= max(xs) and min(ys) <= y and y + h <= max(ys) for x, y, w, h in R)
    print('map ok', HULL[:40])
