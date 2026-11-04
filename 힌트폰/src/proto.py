# 힌트폰 시제품(눌러 보는 앱) 조각을 만든다 → post_proto.py가 논리도 페이지 위쪽에 붙인다
import pathlib, sys, base64, io, json
from PIL import Image
HP = pathlib.Path(sys.argv[1])          # 힌트폰 폴더
OUT = pathlib.Path(sys.argv[2])         # 조각 html

def bg64(name):
    im = Image.open(HP / '배경' / f'{name}.png').convert('RGB').resize((540, 1204), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=78)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
BG = {k: bg64(k) for k in ('bg_pre', 'bg_part1', 'bg_part2', 'bg_end_planet')}
SHIELD = (HP / '로고' / 'shield_plain.svg').read_text(encoding='utf-8').replace('shield_', 'pv_shield_').replace('width="512" height="512"', 'width="100%" height="100%"')

sys.path.insert(0, str(pathlib.Path(__file__).parent)); from shipmap import ROOMS as MAP_ROOMS, HULL as MAP_HULL, INSET as MAP_INSET, RX as MAP_RX
# 화면 문구: 시나리오·대사집·논리도에 있는 문장만. 정해지지 않은 문구는 null → 회색 막대
DATA = {
    'goals': [['알렉스의 승인 확보', '알렉스의 방'], ['오펠리아의 승인 확보', '오펠리아의 방'], ['노아의 승인 확보', '노아의 방'],
              ['오펠리아 재방문', '오펠리아의 방'], ['에바의 승인 확보', '에바의 방'], ['릴리의 승인', '릴리의 방']],
    'bia': ['우선 알렉스의 방에 다시 가 보지 않을래? 뭔가 남아 있는 것 같거든.',
            '오펠리아의 보고서에 제온이 뇌에 영향을 준다고 적혀 있었지? 그쪽을 다시 확인해 보자.',
            '혹시 노아가 가져간 거 아냐? 노아 방에 가 보자!',
            '네 방에 가 보자. 뭘 바꿔 놓았는지 궁금해.',
            '…뭔가 알아낸 모양이네. 좋아. 일단 가 보자고.'],
    'card135': {'title': '제온 추진 연료 전환 실험', 'by': '— 에바 펠로노르',
                'lines': ['소규모 실험에서 추진에 이용할 수 있는 반응을 확인했다.', '하지만 반응을 오래 유지하지 못했고, 현재 추진 장치에 적용하는 방법도 해결하지 못했다.',
                          '실험 조건과 실패 기록을 함께 남긴다.', '당장 돌아갈 방법은 아니지만, 연구를 이어 갈 가치는 있다.']},
    # 시험용 코드 (코드 형식은 아직 미정)
    'codes': {
        'ABCD': {'kind': 'hint', 'part': 1, 'pct': 38, 'hints': ['특정 동작을 통해 숨겨진 것을 알아내자.', '드래그했을 때 뭔가 보이는 것 같다.',
                                                              '각 행성일마다 한 글자씩 하이라이트되며, 이를 합쳐 답을 알 수 있다.'], 'answer': '끝없는탐구'},
        'KLMN': {'kind': 'hint', 'part': 2, 'pct': 72, 'hints': ['별자리 필름이 다시 필요해 보이네.', None, None], 'answer': None},
        'WXYZ': {'kind': 'voice', 'part': 2, 'pct': 95, 'steps': [[['노아', '뭘 기다려. 내리기만 하면 돼.']],
                                                           [['에바', '근데 만약 이게 실패하면? 그때를 대비해서 계획을 하나 더 만들어 둬야겠어.'], ['비아', '…방금 그거 뭐였지?']],
                                                           [['노아', '계속 서 있을 거야? 누가 답이라도 알려 줄 것 같아?']],
                                                           [['오펠리아', '다들 너한테 선택하라고만 했잖아. 혹시 다른 선택은 없을까?'], ['노아', '다른 거? 위로 올려 보기라도 하게? 관둬. 나도 해 봤는데 안 올라가더라.']],
                                                           [['릴리', '넌 어릴 때부터 그랬어. 계획을 하나씩 더 세웠지.']],
                                                           [['비아', '있잖아. 나 살고 싶어. 이제 막 생겼거든.']]]},  # 대사집 1707~1714
        'PQRS': {'kind': 'story'},
    },
    'pattern': [0, 6, 5],  # 시험용 정답: 가운데 → 왼쪽 위 → 왼쪽 아래 (실제 정답은 보너스 문제 담당에게 받기)
    'map': {'rooms': [list(r) for r in MAP_ROOMS], 'hull': MAP_HULL, 'inset': MAP_INSET, 'rx': MAP_RX},
    'bia_intro': [['보호 시스템 로딩 중…', '로딩 완료.'], ['안녕! 나는 Virtual Entity AI.', '줄여서 V.E.A.', '그냥 비아라고 불러도 돼.']],
}

CSS = r'''
#proto { display: grid; gap: 16px; }
#proto .proto-wrap { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 28px; align-items: start; }
@media (max-width: 860px) { #proto .proto-wrap { grid-template-columns: minmax(0, 1fr); justify-items: center; } }
#proto .stage { width: 384px; height: 827px; position: relative; }
#proto .ph { position: absolute; left: 0; top: 0; width: 384px; height: 827px; border-radius: 52px; border: 12px solid #050407; background: #000; overflow: hidden;
  box-shadow: 0 0 0 1px var(--line), 0 18px 50px rgba(0,0,0,.45); transform-origin: 0 0; color: #f2eef6; font-family: var(--body); user-select: none; -webkit-user-select: none; }
#proto .bg { position: absolute; inset: 0; background-size: cover; background-position: center; transition: opacity .6s; }
#proto .layer { position: absolute; inset: 0; display: flex; flex-direction: column; padding: 34px 18px 22px; gap: 14px; }
#proto .hidden { display: none !important; }
#proto .layer.enter { animation: penter .5s ease-out; }
@keyframes penter { from { opacity: 0; transform: scale(.96); } }
#proto .sv { position: relative; width: 140px; height: 140px; flex: none; }
#proto .sv > * { position: absolute; inset: 0; width: 100%; height: 100%; }
#proto .sv.zoom .sv-in { animation: ppop .5s ease-out; }
#proto .sf-t { animation: pfadein .5s .3s both; }
@keyframes pfadein { from { opacity: 0; transform: translateY(6px); } }
#proto .ph.paused * { animation-play-state: paused !important; }
#proto .pz { position: absolute; inset: 0; z-index: 5; display: grid; place-items: center; background: rgba(0,0,0,.55); cursor: pointer; }
#proto .pz span { width: 84px; height: 84px; border-radius: 50%; border: 2px solid rgba(255,255,255,.7); display: grid; place-items: center; }
#proto .glass { background: rgba(24, 21, 30, .62); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border: 1.5px solid rgba(255,255,255,.12); border-radius: 14px; }
#proto .timer { height: 76px; display: flex; align-items: center; justify-content: center; position: relative; font: 700 36px var(--display); font-variant-numeric: tabular-nums; letter-spacing: .02em; }
#proto .sbar { position: absolute; top: 0; left: 0; right: 0; height: 30px; padding: 0 26px; display: flex; align-items: center; justify-content: space-between; font: 700 12px var(--body); color: #f2eef6; z-index: 5; pointer-events: none; font-variant-numeric: tabular-nums; }
#proto .sbar .ic { display: flex; gap: 6px; align-items: center; }
#proto .sbar .off { color: #E5484D; }
#proto .hbar { position: absolute; bottom: 7px; left: 50%; width: 120px; height: 4px; margin-left: -60px; border-radius: 2px; background: rgba(255,255,255,.55); z-index: 5; pointer-events: none; }
#proto .dock { display: flex; justify-content: space-around; padding: 12px 6px 10px; border-radius: 26px; }
#proto .app { display: grid; justify-items: center; gap: 6px; cursor: pointer; font: 500 11px var(--body); color: #f2eef6; background: none; border: 0; }
#proto .app i { position: relative; width: 54px; height: 54px; border-radius: 15px; display: grid; place-items: center; color: #fff; background: linear-gradient(160deg, #a24bc4, #5a1f78); box-shadow: inset 0 0 0 1px rgba(255,255,255,.18); }
#proto .p2 .app i { background: linear-gradient(160deg, #ffa53d, #a85a00); }
#proto .pre .app i { background: linear-gradient(160deg, #5b5763, #2c2a31); }
#proto .dock.off .app { cursor: default; opacity: .45; }
#proto .app .badge { right: -5px; top: -5px; }
#proto .toast { position: absolute; top: 34px; left: 12px; right: 12px; z-index: 6; display: flex; gap: 10px; align-items: center; padding: 10px 12px; border-radius: 18px; cursor: pointer; animation: tdrop .35s ease-out; }
#proto .toast i { width: 32px; height: 32px; border-radius: 9px; display: grid; place-items: center; background: linear-gradient(160deg, #a24bc4, #5a1f78); flex: none; }
#proto .p2 .toast i { background: linear-gradient(160deg, #ffa53d, #a85a00); }
#proto .toast b { display: block; font: 700 13px var(--body); }
@keyframes tdrop { from { transform: translateY(-24px); opacity: 0; } }
#proto .srow { display: grid; grid-template-columns: 1fr 52px; gap: 8px; }
#proto .srow .btn { height: auto; }
#proto .op { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; cursor: pointer; }
#proto .badge { position: absolute; right: -4px; top: -6px; min-width: 18px; height: 18px; padding: 0 5px; border-radius: 9px; background: #E5484D; color: #fff; font: 700 11px/18px var(--body); text-align: center; }
#proto .guide { flex: 1; padding: 18px; display: flex; flex-direction: column; gap: 10px; position: relative; overflow: hidden; }
#proto .p1 .guide { border-color: var(--lily); }
#proto .p2 .guide { border-color: var(--via); }
#proto .pre .guide { border-style: dashed; }
#proto .lbl { font-size: 12px; font-weight: 700; }
#proto .p1 .lbl, #proto .t-lily { color: #d99cf0; }
#proto .p2 .lbl, #proto .t-via { color: #ffb460; }
#proto .goal { font: 700 19px/1.35 var(--display); }
#proto .room { display: flex; align-items: center; gap: 6px; font-weight: 700; font-size: 14px; color: #d99cf0; }
#proto .room[data-act] { cursor: pointer; align-self: flex-start; border-radius: 6px; }
#proto .room[data-act]:focus-visible { outline: 2px solid #cf86e6; outline-offset: 3px; }
#proto .mapov { position: absolute; inset: 0; z-index: 3; display: grid; place-items: center; padding: 18px; background: rgba(0,0,0,.55); animation: pfadein .25s; }
#proto .mapbox { position: relative; width: 100%; padding: 50px 12px 16px; background: rgba(24,21,30,.94); }
#proto .mapbox svg { display: block; width: 100%; height: auto; }
#proto .mapx { position: absolute; right: 10px; top: 10px; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; cursor: pointer; border: 1.5px solid rgba(255,255,255,.18); }
#proto .mapx:focus-visible { outline: 2px solid #cf86e6; }
#proto .vline { display: grid; gap: 4px; font-size: 14px; line-height: 1.55; }
#proto .spk { display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; color: rgba(242,238,246,.8); }
#proto .spk i { width: 8px; height: 8px; border-radius: 50%; }
#proto .vdots { display: flex; gap: 8px; justify-content: center; }
#proto .vdots span { width: 10px; height: 10px; border-radius: 5px; }
#proto .heart { color: #ffae4d; display: block; animation: pbeat 1.1s infinite; }
@keyframes pbeat { 0%, 40%, 100% { transform: scale(1); } 12% { transform: scale(1.18); } 26% { transform: scale(1.08); } }
#proto .ex { color: rgba(242,238,246,.45); font: 400 13px/1.5 var(--body); }
#proto .sep { height: 1px; background: rgba(255,255,255,.12); margin: 4px 0; }
#proto .iconbtn { position: absolute; right: 12px; top: 12px; width: 36px; height: 36px; border-radius: 50%; display: grid; place-items: center; cursor: pointer; border: 1.5px solid rgba(255,255,255,.18); background: rgba(24,21,30,.7); }
#proto .btn { height: 52px; border-radius: 10px; display: grid; place-items: center; font: 700 15px var(--body); cursor: pointer; border: 1.5px solid rgba(255,255,255,.2); background: rgba(24,21,30,.72); color: #f2eef6; position: relative; }
#proto .btn.on1 { background: rgba(142,36,170,.42); border-color: #cf86e6; }
#proto .btn.on2 { background: rgba(196,106,0,.38); border-color: #ffae4d; }
#proto .btn.next1 { color: #d99cf0; } #proto .btn.next2 { color: #ffb460; }
#proto .btn.ans { background: #a7a3ad; border-color: #a7a3ad; color: #17151b; }
#proto .btn:active { transform: translateY(1px); }
#proto .row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
#proto .head { display: grid; grid-template-columns: 96px 1fr 96px; align-items: center; margin: -34px -18px 0; padding: 34px 18px 12px; box-sizing: content-box; min-height: 40px; border-bottom: 1px solid rgba(255,255,255,.16); background: rgba(12,10,16,.5); }
#proto .head .ttl { text-align: center; font: 700 16px var(--display); }
#proto .head .tm { justify-self: end; display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px 4px 8px; border-radius: 99px; border: 1px solid rgba(255,255,255,.2); background: rgba(255,255,255,.08); font: 700 13px var(--body); font-variant-numeric: tabular-nums; }
#proto .head .tm svg { width: 13px; height: 13px; opacity: .75; }
#proto .back { width: 36px; height: 36px; display: grid; place-items: center; cursor: pointer; border-radius: 50%; }
#proto .input { height: 54px; border-radius: 10px; padding: 0 16px; font: 700 20px 'IBM Plex Mono', monospace; letter-spacing: .12em; background: rgba(24,21,30,.72); border: 1.5px solid rgba(255,255,255,.2); color: #fff; outline: none; width: 100%; text-transform: uppercase; }
#proto .input:focus { border-color: rgba(255,255,255,.45); }
#proto .scroll { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; padding-bottom: 6px; scrollbar-width: none; }
#proto .card { border-radius: 12px; padding: 12px 14px; display: grid; gap: 6px; font-size: 14px; line-height: 1.5; }
#proto .card.h1 { background: rgba(142,36,170,.3); border: 1.5px solid #cf86e6; }
#proto .card.h2 { background: rgba(196,106,0,.28); border: 1.5px solid #ffae4d; }
#proto .card .k { font-size: 12px; font-weight: 700; }
#proto .card.ansc { background: #a7a3ad; color: #17151b; }
#proto .card.ansc .v { font: 700 22px var(--display); }
#proto .pct { display: grid; gap: 6px; justify-items: center; }
#proto .pct i { display: block; width: 70%; height: 5px; border-radius: 3px; background: rgba(255,255,255,.18); overflow: hidden; }
#proto .pct i b { display: block; height: 100%; border-radius: 3px; transition: width .8s; }
#proto .on1 .pct i b { background: #cf86e6; } #proto .on2 .pct i b { background: #ffae4d; }
#proto .bia { display: flex; gap: 10px; align-items: flex-start; }
#proto .bia .av { flex: none; width: 40px; height: 40px; border-radius: 50%; border: 1.5px solid #ffae4d; background: rgba(196,106,0,.3); display: grid; place-items: center; font: 700 12px var(--body); color: #ffb460; }
#proto .bia .say { background: rgba(24,21,30,.75); border: 1.5px solid rgba(255,255,255,.14); border-radius: 12px; padding: 10px 12px; font-size: 14px; line-height: 1.55; }
#proto .wave { display: flex; gap: 4px; align-items: center; height: 46px; justify-content: center; }
#proto .wave span { width: 5px; border-radius: 3px; background: #ffae4d; animation: pwave 1s infinite ease-in-out; }
@keyframes pwave { 0%, 100% { transform: scaleY(.35); } 50% { transform: scaleY(1); } }
#proto .center { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; text-align: center; }
#proto .offmsg { margin: 0; font: 700 17px var(--display); color: #f2eef6; }
#proto .load { width: 160px; height: 6px; border-radius: 3px; background: rgba(255,255,255,.16); overflow: hidden; }
#proto .load b { display: block; height: 100%; width: 0; background: #cf86e6; border-radius: 3px; }
#proto .load.go b { animation: pload var(--d, 2s) linear forwards; }
@keyframes pload { to { width: 100%; } }
#proto .full1 { background: rgba(60, 18, 76, .55); }
#proto .bigck { width: 76px; height: 76px; border-radius: 50%; background: #cf86e6; display: grid; place-items: center; animation: ppop .4s; }
@keyframes ppop { from { transform: scale(.4); opacity: 0; } }
#proto .story { border-radius: 12px; padding: 14px 16px; font-size: 14px; line-height: 1.6; }
#proto .story.lily { background: rgba(142,36,170,.32); border: 1.5px solid #cf86e6; }
#proto .story.eva { background: rgba(30,136,229,.25); border: 1.5px solid #64b5f6; }
#proto .story .by { text-align: right; color: rgba(242,238,246,.7); font-size: 13px; margin-top: 6px; }
#proto .pat { position: relative; width: 280px; height: 280px; margin: 0 auto; touch-action: none; }
#proto .pat svg { width: 100%; height: 100%; }
#proto .msgs { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; scrollbar-width: none; margin: -14px -18px 0; padding: 16px 18px; background: rgba(12,10,16,.62); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
#proto .msg { max-width: 76%; border-radius: 16px; padding: 10px 14px; font-size: 14px; line-height: 1.5; word-break: break-word; }
#proto .msg.me { align-self: flex-end; background: rgba(142,36,170,.4); border: 1.5px solid #cf86e6; }
#proto .msg.them { align-self: flex-start; background: rgba(24,21,30,.8); border: 1.5px solid rgba(255,255,255,.16); display: grid; gap: 6px; width: 60%; }
#proto .chatin { display: grid; grid-template-columns: 1fr 48px; gap: 8px; margin: -14px -18px -22px; padding: 12px 18px 22px; border-top: 1px solid rgba(255,255,255,.16); background: rgba(12,10,16,.5); }
#proto .chatin input { height: 48px; border-radius: 24px; padding: 0 16px; background: rgba(24,21,30,.8); border: 1.5px solid rgba(255,255,255,.2); color: #fff; font: 400 15px var(--body); outline: none; }
#proto .send { width: 48px; height: 48px; border-radius: 50%; background: rgba(142,36,170,.5); border: 1.5px solid #cf86e6; display: grid; place-items: center; cursor: pointer; }
#proto .glitch { animation: pglitch .9s steps(2) 2; }
@keyframes pglitch { 0% { transform: translate(0); filter: none; } 20% { transform: translate(-4px, 2px); filter: hue-rotate(40deg); } 40% { transform: translate(5px, -1px); } 60% { transform: translate(-2px, 0); filter: hue-rotate(-30deg) saturate(1.6); } 100% { transform: translate(0); } }
#proto .stripes { position: absolute; inset: 0; pointer-events: none; background: repeating-linear-gradient(0deg, transparent 0 28px, rgba(255,174,77,.55) 28px 34px, transparent 34px 90px); mix-blend-mode: screen; animation: pstripes .25s steps(3) infinite; }
@keyframes pstripes { 50% { transform: translateX(14px); } }
#proto .black { position: absolute; inset: 0; background: #000; }
#proto .blink { animation: pblink 1.6s infinite; }
@keyframes pblink { 50% { opacity: .35; } }
#proto .panel { display: grid; gap: 14px; }
#proto .panel h3 { font: 700 15px var(--display); margin: 0; }
#proto .panel .grp { display: flex; flex-wrap: wrap; gap: 8px; }
#proto .panel button { font: 700 13px var(--body); padding: 8px 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--ink); cursor: pointer; }
#proto .panel button:hover:not(:disabled), #proto .panel button:focus-visible { border-color: var(--lily); }
#proto .panel button:disabled { opacity: .4; cursor: default; }
#proto .panel button[aria-pressed="true"] { background: var(--lily-soft); border-color: var(--lily); color: var(--lily); }
#proto .panel .codes { font-size: 13px; color: var(--muted); display: grid; gap: 4px; }
#proto .panel .codes code { font: 700 13px 'IBM Plex Mono', monospace; color: var(--ink); background: var(--sys-soft); padding: 1px 6px; border-radius: 5px; }
#proto .panel .state { font-size: 13px; color: var(--muted); }
'''

HTML = '''<section id="proto">
<h2 class="grp-title">시험해 보기</h2>
<div class="proto-wrap">
  <div class="stage" id="pv-stage"><div class="ph pre" id="pv"><div class="bg" id="pv-bg"></div><div class="sbar" id="pv-sbar" aria-hidden="true"></div><div class="hbar"></div><div class="layer" id="pv-screen"></div><div class="pz hidden" id="pv-pz" role="button" tabindex="0" aria-label="계속"><span><svg width="30" height="34" viewBox="0 0 30 34"><path d="M4 2 L28 17 L4 32 Z" fill="#fff"/></svg></span></div></div></div>
  <div class="panel">
    <div><h3>진행 바꾸기</h3><p class="state" id="pv-state"></p></div>
    <div class="grp"><button type="button" id="pv-pause" aria-pressed="false">일시정지</button></div>
    <div class="grp" id="pv-ctl"></div>
    <div><h3>시험용 코드</h3></div>
    <div class="codes">
      <span><code>ABCD</code> 1부 힌트 (문제 3) · 힌트 3단계 + 정답</span>
      <span><code>KLMN</code> 2부 힌트 (문제 10)</span>
      <span><code>WXYZ</code> 문제 16 · 대기 연출 6단계 → 그 뒤 심장 소리 (같은 코드를 다시 넣으면 다음 단계)</span>
      <span><code>PQRS</code> 스토리 코드 → 보너스 패턴 (시험용 정답: 가운데 → 왼쪽 위 → 왼쪽 아래)</span>
      <span>그 밖의 코드는 오류로 처리돼요. 코드와 패턴 정답은 시험용이에요.</span>
    </div>
  </div>
</div>
</section>
'''

JS = r'''<script>
(() => {
const D = __DATA__, BG = __BG__, SH = __SHIELDS__, APPICON = __APPICON__;
const $ = s => document.getElementById(s);
const ph = $('pv'), scr = $('pv-screen'), bg = $('pv-bg');
const ICON = {
  bulb: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/></svg>',
  book: '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M4 5.5C6.5 4 9.5 4 12 5.8 14.5 4 17.5 4 20 5.5V19c-2.5-1.5-5.5-1.5-8 .3-2.5-1.8-5.5-1.8-8-.3z"/><path d="M12 5.8v13.5"/></svg>',
  sw: '<svg width="16" height="12" viewBox="0 0 16 12" fill="currentColor" aria-hidden="true"><path d="M8 11.5 10.4 8.6a3.5 3.5 0 0 0-4.8 0zM8 3.2a8.6 8.6 0 0 1 5.9 2.3l1.3-1.5A10.6 10.6 0 0 0 8 1.2 10.6 10.6 0 0 0 .8 4l1.3 1.5A8.6 8.6 0 0 1 8 3.2zm0 2.9a5.7 5.7 0 0 1 3.9 1.5L13.1 6A7.6 7.6 0 0 0 8 4.1 7.6 7.6 0 0 0 2.9 6l1.2 1.6A5.7 5.7 0 0 1 8 6.1z"/></svg>',
  swoff: '<svg width="16" height="12" viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M1.5 4.5a9.5 9.5 0 0 1 13 0M4 7a6 6 0 0 1 8 0" opacity=".45"/><path d="M2 1l12 10"/></svg>',
  bat: '<svg width="24" height="12" viewBox="0 0 24 12" aria-hidden="true"><rect x=".75" y=".75" width="19.5" height="10.5" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".6"/><rect x="2.5" y="2.5" width="13" height="7" rx="1.6" fill="currentColor"/><rect x="21.5" y="4" width="1.8" height="4" rx=".9" fill="currentColor" opacity=".6"/></svg>',
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  head: '<svg width="22" height="22" viewBox="-12 -12 24 24"><path d="M-7 -8 H7 A3 3 0 0 1 10 -5 V2 A3 3 0 0 1 7 5 H-2 L-7 9 V5 A3 3 0 0 1 -10 2 V-5 A3 3 0 0 1 -7 -8 Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="-4.5" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="0" cy="-1.5" r="1.4" fill="currentColor"/><circle cx="4.5" cy="-1.5" r="1.4" fill="currentColor"/></svg>',
  back: '<svg width="20" height="20" viewBox="0 0 20 20"><path d="M13 3 L6 10 L13 17" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  list: '<svg width="18" height="18" viewBox="0 0 18 18"><path d="M3 4 H15 M3 9 H15 M3 14 H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  pin: '<svg width="14" height="18" viewBox="-8 -9 16 18"><path d="M0 8 C-7 0 -6 -7 0 -7 C6 -7 7 0 0 8 Z" fill="#cf86e6"/><circle cx="0" cy="-1.5" r="2.4" fill="#211e26"/></svg>',
  x: '<svg width="16" height="16" viewBox="0 0 16 16"><path d="M3 3 L13 13 M13 3 L3 13" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
  chev: '<svg width="8" height="12" viewBox="0 0 8 12"><path d="M2 2 L6 6 L2 10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  heart: '<svg width="54" height="48" viewBox="0 0 54 48"><path d="M27 45 C10 32 2 23 2 13 C2 6 8 1 15 1 C20 1 24 4 27 8 C30 4 34 1 39 1 C46 1 52 6 52 13 C52 23 44 32 27 45 Z" fill="currentColor"/></svg>',
  send: '<svg width="20" height="20" viewBox="0 0 20 20"><path d="M3 10 H17 M11 4 L17 10 L11 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  ck: '<svg width="40" height="40" viewBox="0 0 40 40"><path d="M10 21 L17 28 L30 13" fill="none" stroke="#211e26" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  ckS: '<svg width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="#cf86e6"/><path d="M5.5 10.5 L8.5 13.5 L14.5 7" fill="none" stroke="#211e26" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  wifi: '<svg width="70" height="60" viewBox="-35 -30 70 60"><path d="M-22 -4 A31 31 0 0 1 22 -4" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/><path d="M-13 5 A18 18 0 0 1 13 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".35"/><circle cx="0" cy="14" r="3.5" fill="currentColor"/><path d="M-20 -18 L20 22" stroke="#ffae4d" stroke-width="3" stroke-linecap="round"/></svg>',
  sig: '<svg width="90" height="70" viewBox="-45 -50 90 70"><circle r="6" fill="#ffae4d"/>' + [16, 28, 40].map((r, i) => `<path d="M${-r} ${-r*.6} A${r} ${r} 0 0 1 ${r} ${-r*.6}" fill="none" stroke="currentColor" stroke-width="2.5" opacity="${1-i*.25}"/>`).join('') + '</svg>',
  note: '<svg width="40" height="44" viewBox="0 0 40 44"><path d="M14 36 V8 L34 2 V30" fill="none" stroke="currentColor" stroke-width="2.6"/><circle cx="9" cy="37" r="6" fill="#ffae4d"/><circle cx="29" cy="31" r="6" fill="#ffae4d"/></svg>',
};
const NM = { 알렉스: '#E53935', 오펠리아: '#FDD835', 노아: '#43A047', 에바: '#1E88E5', 릴리: '#8E24AA' };
const NMT = { 알렉스: '#E57373', 오펠리아: '#FFF176', 노아: '#81C784', 에바: '#64B5F6', 릴리: '#BA68C8' };  // 이름 글자색 (palette.py)
const tint = t => esc(t).replace(/(알렉스|오펠리아|노아|에바|릴리)(?=의 방)/g, n => `<span style="color:${NMT[n]}">${n}</span>`);
const bars = () => '<span class="ex">예시 문구</span>';  // 정해지지 않은 문구 자리
const esc = t => String(t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const wave = () => '<div class="wave">' + [10,22,36,18,44,28,40,24,34,16,26,12].map((h, i) => `<span style="height:${h}px;animation-delay:${i*0.07}s"></span>`).join('') + '</div>';

let S, timers = [];
let PAUSED = false;
function arm(t) { t.due = Date.now() + t.left; t.id = setTimeout(() => { timers = timers.filter(x => x !== t); t.fn(); }, t.left); }
function later(fn, ms) { const t = { fn, left: ms }; timers.push(t); arm(t); return t; }
function clearLater() { timers.forEach(t => clearTimeout(t.id)); timers = []; }
function setPause(on) {
  if (on === PAUSED) return; PAUSED = on;
  if (on) timers.forEach(t => { clearTimeout(t.id); t.left = Math.max(0, t.due - Date.now()); });
  else timers.forEach(arm);
  ph.classList.toggle('paused', on); $('pv-pz').classList.toggle('hidden', !on); panel();
}
function reset() {
  clearLater(); if (typeof PAUSED !== 'undefined' && PAUSED) setPause(false);
  S = { phase: 'pre', view: 'main', time: 6300, run: true, goal: 0, bia: 0, story1: false, code: '', open: {}, pct: null, showHints: false,
        chat: [], unread: 0, offline: false, celebrate: false, patPath: [], patBad: false, endStep: 0, introStep: 0, pending: false };
  render();
}
setInterval(() => { if (!PAUSED && S.run && S.time > 0 && !S.phase.startsWith('end')) { S.time--; if (!S.time) return timeUp(); const el = scr.querySelector('[data-time]'); if (el) el.textContent = fmt(); scr.querySelectorAll('[data-tm]').forEach(e => e.textContent = fmt()); } }, 1000);
const fmt = () => Math.floor(S.time / 3600) + ':' + String(Math.floor(S.time / 60) % 60).padStart(2, '0') + ':' + String(S.time % 60).padStart(2, '0');  // 105분 → 1:45:00
function timeUp() { clearLater(); S.phase = 'end_time'; S.offline = false; render(); }
const part = () => S.phase === 'p2' ? 2 : 1;

function setBg() {
  const k = S.phase === 'pre' ? 'bg_pre' : S.phase === 'p1' ? 'bg_part1' : S.phase === 'p2' ? 'bg_part2' : S.phase === 'end_planet' ? 'bg_end_planet' : null;
  bg.style.backgroundImage = k ? `url(${BG[k]})` : 'none';
  ph.className = 'ph ' + (S.phase === 'pre' ? 'pre' : S.phase === 'p2' ? 'p2' : 'p1') + (PAUSED ? ' paused' : '');
}
function dock(on = true) {  // 아래 독: 폰 앱 아이콘처럼
  const apps = [['codes', '힌트코드', ICON.bulb], ['story', '스토리코드', ICON.book], ['chat', '운영자 호출', ICON.head + (S.unread ? `<span class="badge">${S.unread}</span>` : '')]];
  return `<div class="dock glass${on ? '' : ' off'}">` + apps.map(([a, l, ic]) => `<div class="app"${on ? ` data-act="${a}" role="button" tabindex="0"` : ''}><i>${ic}</i>${l}</div>`).join('') + '</div>';
}
function sbar() {  // 상태 표시줄: 폰 시각 · 와이파이 · 배터리
  const d = new Date(), t = d.getHours() + ':' + String(d.getMinutes()).padStart(2, '0');
  $('pv-sbar').innerHTML = S.phase === 'end_escape' ? '' : `<span>${t}</span><span class="ic">${S.offline ? `<span class="off" aria-label="연결 끊김">${ICON.swoff}</span>` : ICON.sw}${ICON.bat}</span>`;
}
setInterval(() => S && sbar(), 20000);
function timerBox() {
  return `<div class="timer glass"><span data-time>${fmt()}</span></div>`;
}
function head(title) {
  return `<div class="head"><div class="back" data-act="home" role="button" aria-label="뒤로" tabindex="0">${ICON.back}</div><div class="ttl">${title}</div><div class="tm">${ICON.clock}<span data-tm>${fmt()}</span></div></div>`;
}

function vMain() {
  let g = '';
  if (S.phase === 'pre') {
    g = '';  // 스토리카드 1은 폰이 아니라 실물 카드
  } else if (S.phase === 'p1') {
    if (S.celebrate) {
      const [name] = D.goals[S.goal];
      g = `<div class="center"><div class="bigck">${ICON.ck}</div><div class="goal">${esc(name)}</div></div>`;
    } else {
      const [name, room] = D.goals[S.goal];
      g = `<div class="lbl">현재 목표</div><div class="goal">${esc(name)}</div><div class="room" data-act="map" role="button" tabindex="0" aria-haspopup="dialog">${ICON.pin}<span>${tint(room)}</span>${ICON.chev}</div>${bars(2)}`
        + `<div class="iconbtn" data-act="done" role="button" aria-label="완료 목표" tabindex="0">${ICON.list}</div>`;
    }
  } else if (S.phase === 'p2') {
    g = `<div class="bia"><div class="av">비아</div><div class="say">${tint(D.bia[S.bia])}</div></div>` + (S.biaTalk ? wave() : '');
  }
  return timerBox() + `<div class="guide glass">${g}</div>` + dock() + (S.map ? mapOv() : '');
}
// 지도 팝업: 갈 방만 그 사람 색으로 칠함. 바깥이나 X를 누르면 닫힘
function mapSvg(hi) {
  const { inset: i, rx } = D.map;
  const zones = D.map.rooms.map(([n, x, y, w, h]) => n === hi
    ? `<rect class="zone" x="${x + i}" y="${y + i}" width="${w - 2 * i}" height="${h - 2 * i}" rx="${rx}" style="fill:${NM[n]};fill-opacity:.42"/><text x="${x + w / 2}" y="${y + h / 2 + 5}" text-anchor="middle" style="fill:#fff;font:700 15px var(--body)">${n}</text>`
    : `<text x="${x + w / 2}" y="${y + h / 2 + 5}" text-anchor="middle" style="fill:rgba(242,238,246,.5);font:400 13px var(--body)">${n}</text>`).join('');
  return `<svg viewBox="-10 -10 304 196" role="img" aria-label="우주선 지도, ${hi}의 방 구역 표시"><path d="${D.map.hull}" style="fill:rgba(255,255,255,.05);stroke:rgba(255,255,255,.3);stroke-width:1.5"/>${zones}</svg>`;
}
function mapOv() {
  const n = D.goals[S.goal][1].replace(/의 방$/, '');
  return `<div class="mapov" data-act="mapx"><div class="mapbox glass" data-act="noop" role="dialog" aria-label="우주선 지도"><div class="mapx" data-act="mapx" role="button" tabindex="0" aria-label="지도 닫기">${ICON.x}</div>${mapSvg(n)}</div></div>`;
}

function vCodes() {
  const c = D.codes[S.code], p = c && c.part ? c.part : part();
  const opened = S.showHints && c && (c.kind === 'hint' || c.kind === 'voice');
  const pctBtn = S.pct != null
    ? `<div class="btn on${p}" data-act="pct" role="button" tabindex="0"><div class="pct">${S.pct}%<i><b style="width:${S.pct}%"></b></i></div></div>`
    : '<div class="btn" data-act="pct" role="button" tabindex="0">진행도</div>';
  let body = '';
  if (opened) {
    const st = S.open[S.code] || 0;
    if (c.kind === 'hint') {
      for (let i = 0; i < st; i++) body += `<div class="card h${p}"><span class="k ${p === 2 ? 't-via' : 't-lily'}">힌트 ${i + 1}</span>${c.hints[i] ? esc(c.hints[i]) : bars(2)}</div>`;
      if (st < c.hints.length) body += `<div class="btn next${p}" data-act="next" role="button" tabindex="0">다음 힌트</div>`;
      else if (!S.ans) body += '<div class="btn ans" data-act="ans" role="button" tabindex="0">정답 보기</div>';
      else body += `<div class="card ansc"><span class="k">정답 보기</span><span class="v">${c.answer ? esc(c.answer) : bars(1)}</span></div>`;
    } else if (c.kind === 'voice') {
      const n = c.steps.length, i = Math.min(st, n + 1) - 1;  // i === n: 6단계 뒤, 심장 소리만 반복
      const SPK = Object.assign({ 비아: '#FB8C00' }, NM);
      const inner = i < n
        ? c.steps[i].map(([who, t]) => `<div class="vline"><span class="spk"><i style="background:${SPK[who]}"></i>${esc(who)}</span><span>${esc(t)}</span></div>`).join('') + wave()
        : `<div class="center" style="padding:22px 0"><span class="heart" aria-label="심장 소리">${ICON.heart}</span></div>`;
      body += `<div class="card h2" style="gap:12px">${inner}<div class="vdots">${c.steps.map((_, k) => `<span style="background:${k <= i ? '#ffae4d' : 'rgba(255,255,255,.2)'}"></span>`).join('')}</div></div>`;
    }
  }
  if (S.mode === 'story') return head('스토리코드')
    + `<div class="srow"><input class="input" id="pv-in" value="${esc(S.code)}" maxlength="8" autocomplete="off" spellcheck="false" aria-label="스토리코드"><div class="btn" data-act="hint" role="button" tabindex="0" aria-label="확인">${ICON.send}</div></div>`;
  return head('힌트코드')
    + `<input class="input" id="pv-in" value="${esc(S.code)}" maxlength="8" autocomplete="off" spellcheck="false" aria-label="힌트코드">`
    + `<div class="row"><div class="btn${opened ? ' on' + p : ''}" data-act="hint" role="button" tabindex="0">힌트 보기</div>${pctBtn}</div>`
    + `<div class="scroll">${body}</div>`;
}

function vDone() {
  const rows = D.goals.slice(0, S.goal).map(([n]) => `<div class="glass" style="display:flex;gap:10px;align-items:center;padding:12px 14px;border-radius:10px">${ICON.ckS}<b style="font-size:14px">${esc(n)}</b></div>`).join('');
  return head('완료 목표') + `<div class="scroll">${rows}<div class="card h1"><span class="k t-lily">현재 목표</span><b style="font-size:15px">${esc(D.goals[S.goal][0])}</b></div></div>`;
}

const PTS = [[140, 140]].concat([-90, -30, 30, 90, 150, 210].map(a => [140 + 100 * Math.cos(a * Math.PI / 180), 140 + 100 * Math.sin(a * Math.PI / 180)]));
function patSvg() {
  const red = S.patBad, path = S.patPath, col = red ? '#E5484D' : '#ffae4d';
  const line = path.length > 1 ? `<path d="M${path.map(i => PTS[i].join(' ')).join(' L')}" fill="none" stroke="${col}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>` : '';
  const dots = PTS.map(([x, y], i) => `<circle cx="${x}" cy="${y}" r="${path.includes(i) ? 13 : 10}" fill="${path.includes(i) ? col : 'rgba(255,255,255,.22)'}"/>`).join('');
  return line + dots + `<path id="pv-drag" fill="none" stroke="${col}" stroke-width="6" stroke-linecap="round" opacity=".6"/>`;
}
function vPattern() { return head('') + `<div class="center"><div class="pat" id="pv-pat"><svg viewBox="0 0 280 280">${patSvg()}</svg></div></div>`; }
function vCard135() {
  const c = D.card135;
  return head('') + `<div class="scroll"><div class="story eva"><b style="font-size:16px">${esc(c.title)}</b><div class="by" style="text-align:left;margin:0 0 8px">${esc(c.by)}</div>${c.lines.map(esc).join('<br>')}</div></div>`;
}
function vChat() {
  const ms = S.chat.map(m => m.me ? `<div class="msg me">${esc(m.t)}</div>` : `<div class="msg them">${bars(2)}</div>`).join('');
  return `<div class="head chathead"><div class="back" data-act="home" role="button" aria-label="뒤로" tabindex="0">${ICON.back}</div><div class="ttl" style="display:grid;place-items:center">${ICON.head}</div><div class="tm">${ICON.clock}<span data-tm>${fmt()}</span></div></div>`
    + `<div class="msgs" id="pv-msgs" role="log" aria-label="운영자 채팅">${ms}</div><form class="chatin" id="pv-chat"><input id="pv-chatin" aria-label="운영자에게 보낼 말" autocomplete="off"><button class="send" type="submit" aria-label="보내기" style="color:#fff">${ICON.send}</button></form>`;
}
function vSafe() {  // 방패가 커지며 나타나고 아래 로딩 막대
  return `<div class="center full1" style="margin:-34px -18px -22px;padding:0 18px"><div class="sv zoom"><div class="sv-in">${SH}</div></div>`
    + '<b class="sf-t" style="font-size:18px">안전 모드 감지</b><div class="load go sf-t" style="--d:3s"><b></b></div></div>';
}
function vIntro() {
  if (S.introStep === 0) return vMain().replace('<div class="guide glass">', '<div class="guide glass glitch" style="border-color:#cf86e6">') + '<div class="stripes"></div>';
  const lines = D.bia_intro[S.introStep - 1], name = S.introStep === 1 ? '?' : '비아';
  return timerBox() + `<div class="guide glass" style="border-color:#ffae4d"><div class="bia"><div class="av" style="font-size:${name === '?' ? 18 : 12}px">${name}</div><div class="say">${lines.map(esc).join('<br>')}</div></div>${wave()}</div><div class="btn glass">힌트</div>`;
}
function vEnd() {
  if (S.phase === 'end_time') return `<div class="center"><b style="font:700 64px var(--display);color:#E5484D;font-variant-numeric:tabular-nums">0:00:00</b>${bars()}</div>`;
  if (S.phase === 'end_escape') return S.endStep === 0 ? '<div class="center glitch"><b style="font-size:20px">탈출 절차를 시—</b></div><div class="stripes" style="opacity:.4"></div>' : '<div class="black"></div>';
  const st = S.endStep;
  if (st === 0) return `<div class="center">${ICON.sig}<b style="font-size:17px">행성 프로젝트를 실행합니다.</b></div>`;
  if (st === 1) return `<div class="center"><div style="display:flex;gap:10px;align-items:flex-end">${ICON.sig}<span style="color:#fff">${ICON.note}</span></div><b style="font-size:17px">공개 구조 신호 송출을<br>시작합니다.</b></div>`;
  const L = ['공개 구조 신호 송출 중.', '좌표 전송 중.', '생체 반응 전송 중.', '여기는 알파. 여기는 알파…'];
  return `<div class="center" style="gap:14px">${ICON.sig}${L.slice(0, Math.min(st - 1, 4)).map((t, i) => `<b style="font-size:16px${i === 3 ? ';color:#ffb460' : ''}" class="${i === 3 ? 'blink' : ''}">${t}</b>`).join('')}</div>`;
}
function vOffline() {
  return timerBox() + `<div class="guide glass"><div class="center">${ICON.wifi}<p class="offmsg">연결이 끊겼습니다</p></div></div>` + dock(false);
}

function render() {
  S.stale = false;  // 화면에 남은 힌트·진행도가 지금 코드와 맞음
  if (S.view !== 'main' || S.phase !== 'p1' || S.celebrate || S.offline) S.map = false;  // 지도는 1부 목표 창 위에서만
  setBg();
  let h;
  if (S.phase.startsWith('end')) h = vEnd();
  else if (S.offline) h = vOffline();
  else h = ({ main: vMain, codes: vCodes, done: vDone, pattern: vPattern, card135: vCard135, chat: vChat, safe: vSafe, intro: vIntro })[S.view]();
  if (S.toast && S.view !== 'chat' && !S.phase.startsWith('end')) h += `<div class="toast glass" data-act="chat" role="button" tabindex="0"><i>${ICON.head}</i><div><b>운영자 호출</b>${bars()}</div></div>`;
  scr.innerHTML = h; sbar();
  const inp = $('pv-in'); if (inp && S.view === 'codes') { inp.oninput = () => { S.code = inp.value.toUpperCase().replace(/[^A-Z0-9]/g, ''); inp.value = S.code; S.stale = S.stale || S.showHints || S.pct != null; S.pct = null; S.showHints = false; S.ans = false; }; }
  const f = $('pv-chat'); if (f) { f.onsubmit = e => { e.preventDefault(); const t = $('pv-chatin').value.trim(); if (!t) return; S.chat.push({ me: true, t }); render(); $('pv-chatin').focus(); later(() => reply(), 2200); }; const m = $('pv-msgs'); m.scrollTop = m.scrollHeight; }
  if (S.view === 'pattern' && !S.phase.startsWith('end') && !S.offline) bindPattern();
  panel();
}
function reply() { S.chat.push({ me: false }); if (S.view !== 'chat') { S.unread++; S.toast = true; later(() => { S.toast = false; render(); }, 3500); } render(); }

function check(code) {
  const c0 = D.codes[code], app = c0 && (S.mode === 'story') === (c0.kind === 'story');  // 힌트코드 앱은 힌트 코드만, 스토리코드 앱은 스토리 코드만
  const c = !app || ((c0.part === 2 || c0.kind === 'story') && S.phase !== 'p2') ? null : c0;  // 2부·스토리 코드는 비아 등장 후에만
  if (!c) {  // 없는 코드: 아무 반응 없음. 앞 코드의 힌트·진행도가 펼쳐져 있었다면 그것만 걷는다
    if (S.stale) { render(); const i = $('pv-in'); i.focus(); i.setSelectionRange(i.value.length, i.value.length); }
    return null;
  }
  return c;
}
scr.addEventListener('click', e => {
  const t = e.target.closest('[data-act]'); if (!t) return;
  act(t.dataset.act);
});
scr.addEventListener('keydown', e => { if (e.key === 'Escape' && S.map) { act('mapx'); return; } if ((e.key === 'Enter' || e.key === ' ') && e.target.dataset && e.target.dataset.act) { e.preventDefault(); act(e.target.dataset.act); } else if (e.key === 'Enter' && e.target.id === 'pv-in') act('hint'); });
function act(a) {
  if (a === 'noop') return;
  if (a === 'map') { if (S.phase === 'p1' && S.view === 'main' && !S.celebrate) { S.map = true; render(); scr.querySelector('.mapx').focus(); } return; }
  if (a === 'mapx') { S.map = false; render(); scr.querySelector('.room')?.focus(); return; }
  if (a === 'chat') { S.view = 'chat'; S.unread = 0; S.toast = false; render(); return; }
  if (a === 'home') { S.view = 'main'; S.patPath = []; render(); return; }
  if (a === 'story') { S.mode = 'story'; S.view = 'codes'; S.code = ''; S.pct = null; S.showHints = false; S.ans = false; render(); $('pv-in')?.focus(); return; }
  if (a === 'codes') { S.mode = 'hint'; S.view = 'codes'; S.code = ''; S.pct = null; S.showHints = false; S.ans = false; render(); $('pv-in')?.focus(); return; }
  if (a === 'done' && S.phase === 'p1') { S.view = 'done'; render(); return; }
  if (a === 'hint') {
    const c = check(S.code); if (!c) return;
    if (c.kind === 'story') { S.view = 'pattern'; S.patPath = []; S.patBad = false; render(); return; }
    if (c.kind === 'voice') S.open[S.code] = Math.min((S.open[S.code] || 0) + 1, c.steps.length + 1);  // 넣을 때마다 다음 단계, 끝나면 심장 소리
    else if (c.kind === 'hint') S.open[S.code] = Math.max(1, S.open[S.code] || 0);
    S.showHints = true; S.ans = (S.answered || {})[S.code] || false; render(); return;
  }
  if (a === 'next') { const c = D.codes[S.code]; S.open[S.code] = Math.min((S.open[S.code] || 0) + 1, c.hints.length); render(); return; }
  if (a === 'ans') { S.ans = true; (S.answered = S.answered || {})[S.code] = true; render(); return; }
  if (a === 'pct') { const c = check(S.code); if (!c) return; if (c.pct == null) { check('-'); return; } S.pct = c.pct; render(); return; }
}

function bindPattern() {
  const box = $('pv-pat'); if (!box) return;
  const svg = box.querySelector('svg'), drag = $('pv-drag');
  let down = false;
  const pt = e => { const r = svg.getBoundingClientRect(); return [(e.clientX - r.left) / r.width * 280, (e.clientY - r.top) / r.height * 280]; };
  const hit = ([x, y]) => PTS.findIndex(([px, py]) => Math.hypot(px - x, py - y) < 26);
  box.onpointerdown = e => { if (S.patBad) return; down = true; box.setPointerCapture(e.pointerId); S.patPath = []; const i = hit(pt(e)); if (i >= 0) { S.patPath = [i]; redraw(); } };
  box.onpointermove = e => {
    if (!down) return; const p = pt(e), i = hit(p);
    if (i >= 0 && !S.patPath.includes(i)) { S.patPath.push(i); redraw(); }
    const d = $('pv-drag'); if (d && S.patPath.length) { const [lx, ly] = PTS[S.patPath[S.patPath.length - 1]]; d.setAttribute('d', `M${lx} ${ly} L${p[0]} ${p[1]}`); }
  };
  box.onpointerup = () => {
    if (!down) return; down = false;
    if (!S.patPath.length) return;
    if (S.patPath.join() === D.pattern.join()) { S.view = 'card135'; render(); }
    else { S.patBad = true; redraw(); later(() => { S.patBad = false; S.patPath = []; render(); }, 900); }
  };
  function redraw() { svg.innerHTML = patSvg(); }  // 상자를 갈아 끼우지 않아야 드래그가 이어진다
}

// 진행 바꾸기 (시험용 조작판)
const CTL = [
  ['처음부터', () => true, () => reset()],
  ['안전 모드 가동', () => S.phase === 'pre' && S.view === 'main', () => { S.view = 'safe'; render();
    later(() => { S.phase = 'p1'; S.view = 'main'; render(); scr.classList.remove('enter'); void scr.offsetWidth; scr.classList.add('enter'); }, 3700); }],
  ['목표 완료', () => (S.phase === 'p1' && S.view === 'main' && !S.celebrate && S.goal < D.goals.length - 1) || (S.phase === 'p2' && S.view === 'main' && S.bia < D.bia.length - 1),
    () => { if (S.phase === 'p1') { S.celebrate = true; render(); later(() => { S.celebrate = false; S.goal++; render(); }, 1500); } else { S.bia++; S.biaTalk = true; render(); later(() => { S.biaTalk = false; render(); }, 2600); } }],
  ['2부로 · 비아 등장', () => S.phase === 'p1' && S.view === 'main', () => { S.view = 'intro'; S.introStep = 0; render(); later(() => { S.phase = 'p2'; S.introStep = 1; render(); }, 1900); later(() => { S.introStep = 2; render(); }, 1900 + 2600); later(() => { S.view = 'main'; S.biaTalk = true; render(); later(() => { S.biaTalk = false; render(); }, 2600); }, 1900 + 2600 + 3200); }],
  ['운영자 답장 보내기', () => !S.phase.startsWith('end'), () => reply()],
  ['연결 끊김', () => !S.phase.startsWith('end') && !S.offline, () => { S.offline = true; render(); }],
  ['다시 연결', () => S.offline, () => { S.offline = false; render(); }],
  ['타이머 −5분', () => S.run && !S.phase.startsWith('end'), () => { S.time = Math.max(0, S.time - 300); if (S.time) render(); else timeUp(); }],
  ['시간 종료', () => S.run && !S.phase.startsWith('end'), () => { S.time = 0; timeUp(); }],
  ['탈출 엔딩', () => S.phase === 'p2' && S.view === 'main', () => { S.phase = 'end_escape'; S.endStep = 0; render(); later(() => { S.endStep = 1; render(); }, 1800); }],
  ['행성 엔딩', () => S.phase === 'p2' && S.view === 'main', () => { S.phase = 'end_planet'; S.endStep = 0; render(); [2600, 5600, 6600, 7600, 8600].forEach((ms, i) => later(() => { S.endStep = i + 1; render(); }, ms)); }],
];
const ctl = $('pv-ctl');
CTL.forEach(([label, ok, fn], i) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = label; b.onclick = () => { if (ok()) fn(); }; ctl.append(b); });
$('pv-pause').onclick = () => setPause(!PAUSED);
$('pv-pz').onclick = () => setPause(false);
$('pv-pz').onkeydown = e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setPause(false); } };
function panel() {
  [...ctl.children].forEach((b, i) => b.disabled = PAUSED || !CTL[i][1]());
  const pb = $('pv-pause'); pb.textContent = PAUSED ? '계속' : '일시정지'; pb.setAttribute('aria-pressed', String(PAUSED));
  const ph = { pre: '안전 모드 이전', p1: '1부 · 릴리 안내', p2: '2부 · 비아 안내', end_escape: '탈출 엔딩', end_planet: '행성 엔딩', end_time: '시간 종료' }[S.phase];
  $('pv-state').textContent = '지금: ' + ph + (S.phase === 'p1' ? ` · 목표 ${S.goal + 1}/${D.goals.length}` : S.phase === 'p2' ? ` · 비아 안내 ${S.bia + 1}/${D.bia.length}` : '');
}
// 좁은 화면에서는 폰을 줄여 보이기
function fit() { const st = $('pv-stage'), w = Math.min(384, st.parentElement.clientWidth); const k = w / 384; ph.style.transform = `scale(${k})`; st.style.width = 384 * k + 'px'; st.style.height = 827 * k + 'px'; }
addEventListener('resize', fit); fit();
reset();
})();
</script>
'''
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from icon import inline
JS = JS.replace('__APPICON__', json.dumps(inline('pv-appicon', '100%'))).replace('__DATA__', json.dumps(DATA, ensure_ascii=False)).replace('__BG__', json.dumps(BG)).replace('__SHIELDS__', json.dumps(SHIELD, ensure_ascii=False))
OUT.write_text(json.dumps({'css': CSS, 'html': HTML, 'js': JS}, ensure_ascii=False), encoding='utf-8')
print('proto', len(JS) // 1024, 'KB js')
