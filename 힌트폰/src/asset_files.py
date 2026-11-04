# 에셋 목록의 '에셋 파일' 칸: 힌트폰/에셋 폴더(assets_draw.py가 만듦)의 SVG를 실제 그림으로 보여 줌
import pathlib, base64

KINDS = ('공통', '1부', '2부', '이전', '채팅 아이콘 시안')

def kind(f):
    if '시안' in f.stem: return '채팅 아이콘 시안'
    return next((k for k in ('1부', '2부', '이전') if f.stem.endswith('_' + k)), '공통')

def tile(f):
    u = base64.b64encode(f.read_bytes()).decode()
    return f'    <figure class="afile"><div><img src="data:image/svg+xml;base64,{u}" alt="{f.stem}"></div><figcaption>{f.stem}</figcaption></figure>\n'

def section(folder='에셋'):
    fs = sorted(pathlib.Path(folder).glob('*.svg'))
    if not fs: return '', 0
    body = ''
    for k in KINDS:
        g = [f for f in fs if kind(f) == k]
        if g: body += f'  <h3 class="fk">{k} <small>{len(g)}개</small></h3>\n  <div class="fgrid">\n' + ''.join(map(tile, g)) + '  </div>\n'
    return body, len(fs)  # 꾸밈은 post_assets.py 스타일에 (페이지에 <style>은 하나만)
