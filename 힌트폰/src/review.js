(() => {
  const out = [], errs = [];
  addEventListener('error', e => errs.push(e.message));
  const scr = () => document.getElementById('pv-screen');
  const ctl = () => [...document.querySelectorAll('#pv-ctl button')];
  const press = t => { const b = ctl().find(b => b.textContent === t); if (b) b.click(); return !!b; };
  const tap = a => { const e = scr().querySelector(`[data-act="${a}"]`); if (e) e.click(); return !!e; };
  function check(tag) {
    const S = scr(), r = S.getBoundingClientRect(), bad = [];
    S.querySelectorAll('*').forEach(e => {
      const b = e.getBoundingClientRect(); if (!b.width || !b.height) return;
      const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none') return;
      if (e.closest('.scroll,.msgs')) return;
      if (b.right > r.right + 1 || b.left < r.left - 1 || b.bottom > r.bottom + 1) bad.push((e.className && e.className.baseVal === undefined ? e.className : e.tagName) + ' ' + (e.textContent || '').trim().slice(0, 20));
      if (e.children.length === 0 && e.scrollWidth > e.clientWidth + 2 && cs.overflow !== 'visible') bad.push('clip:' + (e.textContent || '').trim().slice(0, 20));
    });
    const t = S.innerText;
    if (/[12]부/.test(t)) bad.push('부 표기: ' + t.match(/.{0,10}[12]부.{0,10}/)[0]);
    out.push(`${tag}: ${bad.length ? 'ISSUE ' + [...new Set(bad)].slice(0, 5).join(' / ') : 'ok'}`);
  }
  const steps = [
    [500, () => { out.push('CONTROLS: ' + ctl().map(b => b.textContent).join(' | ')); check('홈(안전 모드 전)'); }],
    [800, () => { tap('codes'); check('힌트코드 앱'); tap('kb'); check('코드 키보드'); tap('home'); }],
    [1100, () => { tap('chat'); check('채팅'); tap('ckb'); check('한글 키보드'); tap('home'); }],
    [1400, () => press('안전 모드 가동')],
    [2000, () => check('안전 모드 알림')],
    [6500, () => check('메인(1부)')],
    [6800, () => { tap('codes'); ['A','B','C','D'].forEach(k => tap('k:' + k)); tap('hint'); check('힌트 1'); tap('next'); tap('next'); tap('next'); check('힌트 다 봄'); tap('ans'); check('정답'); tap('home'); }],
    [7200, () => { const m = scr().querySelector('[data-act="map"]'); if (m) { m.click(); check('지도 팝업'); } else out.push('지도: 버튼 못 찾음'); }],
    [7400, () => { const m = scr().querySelector('.mapov'); if (m) { const a = m.getBoundingClientRect(), b = scr().getBoundingClientRect(); out.push(`mapov rect ${a.left-b.left|0},${a.top-b.top|0},${a.right-b.right|0},${a.bottom-b.bottom|0}`); } document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'})); }],
    [7600, () => { press('목표 완료'); }],
    [8000, () => check('목표 완료')],
    [9000, () => { press('운영자 답장 보내기'); }],
    [9300, () => check('알림 배너')],
    [9500, () => { press('2부로 · 비아 등장'); }],
    [10500, () => check('비아 등장')],
    [14000, () => check('2부 메인')],
    [14200, () => { tap('codes'); check('힌트코드 앱 (2부)'); tap('kb'); check('스토리 키보드'); tap('home'); }],
    [14500, () => { press('연결 끊김'); }], [14800, () => { check('연결 끊김'); press('다시 연결'); }],
    [15200, () => { press('시간 종료'); }], [16000, () => check('시간 종료')],
    [16200, () => { press('처음부터'); }], [16600, () => { press('탈출 엔딩'); }], [19000, () => check('탈출 엔딩')],
    [19200, () => { press('처음부터'); }], [19600, () => { press('행성 엔딩'); }], [22000, () => check('행성 엔딩')],
  ];
  steps.forEach(([t, f]) => setTimeout(() => { try { f(); } catch (e) { errs.push(String(e)); } }, t));
  setTimeout(() => { const p = document.createElement('pre'); p.id = 'testout'; p.textContent = out.join('\n') + '\nERRORS: ' + (errs.join(' ; ') || 'none'); document.body.append(p); }, 22500);
})();
