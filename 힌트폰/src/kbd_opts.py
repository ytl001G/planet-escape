# 공통 규정 탭: 키보드 칸 시안 5가지 (고르는 중). 실제 CSS로 그림 · 그림자·빛 효과 없음
import pathlib
ROWS = ['ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ', 'ㅁㄴㅇㄹㅎㅗㅓㅏㅣ', 'ㅋㅌㅊㅍㅠㅜㅡ']
def kb(cls):
    r = ''.join(f'<div class="r">{"".join(f"<i>{k}</i>" for k in row)}</div>' for row in ROWS[:2])
    r += f'<div class="r"><i class="f">⇧</i>{"".join(f"<i>{k}</i>" for k in ROWS[2])}<i class="f">⌫</i></div>'
    r += '<div class="r"><i class="f w">한/영</i><i class="sp">띄어쓰기</i><i class="f w">완료</i></div>'
    return f'<div class="kb {cls}">{r}</div>'
OPTS = [('A', '지금 쓰는 것', '옅은 회색 칸. 글자 칸은 조금 밝게, 기능 키는 더 어둡게. 누르면 1부 보라.'),
        ('B', '테두리만', '칸 안은 비우고 얇은 선만. 배경 그림이 잘 보이고 가벼움.'),
        ('C', '칸 없이 글자만', '평소엔 글자만, 누를 때만 칸이 생김. 가장 깔끔하지만 누를 자리가 덜 보임.'),
        ('D', '진한 칸 (일반 폰 키보드처럼)', '불투명한 짙은 회색. 익숙하고 또렷함. 배경은 키보드 뒤로 가려짐.'),
        ('E', '부 색을 옅게 깐 칸', '1부 보라 · 2부 주황이 칸에 살짝. 화면과 한 벌로 보임.')]
CSS = """<style>
#ko { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; margin-top: 10px; }
#ko .op h4 { margin: 0 0 8px; font-size: 15px; } #ko .op p { margin: 8px 0 0; font-size: 12.5px; color: var(--muted); line-height: 1.5; }
#ko .ph { border-radius: 22px; padding: 70px 4px 12px; background: radial-gradient(120% 90% at 70% 10%, #4a2160 0%, #1c1026 50%, #0b0910 100%); border: 1.5px solid #3a3541; overflow: hidden; }
#ko .kb { display: grid; gap: 8px; color: #f2eef6; font: 500 15px var(--body); }
#ko .r { display: flex; gap: 5px; justify-content: center; }
#ko i { font-style: normal; width: 25px; height: 40px; border-radius: 6px; display: grid; place-items: center; user-select: none; }
#ko i.f { width: 36px; } #ko i.w { width: 54px; font-size: 12px; font-weight: 700; } #ko i.sp { width: 150px; font-size: 12px; color: rgba(255,255,255,.6); }
#ko i.dn { } /* 누른 칸 보기 */
#ko .A i { background: rgba(255,255,255,.13); } #ko .A i.f, #ko .A i.sp { background: rgba(255,255,255,.07); } #ko .A i.dn { background: color-mix(in srgb, #cf86e6 55%, transparent); }
#ko .B i { border: 1px solid rgba(255,255,255,.28); } #ko .B i.f { border-color: rgba(255,255,255,.16); } #ko .B i.dn { border-color: #cf86e6; color: #cf86e6; }
#ko .C i.f, #ko .C i.w { color: rgba(255,255,255,.6); } #ko .C i.dn { background: rgba(255,255,255,.16); }
#ko .D .kb { background: #1d1b21; margin: 0 -4px -12px; padding: 10px 4px 14px; border-radius: 16px 16px 0 0; } #ko .D i { background: #4a4750; } #ko .D i.f, #ko .D i.sp { background: #2f2d34; } #ko .D i.dn { background: #6b6772; }
#ko .E i { background: color-mix(in srgb, #cf86e6 18%, transparent); } #ko .E i.f, #ko .E i.sp { background: color-mix(in srgb, #cf86e6 9%, transparent); } #ko .E i.dn { background: color-mix(in srgb, #cf86e6 55%, transparent); }
</style>"""
dn = lambda s: s.replace('<i>ㅇ</i>', '<i class="dn">ㅇ</i>', 1)
cards = ''.join(f'<div class="op"><h4>{k}. {t}</h4><div class="ph">{dn(kb(k))}</div><p>{d} (보기의 ‘ㅇ’은 누른 칸)</p></div>' for k, t, d in OPTS)
html = CSS + '<h2 style="margin:28px 0 4px">키보드 칸 시안 <small style="font-size:13px;color:var(--muted);font-weight:500">고르는 중 · 한글 키보드 · 1부 보라 기준</small></h2><div id="ko">' + cards + '</div>\n'
pathlib.Path(__file__).with_name('kbd_opts.html').write_text(html, encoding='utf-8'); print('kbd opts', len(OPTS))
