# 시험판 '에셋 적용': assets_draw.py의 새 에셋을 CSS(data URI)와 바꿔 낄 아이콘으로 만들어 proto.py에 넘김
import base64, json
import assets_draw as AD

def U(n): return 'url("data:image/svg+xml;base64,' + base64.b64encode(AD.A[n].encode()).decode() + '")'
def NINE(sel, n, s):  # 모서리는 그대로 두고 가운데만 늘림 (border-image 9칸)
    return f'{sel} {{ background: none; border-color: transparent; -webkit-backdrop-filter: none; backdrop-filter: none; border-image: {U(n)} {s} fill / {s}px stretch; }}\n'

c2l, c2d = AD.PART['2부'][1], AD.PART['2부'][2]
CSS = (NINE('#proto.skin .lb-code', '입력_판', 16) + NINE('#proto.skin .input', '입력_칸', 12) + NINE('#proto.skin .btn', '버튼', 12) + NINE('#proto.skin .btn.ans', '버튼_정답', 12)
       + NINE('#proto.skin .card.h1', '힌트_카드_틀_1부', 16) + NINE('#proto.skin .card.h2', '힌트_카드_틀_2부', 16) + NINE('#proto.skin .card.ansc', '정답_칸_틀', 14)
       + NINE('#proto.skin .key', '키_기본', 8) + NINE('#proto.skin .key.num', '키_숫자줄', 8)
       + NINE('#proto.skin .key.mid, #proto.skin .key.wide, #proto.skin .key.wide2', '키_넓은', 8) + NINE('#proto.skin .kbd', '키보드_판', 22)
       + '#proto.skin .lb-goal { padding-left: 24px; } #proto.skin .lb-goal:has(.bia), #proto.skin .lb-goal:has(.bigck) { padding-left: 14px; } #proto.skin .card.h1, #proto.skin .card.h2 { padding-left: 26px; }\n'  # 왼쪽 세로 막대만큼 글자를 띄움
       + '#proto.skin .idle .timer { width: 316px; height: 316px; font-size: 40px; } #proto.skin .idle .timer .prog { top: 63%; font-size: 14px; }\n'  # 시계는 키우고 남은 시간 글자는 줄임
       + '#proto.skin .idle .timer .tr { fill: none; stroke: none; } #proto.skin .idle .timer .tp { r: 66px; stroke-width: 3.6; }\n'
       + '#proto.skin .bigck { background-color: transparent; } #proto.skin .bigck svg { visibility: hidden; } #proto.skin .badge { outline: 2px solid #1a1220; }\n'
       + f'#proto.skin .bia .av {{ border-color: transparent; background: {U("비아_동그라미_틀")} center/100% no-repeat; }} #proto.skin .wave span {{ background: linear-gradient(135deg, {c2l}, {c2d}); }}\n')
for p, cls in (('1부', 'p1'), ('2부', 'p2'), ('이전', 'pre')):
    q = '1부' if p == '이전' else p; S0 = f'#proto.skin .ph.{cls}'
    CSS += (NINE(f'{S0} .lb-chatbox', f'채팅_칸_틀_{p}', 24) + NINE(f'{S0} .lb-goal', f'목표_칸_틀_{q}', 24)
            + NINE(f'{S0} .lb-goal:has(.bia), {S0} .lb-goal:has(.bigck), {S0} .mapbox', f'판_틀_{q}', 24)
            + NINE(f'{S0} .btn:active', f'버튼_눌림_{q}', 12) + NINE(f'{S0} .key:active, {S0} .key.mid.on', f'키_눌림_{q}', 8)
            + f'{S0} .idle .timer {{ background: {U("타이머_링_틀_" + p)} center/100% 100% no-repeat; }} {S0} .bigck {{ background: {U("완료_체크_큰_" + q)} center/100% no-repeat; }}\n')

def SI(body, w, h, vb='0 0 24 24', style=''): return f'<svg width="{w}" height="{h}" viewBox="{vb}" aria-hidden="true"{style}>{body}</svg>'
ICON = {'pin': SI(AD.IC['핀'], 14, 18, '4 2 16 20.5', ' style="color:var(--c1)"'), 'ck': SI(AD.IC['체크'], 40, 40, style=' style="color:#211e26"'),
        'chev': SI(AD.IC['꺾쇠'], 8, 12, '7 3 11 18'), 'x': SI(AD.IC['닫기'], 16, 16), 'back': SI(AD.IC['뒤로'], 20, 20), 'send': SI(AD.IC['보내기'], 20, 20),
        'del': SI(AD.IC['지우기'], 24, 18, '0.5 2.5 23 18'), 'shift': SI(AD.IC['시프트'], 18, 18), 'sw': SI(AD.IC['와이파이'], 16, 12, '2.5 5.5 19 14.25'),
        'swoff': SI(AD.IC['와이파이_끊김'], 16, 12, '1 2.5 22 16.5'), 'bat': SI(AD.IC['배터리'], 24, 12, '1.5 6 22 11')}
CHAT = {k: SI(b, 38, 34) for k, b in AD.CHAT.items()}
JSDECL = 'const SKINICON = ' + json.dumps(ICON, ensure_ascii=False) + ', SKINCHAT = ' + json.dumps(CHAT, ensure_ascii=False) + ';\n'
