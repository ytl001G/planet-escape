# 라이트/다크 모드와 상관없이 항상 같은 모양: 어두운 색 값을 기본으로 박고, 모드에 따라 바뀌는 규칙을 모두 지운다
import pathlib, sys, re
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')

def kv(block):  # '--a: #x; --b: #y;' → dict
    return dict(re.findall(r'(--[\w-]+):\s*([^;]+);', block))

# 1) 페이지 색: 다크 값 → :root 기본값
m = re.search(r'@media \(prefers-color-scheme: dark\) \{\n  :root:not\(\[data-theme="light"\]\) \{\n(.*?)\n  \}\n\}\n', s, re.S)
assert m; dark = kv(m.group(1)); s = s.replace(m.group(0), '', 1)
m2 = re.search(r':root\[data-theme="dark"\] \{\n.*?\n\}\n', s, re.S); assert m2; s = s.replace(m2.group(0), '', 1)
root = re.search(r':root \{\n.*?\n\}\n', s, re.S); assert root
blk = root.group(0)
for k, v in dark.items():
    blk, n = re.subn(rf'({re.escape(k)}:\s*)[^;]+;', rf'\g<1>{v};', blk); assert n == 1, k
blk = blk.replace('color-scheme: light;', 'color-scheme: dark;')
s = s.replace(root.group(0), blk, 1)

# 2) 에셋 목록 상태 색
m = re.search(r'@media \(prefers-color-scheme: dark\) \{ :root:not\(\[data-theme="light"\]\) #assets \{\n(.*?)\} \}\n', s, re.S)
assert m; adark = kv(m.group(1)); s = s.replace(m.group(0), '', 1)
m2 = re.search(r':root\[data-theme="dark"\] #assets \{[^}]*\}\n', s); assert m2; s = s.replace(m2.group(0), '', 1)
a = re.search(r'#assets \{ display: grid;[^}]*\}', s); assert a
ab = a.group(0)
for k, v in adark.items():
    ab, n = re.subn(rf'({re.escape(k)}:\s*)[^;]+;', rf'\g<1>{v};', ab); assert n == 1, k
s = s.replace(a.group(0), ab, 1)

assert 'prefers-color-scheme' not in s and 'data-theme' not in s, '모드에 따라 바뀌는 규칙이 남음'
s = s.replace('<html lang="ko">', '<html lang="ko" style="color-scheme: dark">', 1)
s = s.replace('<head>', '<head>\n<meta name="color-scheme" content="dark">', 1)
p.write_text(s, encoding='utf-8'); print('theme fixed: dark', len(dark), len(adark))
