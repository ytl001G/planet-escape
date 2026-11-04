// 지도 팝업 시험: 열기 · 안쪽 눌러도 유지 · X · Esc · 바깥 · 목표 바뀌면 닫힘 · 다음 목표 색 · 2부엔 없음
addEventListener('load', () => {
  const out = [], log = (ok, m) => out.push((ok ? 'PASS ' : 'FAIL ') + m);
  const scr = document.getElementById('pv-screen'), q = s => scr.querySelector(s);
  const press = t => [...document.querySelectorAll('#pv-ctl button')].find(b => b.textContent === t).click();
  const open = () => !!q('.mapov');
  const hi = () => q('.mapbox > svg rect.zone');
  const steps = [
    [2200, () => press('안전 모드 가동')],
    [6500, () => { const r = q('.room[data-act="map"]'); log(!!r, '1부 목표 창 방 이름 누를 수 있음'); r.click();
      log(open(), '지도 열림'); log(hi() && /--ch-alex/.test(hi().getAttribute('style')), '알렉스 방 빨강'); log(document.activeElement === q('.mapx'), 'X에 초점');
      log(scr.querySelectorAll('.mapbox > svg path').length === 1 && scr.querySelectorAll('.mapbox > svg rect').length === 1 && scr.querySelectorAll('.mapbox > svg text').length === 5, '윤곽 하나 · 칠한 구역 하나 · 이름 5개 (벽·문 없음)'); q('.mapbox > svg').dispatchEvent(new MouseEvent('click', { bubbles: true })); log(open(), '지도 안쪽 눌러도 유지'); q('.mapx').click(); }],
    [6700, () => { log(!open(), 'X로 닫힘'); log(document.activeElement === q('.room'), '닫으면 방 이름으로 초점');
      q('.room').click(); q('.mapx').dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); }],
    [6900, () => { log(!open(), 'Esc로 닫힘'); q('.room').click(); q('.mapov').click(); }],
    [7100, () => { log(!open(), '바깥 눌러 닫힘'); q('.room').click(); press('목표 완료'); log(!open(), '목표 완료 연출 때 닫힘'); }],
    [9200, () => { log(!open(), '다음 목표에서도 닫힌 채'); q('.room').click(); log(hi() && /--ch-ophelia/.test(hi().getAttribute('style')), '오펠리아 방 노랑'); q('.mapx').click(); press('2부로 · 비아 등장'); }],
    [19000, () => { log(!q('.room[data-act]') && !open(), '2부에는 지도 버튼 없음');
      const pre = document.createElement('pre'); pre.id = 'testout'; pre.textContent = out.join('\n'); document.body.prepend(pre); }],
  ];
  steps.forEach(([ms, f]) => setTimeout(() => { try { f(); } catch (e) { out.push('EXC ' + e.message); } }, ms));
});
