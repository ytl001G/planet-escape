// 시제품 자동 시험: 버튼을 순서대로 눌러 보고 결과를 #testout에 적는다 (headless --virtual-time-budget로 실행)
(() => {
  const out = []; const log = (ok, m) => out.push((ok ? 'PASS ' : 'FAIL ') + m);
  addEventListener('error', e => out.push('ERROR ' + e.message));
  const scr = () => document.getElementById('pv-screen');
  const has = t => scr().textContent.includes(t);
  const ctl = label => [...document.querySelectorAll('#pv-ctl button')].find(b => b.textContent === label);
  const press = label => { const b = ctl(label); if (!b || b.disabled) { log(false, '조작판 버튼 못 누름: ' + label); return; } b.click(); if (label === '처음부터') document.querySelector('#pv-screen [data-act="start"]')?.click(); };  // 처음부터 → 시작 전 화면이니 Start까지
  const tap0 = act => { const el = scr().querySelector(`[data-act="${act}"]`); if (!el) { log(false, '화면 버튼 없음: ' + act); return; } el.click(); };
  // 힌트코드 앱 화면이 없어지고 메인 아래 입력 창 + 힌트 팝업이 됨: 예전 시험 동작을 새 화면에 맞춰 옮김
  const tap = act => {
    const q = a => scr().querySelector(`[data-act="${a}"]`);
    if (act === 'codes') { if (q('hpx')) q('hpx').click(); const i = document.getElementById('pv-in'); if (i && i.value) { i.value = ''; i.dispatchEvent(new Event('input')); } return; }  // 앱 열기 → 메인 입력 창을 비움
    if (act === 'hint') return tap0('bhint');                                   // 힌트 보기
    if (act === 'pct') return;                                                  // 진행도는 맞는 코드면 바로 보임
    if (act === 'home' && !q('home')) { if (q('hpx')) q('hpx').click(); return; } // 팝업 닫기 (채팅 · 패턴 화면은 진짜 뒤로)
    tap0(act);
  };
  const type = v => { const i = document.getElementById('pv-in'); i.value = v; i.dispatchEvent(new Event('input')); };
  const drag = idxs => {
    const box = document.getElementById('pv-pat'), svg = box.querySelector('svg'), r = svg.getBoundingClientRect();
    const P = [[140, 140]].concat([-90, -30, 30, 90, 150, 210].map(a => [140 + 100 * Math.cos(a * Math.PI / 180), 140 + 100 * Math.sin(a * Math.PI / 180)]));
    const at = i => ({ clientX: r.left + P[i][0] / 280 * r.width, clientY: r.top + P[i][1] / 280 * r.height, pointerId: 1, bubbles: true });
    box.setPointerCapture = () => {};
    box.dispatchEvent(new PointerEvent('pointerdown', at(idxs[0])));
    idxs.slice(1).forEach(i => box.dispatchEvent(new PointerEvent('pointermove', at(i))));
    box.dispatchEvent(new PointerEvent('pointerup', at(idxs[idxs.length - 1])));
  };
  const steps = [];
  const at = (ms, fn) => steps.push([ms, fn]);
  at(300, () => log(!!document.querySelector('#pv-sbar span') && !!scr().querySelector('.lb-chat') && !!scr().querySelector('.lb-code #pv-in') && !scr().querySelector('.dock') && !document.querySelector('.hbar'), '홈 화면: 상태 표시줄 · 채팅 칸 · 아래 힌트코드 입력 창 · 홈 바 없음'));
  at(305, () => log(!!scr().querySelector('.idle .timer [data-prog]'), '안전 모드 전에도 타이머 안 진행도'));
  at(300, () => log(window.__demo === true, 'Start 전: 0000 힌트 나옴'));
  at(301, () => { const s = document.getElementById('pv-screen'); log(!s.querySelector('[data-act="start"]') && !!s.querySelector('.idle [data-time]'), 'Start 누른 뒤: 시간 감'); });
  at(310, () => { tap('codes'); type('0000'); tap('hint'); log(!scr().querySelector('.card'), 'Start 뒤엔 0000 반응 없음'); tap('home');
    press('연결 끊김'); log(getComputedStyle(scr().querySelector('.timer .tp')).stroke === 'rgb(233, 230, 238)', '안전 모드 전 끊김: 흰 링'); press('다시 연결'); });
  at(302, () => log(!!scr().querySelector('.idle [data-time]') && !!scr().querySelector('.idle [data-ring]') && !scr().querySelector('.guide'), '안전 모드 전: 큰 링 타이머 · 안내 창 없음'));
  at(301, () => log(!scr().querySelector('.load') && !!scr().querySelector('[data-time]'), '켜지자마자 메인(이전) · 시작 화면 없음'));
  at(2000, () => { log(!!scr().querySelector('[data-time]'), '메인(이전) 타이머'); press('스토리카드 1 띄우기'); log(has('보안이 아니잖아?'), '스토리카드 1 문구'); });
  at(2600, () => { press('안전 모드 가동'); log(has('안전 모드 감지') && !!scr().querySelector('svg linearGradient'), '안전 모드 방패'); });
  at(7200, () => { log(has('알렉스의 승인 확보') && has('알렉스의 방'), '1부 첫 목표 · 장소'); log(document.getElementById('pv').className.includes('p1'), '1부 색'); });
  at(7290, () => { const r = scr().querySelector('.timer [data-ring]'); log(!!r && +r.getAttribute('stroke-dashoffset') > 0 && +r.getAttribute('stroke-dashoffset') < 100, '타이머 링: 남은 시간만큼'); });
  at(7300, () => { tap('codes'); log(!scr().querySelector('.kbd'), '코드 앱에 들어가면 키보드 안 뜸'); tap('kb'); log(!!scr().querySelector('.kbd') && scr().querySelectorAll('.kbd .key').length === 37, '입력 칸 누르면 키보드 (36키 + 지우기)');
    ['A', 'B', 'C', 'X'].forEach(k => tap('k:' + k)); tap('kdel'); tap('k:D'); log(document.getElementById('pv-in').value === 'ABCD', '키보드로 입력 · 지우기');
    tap('hint'); log(!scr().querySelector('.kbd') && scr().querySelectorAll('.card.h1').length === 1, '힌트 보기 → 키보드 내려감'); tap('kb'); log(!!scr().querySelector('.kbd'), '입력 칸 누르면 다시 올라옴'); tap('home'); });
  at(7330, () => { tap('codes'); const n = () => +(scr().querySelector('.lb-used')?.textContent.match(/\d+/) || [-1])[0]; const a = n(); type('ABCD'); tap('hint'); const b = n(); type('0000'); tap('hint'); log(a === 1 && b === 1 && n() === 1, '힌트 사용 횟수: ABCD 본 뒤 1회, 다시 봐도·가짜 코드도 그대로 (' + a + ',' + b + ',' + n() + ')'); tap('home'); });
  at(7335, () => { const g = scr().querySelector('.lb-goal');
    log(!!g && g.textContent.includes('알렉스의 승인 확보') && !!scr().querySelector('.lb-chat') && !!scr().querySelector('.lb .idle [data-time]') && !!scr().querySelector('.lb-code #pv-in'), '배치 시안 B: 목표 오른쪽 위 · 채팅 왼쪽 위 · 타이머 가운데 · 아래 힌트코드 입력 창');
    tap('kb'); log(!!scr().querySelector('.kbd'), '시안 B: 입력 창 누르면 키보드'); for (let k = 0; k < 8; k++) tap('kdel'); 'ABC'.split('').forEach(k => tap('k:' + k)); 
    tap('k:D'); { const i = document.getElementById('pv-in'); log(document.activeElement === i && i.selectionStart === i.value.length, '시안 B: 치는 동안 커서가 글자 끝'); } log(!scr().querySelector('.lb-code .pct'), '입력 창엔 진행도 없음 (타이머 안으로)');
    tap('bhint'); const nx = () => scr().querySelector('.hpop [data-act="next"],.hpop [data-act="ans"]')?.textContent;
    log(!!scr().querySelector('.hpop .card') && !!scr().querySelector('.lb-goal') && nx() === '다음' && scr().querySelector('[data-act="bhint"]').textContent === '힌트 보기', '시안 B: 힌트 보기 → 힌트 팝업 (힌트 1 · 버튼 다음)'); log(/힌트 사용 1회/.test(scr().querySelector('.lb-used').textContent), '시안 B: 입력 창 위 힌트 사용 횟수');
    tap('hpx'); log(!scr().querySelector('.hpop'), '시안 B: 팝업 닫힘'); tap('kb'); for (let k = 0; k < 4; k++) tap('kdel'); scr().querySelector('.timer').click(); scr().querySelector('.lb-goal .goal').click(); log(!!scr().querySelector('.mapov'), '시안 B: 목표 칸 아무 데나 누르면 지도'); tap('mapx'); });
  at(7340, () => { tap('codes'); type('0000'); tap('hint'); log(!scr().querySelector('.card'), '1부: 0000 반응 없음'); tap('home'); });
  at(7350, () => { tap('codes'); tap('kb'); scr().querySelector('.timer').click(); log(!scr().querySelector('.kbd'), '코드 키보드: 바깥 누르면 내려감');
    tap('kb'); tap('k:Z'); log(!!scr().querySelector('.kbd'), '키보드 누르는 동안은 그대로'); tap('kdel'); tap('home');
    tap('chat'); tap('ckb'); scr().querySelector('.head .ttl').click(); log(!scr().querySelector('.kbd'), '한글 키보드: 바깥 누르면 내려감'); tap('home'); });
  at(7400, () => { tap('codes'); type('ABCD'); tap('hint'); log(scr().querySelectorAll('.card.h1').length === 1, '힌트 1 열림'); tap('next'); tap('next');
    log(scr().querySelectorAll('.card.h1').length === 3 && !scr().querySelector('[data-act="next"]'), '힌트 3까지'); tap('ans'); log(has('끝없는탐구'), '정답 보기'); });
  at(7600, () => { tap('home'); tap('codes'); type('ABCD'); tap('hint'); log(scr().querySelectorAll('.card.h1').length === 3, '본 힌트 다시 보기'); tap('home'); const pg = document.getElementById('pv-prog'); pg.value = 38; pg.dispatchEvent(new Event('input')); log(scr().querySelector('.timer [data-prog]')?.textContent === '진행도 38%', '진행도: 서버 값이 타이머 안에 바로'); pg.value = 0; pg.dispatchEvent(new Event('input')); });
  at(7800, () => { type('QRST'); tap('hint'); log(document.getElementById('pv-in').value === 'QRST' && !scr().querySelector('.card') && !has('38%'), '없는 코드: 앞 코드 힌트만 걷힘'); tap('home'); tap('codes'); type('QRST'); tap('hint'); tap('pct'); log(document.getElementById('pv-in').value === 'QRST' && !scr().querySelector('.card') && !scr().querySelector('.err'), '없는 코드: 아무 반응 없음'); });
  at(9400, () => { type('EFGH'); tap('hint'); log(!scr().querySelector('.card'), '힌트 없는 문제 코드는 없음'); tap('home'); log(!!scr().querySelector('.room span span[style*="--cht-alex"]') && has('알렉스의 방'), '방 이름: 알렉스만 빨강'); tap('codes'); });
  at(9600, () => { type('PQRS'); tap('hint'); log(!document.getElementById('pv-pat'), '1부: 스토리 코드 반응 없음'); type('KLMN'); tap('hint'); log(!scr().querySelector('.card'), '1부: 2부 코드 반응 없음'); tap('home'); });
  at(11000, () => { press('목표 완료'); log(!!scr().querySelector('.bigck'), '목표 완료 체크'); });
  at(12800, () => { log(has('오펠리아의 승인 확보'), '다음 목표'); });
  at(12900, () => { tap('chat'); log(!scr().querySelector('.kbd'), '채팅: 들어가면 키보드 없음'); tap('ckb'); log(!!scr().querySelector('.kbd.ck'), '입력 칸 누르면 한글 키보드');
    [...'ㄷㅗㅇㅗㅏㅈㅜㅅㅔㅇㅛ'].forEach(k => tap('ck:' + k)); log(document.getElementById('pv-chatin').value === '도와주세요', '한글 조합: 도와주세요');
    tap('ckdel'); tap('ck:ㅛ'); tap('ckshift'); log(!!scr().querySelector('[data-act="ck:ㅃ"]'), '시프트: 쌍자음'); tap('ckshift');
    tap('cklang'); log(!!scr().querySelector('[data-act="ck:q"]'), '한/영 전환'); tap('ck:?'); log(document.getElementById('pv-chatin').value === '도와주세요?', '영문 상태 문장부호');
    tap('cklang'); document.getElementById('pv-chat').requestSubmit(); log(has('도와주세요?') && document.getElementById('pv-chatin').value === '' && !!scr().querySelector('.kbd.ck'), '보낸 뒤 칸 비움 · 키보드 유지');
    tap('ckbx'); log(!scr().querySelector('.kbd'), '대화 쪽 누르면 키보드 내림'); tap('home'); });
  at(13000, () => { tap('chat'); const i = document.getElementById('pv-chatin'); i.value = '도와주세요'; document.getElementById('pv-chat').requestSubmit(); log(has('도와주세요'), '채팅 보내기'); tap('home'); });
  at(15600, () => { log(!!scr().querySelector('.badge'), '안 읽음 숫자'); tap('chat'); log(!!scr().querySelector('.msg.them') && !scr().querySelector('.badge'), '답장 읽음'); tap('home'); });
  at(15800, () => { press('연결 끊김'); log(!!scr().querySelector('.offov svg') && has('연결이 끊겼습니다') && !scr().querySelector('.load') && getComputedStyle(scr().querySelector('.timer')).zIndex === '5', '연결 끊김: 화면 전체를 덮고 타이머는 위에'); press('다시 연결'); log(has('오펠리아의 승인 확보'), '다시 연결'); });
  at(16000, () => { press('2부로 · 비아 등장'); log(!!scr().querySelector('.stripes'), '비아 끼어들기'); });
  at(18300, () => { log(!!scr().querySelector('.lb-goal .wave') && !scr().querySelector('.lb-goal .vplay') && scr().querySelector('.av').textContent === '?', '이름 ? · 음성 재생 중'); });
  at(21000, () => { log(!!scr().querySelector('.lb-goal .wave') && !has('그냥 비아라고') && scr().querySelector('.av').textContent === 'V', '비아 소개: 동그라미 V · 글 대신 음성 재생 중'); });
  at(24500, () => { log(!has('우선 알렉스의 방에') && document.getElementById('pv').className.includes('p2'), '2부 메인: 비아 글은 폰에 없음'); press('목표 완료'); log(!!scr().querySelector('.lb-goal .wave') && !scr().querySelector('.lb-goal .vplay'), '2부 다음 안내: V와 파형만'); });
  at(24700, () => { tap('codes'); type('WXYZ'); tap('hint'); log(!!scr().querySelector('.card .vplay') && !has('뭘 기다려'), '문제 16 1단계: 대사 글 없이 재생 아이콘'); tap('hint'); log(scr().querySelectorAll('.card .spk').length === 2, '문제 16 2단계: 말하는 사람 점 2개 (에바 + 비아)'); [3, 4, 5, 6].forEach(() => tap('hint')); log(!!scr().querySelector('.card .vplay') && !has('나 살고 싶어'), '문제 16 6단계'); log(scr().querySelectorAll('.vdots span').length === 6, '문제 16 점 6칸'); tap('hint'); log(!!scr().querySelector('.heart') && !has('나 살고 싶어'), '6단계 뒤 심장 소리'); tap('hint'); log(!!scr().querySelector('.heart'), '그 뒤에도 심장 소리 반복'); tap('home'); });
  at(24740, () => { tap('codes'); type('ABCD'); tap('hint'); log(!scr().querySelector('.card'), '2부: 1부 코드 반응 없음'); type('KLMN'); tap('hint'); log(!!scr().querySelector('.card'), '2부: 2부 코드 힌트'); tap('home'); });
  at(24745, () => { tap('kb'); for (let k = 0; k < 8; k++) tap('kdel'); 'KLMN'.split('').forEach(k => tap('k:' + k)); tap('bhint');
    log(!!scr().querySelector('.hpov.new'), '시안 B: 팝업 처음 뜰 때만 나타나는 효과'); tap('next'); log(!!scr().querySelector('.hpov') && !scr().querySelector('.hpov.new') && scr().querySelectorAll('.hpop .card').length === 2, '다음 눌러도 팝업이 새로 뜨지 않음');
    tap('hpx'); });
  at(24750, () => { log(!scr().querySelector('[data-act="story"]') && !!scr().querySelector('.lb-chat'), '2부: 스토리코드 앱 없이 같은 화면'); tap('codes'); type('PQRS'); tap('hint'); log(!!document.getElementById('pv-pat'), '힌트코드 앱에 스토리 코드 → 패턴 화면'); drag([0, 1, 2]); log(scr().textContent !== '' && !!scr().querySelector('circle[style*="--err"]'), '패턴 오답 빨강'); });
  at(25800, () => { log(!scr().querySelector('circle[style*="--err"]'), '패턴 초기화'); drag([0, 6, 5]); log(has('제온 추진 연료 전환 실험'), '패턴 정답 → 카드 13.5'); tap('home'); });
  at(26000, () => { press('행성 엔딩'); log(has('행성 프로젝트를 실행합니다.'), '행성 엔딩 1'); });
  at(35000, () => { log(has('여기는 알파. 여기는 알파…'), '행성 엔딩 반복 화면'); press('처음부터'); });
  at(37000, () => { press('안전 모드 가동'); });
  at(41000, () => { press('2부로 · 비아 등장'); });
  at(49500, () => { press('탈출 엔딩'); log(has('탈출 절차를 시—'), '탈출 엔딩 끊김'); });
  at(51700, () => { log(!!scr().querySelector('.black'), '탈출 엔딩 검은 화면'); press('처음부터'); });
  at(53800, () => { press('타이머 −5분'); press('시간 종료'); log(has('0:00:00') && has('예시 문구') && !scr().querySelector('[data-act="codes"]'), '시간 종료 화면'); });
  at(56500, () => { log(has('0:00:00') && document.getElementById('pv-state').textContent.includes('시간 종료'), '시간 종료 유지');
    const pre = document.createElement('pre'); pre.id = 'testout'; pre.textContent = out.join('\n'); document.body.prepend(pre); });
  steps.forEach(([ms, fn]) => setTimeout(() => { try { fn(); } catch (e) { out.push('EXC ' + e.message); } }, ms));
})();
