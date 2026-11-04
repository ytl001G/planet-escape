import pathlib,sys,re
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
# 손으로 그린 옛 메인 화면들: 아래 '힌트코드' 버튼 → 폰 홈 화면의 아래 독(힌트코드 · 스토리코드 · 운영자 호출) + 상태 표시줄 · 홈 바
def dock(x, y, w, cls, k):
    out = f'<rect x="{x-4*k:g}" y="{y-20*k:g}" width="{w+8*k:g}" height="{76*k:g}" rx="{20*k:g}" class="soft"/>'
    names = ('힌트코드', '스토리코드', '운영자 호출') if cls == 'via' else ('힌트코드', '운영자 호출')  # 스토리코드는 비아 등장 뒤에만
    for i, l in enumerate(names):
        cx = x + w * (i * 2 + 1) / (2 * len(names))
        out += f'<rect x="{cx-19*k:g}" y="{y-11*k:g}" width="{38*k:g}" height="{38*k:g}" rx="{10*k:g}" class="{cls}"/>'
        out += f'<text x="{cx:g}" y="{y+48*k:g}" text-anchor="middle" font-size="{9*k:g}" font-weight="500">{l}</text>'
    return out
def sbar(o):
    return (f'<text x="{34+o}" y="29" font-size="9" font-weight="700">9:41</text>'
            f'<path d="M{o+228} 24 a6 6 0 0 1 9 0 M{o+230} 26.5 a3.2 3.2 0 0 1 5 0" fill="none" class="ln" stroke-width="1.4"/><circle cx="{o+232.5}" cy="28.5" r="1.2" fill="currentColor"/>'
            f'<rect x="{o+242}" y="22.5" width="14" height="7.5" rx="2" class="n"/><rect x="{o+243.5}" y="24" width="9" height="4.5" rx="1" class="soft"/>')
o1 = '''      <rect x="40" y="52" width="210" height="58" rx="10" class="soft"/>
      <text x="145" y="99" text-anchor="middle" font-size="24" font-weight="700">58:30</text>
      <rect x="40" y="124" width="210" height="232" rx="12" class="n dashbox"/>'''
assert s.count(o1) == 1  # 안전 모드 이전: 가운데 큰 타이머만 (빈 안내 창 없음)
s = s.replace(o1, '      <text x="145" y="215" text-anchor="middle" font-size="44" font-weight="700">1:40:30</text>')
s = s.replace('안전 모드 이전 메인 화면: 위에 타이머, 가운데 진행 가이드 자리는 비어 있고, 아래에 힌트코드 버튼.', '안전 모드 이전 메인 화면: 잠금 화면처럼 가운데 큰 타이머만 있고 안내 창은 없다. 아래에 앱 아이콘 세 개.', 1)
big = iter(['n', 'lily', 'lily'])  # 안전 모드 이전 · (지운 스토리카드 화면) · 이후 1부
def rep_big(m):
    x = int(m[1]); cls = 'via' if x == 350 else next(big); o = x - 40
    return dock(x, 380, 210, cls, 1) + sbar(o + 10)
s, n1 = re.subn(r'<rect x="(\d+)" y="372" width="210" height="50" rx="10" class="n"/>\s*<text x="\d+" y="402" text-anchor="middle" font-size="13" font-weight="700">힌트코드</text>', rep_big, s)
small = iter(['lily', 'lily', 'via'])  # 안전 모드 가동 끝 · 비아 등장 전 · 비아 등장 후
s, n2 = re.subn(r'<rect x="(\d+)" y="302" width="168" height="44" rx="8" class="n"/>\s*<text x="\d+" y="329" text-anchor="middle" font-size="12" font-weight="700">힌트코드</text>',
                lambda m: dock(int(m[1]), 302 + 4, 168, next(small), 0.8), s)
assert (n1, n2) == (4, 3), (n1, n2)
# 옛 그림의 예시 시간 MM:SS → 105분 형식 시:분:초 (45분 이상은 0시간대)
s, n3 = re.subn(r'(font-weight="700"[^>]*>)(\d\d):(\d\d)(</text>)', lambda m: m[0] if m[2] + m[3] == '0000' else f'{m[1]}{"1" if int(m[2]) < 45 else "0"}:{m[2]}:{m[3]}{m[4]}', s)
print('old times → h:mm:ss', n3)
p.write_text(s,encoding='utf-8'); print('old main buttons → dock', n1, n2)
