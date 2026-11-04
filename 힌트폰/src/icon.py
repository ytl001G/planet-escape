# 행성탈출 로고로 힌트폰 앱 아이콘 만들기 (1024 정사각, 모서리는 OS가 깎음)
# 다른 생성기(screens/thumbs/proto)에서 nest()/inline()으로 가져다 쓴다. 힌트폰 폴더에서 실행 기준.
import pathlib, re, glob

def _logo():
    src = glob.glob('../[Nn]otion*/**/*.svg', recursive=True)  # 노션 내보내기마다 하위 폴더가 바뀜
    assert len(src) == 1, src                       # notion 자료/행성탈출_로고_최종.svg (이름은 NFD라 글자로 찾지 않음)
    s = pathlib.Path(src[0]).read_text(encoding='utf-8')
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s)[1].split()]
    paths = re.findall(r'<path d="([^"]+)"', s); assert paths
    return vb[2], vb[3], ''.join(f'<path d="{d}"/>' for d in paths)

PAL = {  # 배경 (가운데 · 중간 · 가장자리), 로고 (위 · 가운데 · 아래), 번짐 색
    'lily': (('#4a1a5e', '#24102e', '#120c18'), ('#f8e6fd', '#d99cf0', '#b15fd0'), '#cf86e6'),
    'gray': (('#3b3940', '#1f1e23', '#101013'), ('#f6f5f8', '#cbc8d0', '#8e8a96'), '#b8b4bf'),
}
def body(uid, round_=False, pal='lily'):
    (b0, b1, b2), (l0, l1, l2), gl = PAL[pal]
    W, H, logo = _logo()
    k = 600 / H                                     # 로고 높이 = 아이콘의 약 59% (안전 영역 안)
    tx, ty = (1024 - W * k) / 2, (1024 - H * k) / 2 + 10
    cp = f' clip-path="url(#{uid}-clip)"' if round_ else ''
    clip = f'<clipPath id="{uid}-clip"><rect width="1024" height="1024" rx="230"/></clipPath>' if round_ else ''
    return (f'<defs><radialGradient id="{uid}-bg" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="{b0}"/><stop offset=".55" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/></radialGradient>'
            f'<linearGradient id="{uid}-lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l0}"/><stop offset=".5" stop-color="{l1}"/><stop offset="1" stop-color="{l2}"/></linearGradient>'
            f'<filter id="{uid}-glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="22"/></filter>{clip}</defs>'
            f'<g{cp}><rect width="1024" height="1024" fill="url(#{uid}-bg)"/>'
            f'<g transform="translate({tx:.1f} {ty:.1f}) scale({k:.4f})">'
            f'<g fill="{gl}" opacity=".55" filter="url(#{uid}-glow)">{logo}</g>'
            f'<g fill="url(#{uid}-lg)">{logo}</g></g></g>')

def full(uid='appicon', pal='lily'):  # 파일용: 모서리 안 깎음
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">{body(uid, pal=pal)}</svg>'

def nest(uid, x, y, size):        # 다른 SVG 안에 넣는 둥근 아이콘
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 1024 1024">{body(uid, True)}</svg>'

def inline(uid, size):            # HTML 안에 넣는 둥근 아이콘
    return f'<svg width="{size}" height="{size}" viewBox="0 0 1024 1024" aria-hidden="true">{body(uid, True)}</svg>'

if __name__ == '__main__':
    out = pathlib.Path('로고'); out.mkdir(exist_ok=True)
    (out / 'app_icon.svg').write_text(full(), encoding='utf-8')
    (out / 'app_icon_gray.svg').write_text(full('appicon-gray', 'gray'), encoding='utf-8')  # 릴리 보라 대신 회색판
    print('icon ok')
