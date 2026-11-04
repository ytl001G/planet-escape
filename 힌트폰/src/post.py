import pathlib,sys,re
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
# 메인 화면 버튼 이름: 힌트코드 → 힌트 (코드 입력 화면 제목 14px은 그대로)
s,n=re.subn(r'(font-size="1[23]" font-weight="700">)힌트코드(</text>)',r'\1힌트\2',s)
p.write_text(s,encoding='utf-8'); print('main buttons renamed',n)
