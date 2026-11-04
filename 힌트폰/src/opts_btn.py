# 공통 규정 탭: 안전 모드 뒤 타이머 틀 + 버튼 기본 틀 시안 5가지 (고르는 중). 실제 CSS로 그림
import pathlib
CSS = """<style>
#bo { display: grid; grid-template-columns: repeat(auto-fill, minmax(232px, 1fr)); gap: 18px; margin-top: 10px; }
#bo .op h4 { margin: 0 0 8px; font-size: 15px; } #bo .op p { margin: 8px 0 0; font-size: 12.5px; color: var(--muted); line-height: 1.5; }
#bo .ph { height: 430px; border-radius: 28px; padding: 18px 14px; display: flex; flex-direction: column; gap: 12px; color: #f2eef6;
  background: radial-gradient(120% 70% at 70% 35%, #4a2160 0%, #1c1026 45%, #0b0910 100%); border: 1.5px solid #3a3541; overflow: hidden; font-family: inherit; }
#bo .tm { font: 700 38px/1 'IBM Plex Mono', monospace; font-variant-numeric: tabular-nums; display: grid; place-items: center; }
#bo .card { padding: 14px; } #bo .card small { color: #cf86e6; font-size: 11px; font-weight: 700; } #bo .card b { display: block; font-size: 16px; margin-top: 4px; }
#bo .row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; } #bo .b { height: 44px; display: grid; place-items: center; font-size: 14px; font-weight: 700; }
/* A 틀 없음 */
#bo .A .tm { height: 86px; font-size: 46px; text-shadow: 0 0 24px rgba(207,134,230,.45); }
#bo .A .card { background: rgba(255,255,255,.06); border-radius: 16px; }
#bo .A .b { border-radius: 12px; background: rgba(255,255,255,.10); } #bo .A .b.p { background: #cf86e6; color: #1a0f20; }
/* B 유리 알약 */
#bo .B .tm { height: 72px; margin: 0 4px; font-size: 34px; border-radius: 999px; background: rgba(255,255,255,.08); backdrop-filter: blur(10px); box-shadow: inset 0 1px 0 rgba(255,255,255,.18), 0 8px 24px rgba(0,0,0,.35); }
#bo .B .card { border-radius: 22px; background: rgba(255,255,255,.07); box-shadow: inset 0 1px 0 rgba(255,255,255,.12); }
#bo .B .b { border-radius: 999px; background: rgba(255,255,255,.10); box-shadow: inset 0 1px 0 rgba(255,255,255,.16); } #bo .B .b.p { background: linear-gradient(180deg, #dba0ee, #b86ad3); color: #1a0f20; }
/* C 빛 테두리 */
#bo .C .tm { height: 80px; border-radius: 18px; border: 1.5px solid transparent; background: linear-gradient(#170f1e, #170f1e) padding-box, linear-gradient(135deg, #cf86e6, rgba(207,134,230,.05) 60%, #7b5cff) border-box; box-shadow: 0 0 22px rgba(207,134,230,.25); }
#bo .C .card { border-radius: 14px; border: 1px solid rgba(207,134,230,.35); background: rgba(20,12,26,.6); }
#bo .C .b { border-radius: 12px; border: 1px solid rgba(207,134,230,.45); background: rgba(20,12,26,.6); } #bo .C .b.p { border-color: #cf86e6; box-shadow: 0 0 14px rgba(207,134,230,.45); color: #e9c2f5; }
/* D 톤 채움 */
#bo .D .tm { height: 80px; border-radius: 20px; background: rgba(207,134,230,.16); color: #f4dafb; }
#bo .D .card { border-radius: 20px; background: rgba(255,255,255,.07); }
#bo .D .b { border-radius: 16px; background: rgba(207,134,230,.16); color: #ecc8f7; } #bo .D .b.p { background: #cf86e6; color: #1a0f20; }
/* E 둥근 링 */
#bo .E .ring { width: 132px; height: 132px; margin: 0 auto; border-radius: 50%; display: grid; place-items: center; background: conic-gradient(#cf86e6 0 82%, rgba(255,255,255,.10) 0); -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 6px)); mask: radial-gradient(farthest-side, transparent calc(100% - 7px), #000 calc(100% - 6px)); }
#bo .E .rw { position: relative; height: 132px; } #bo .E .rw .tm { position: absolute; inset: 0; font-size: 26px; }
#bo .E .card { border-radius: 18px; background: rgba(255,255,255,.07); }
#bo .E .b { border-radius: 999px; background: rgba(255,255,255,.10); } #bo .E .b.p { background: #cf86e6; color: #1a0f20; }
</style>"""
def phone(k):
    tm = '<div class="tm">1:38:15</div>'
    if k == 'E': tm = '<div class="rw"><div class="ring"></div><div class="tm">1:38:15</div></div>'
    return (f'<div class="ph {k}">{tm}<div class="card"><small>현재 목표</small><b>에바의 승인 확보</b></div>'
            '<div class="row"><div class="b">힌트 보기</div><div class="b">진행도</div></div><div class="b p">다음 힌트</div></div>')
OPTS = [('A', '틀 없음', '타이머는 상자 없이 숫자만 크게, 은은한 빛. 버튼은 테두리 없는 반투명 칸, 주 버튼만 색으로 채움.'),
        ('B', '유리 알약', '타이머를 둥근 알약 유리판에. 버튼도 끝이 완전히 둥근 알약, 위쪽에 얇은 빛 반사.'),
        ('C', '빛 테두리', '어두운 판 + 보라빛 그라데이션 테두리. 우주선 계기판 느낌. 주 버튼은 테두리가 빛남.'),
        ('D', '톤 채움', '테두리 없이 보라를 옅게 깐 판. 모서리 크게(20). 주 버튼만 진한 보라 — 요즘 폰 앱(머티리얼) 느낌.'),
        ('E', '둥근 링', '노션 와이어프레임의 큰 동그라미 타이머. 링이 남은 시간만큼 줄어듦. 버튼은 알약.')]
html = ('<section>' + CSS + '\n  <h2>타이머 · 버튼 틀 시안 <small>고르는 중 · 1부 보라 기준</small></h2>\n  <div id="bo">'
        + ''.join(f'<div class="op"><h4>{k}. {t}</h4>{phone(k)}<p>{d}</p></div>' for k, t, d in OPTS) + '</div>\n</section>\n')
pathlib.Path(__file__).with_name('rules_opts.html').write_text(html, encoding='utf-8'); print('opts', len(OPTS))
