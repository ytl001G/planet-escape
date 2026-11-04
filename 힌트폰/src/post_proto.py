# 시제품 조각을 논리도 페이지에 붙인다: 제목 아래, 화면 제안·순서도 위 / 목차 맨 앞에 '시험해 보기'
import pathlib, sys, json
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
part = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding='utf-8'))
for anchor in ('</style>', '<div class="split">', '<nav class="toc" aria-label="목차">', '</body>'):
    assert s.count(anchor) == 1, anchor
s = s.replace('</style>', part['css'] + '</style>')
s = s.replace('<div class="split">', part['html'] + '<div class="split">')
s = s.replace('<nav class="toc" aria-label="목차">', '<nav class="toc" aria-label="목차"><a href="#proto">시험해 보기</a>')
s = s.replace('</body>', part['js'] + '</body>')
p.write_text(s, encoding='utf-8'); print('proto inserted')
