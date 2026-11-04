// 두벌식 한글 조합: 누른 낱자 배열 → 글자. 지우기는 마지막 낱자 하나를 빼고 다시 조합하면 된다
const HG = (() => {
  const CHO = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ', JUNG = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ';
  const JONG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
  const V2 = { 'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ': 'ㅝ', 'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ', 'ㅡㅣ': 'ㅢ' };
  const J2 = { 'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ', 'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ', 'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ' };
  const SPLIT = Object.fromEntries(Object.entries(J2).map(([k, v]) => [v, [k[0], k[1]]]));
  const isC = j => CHO.includes(j), isV = j => JUNG.includes(j);
  const out = s => s.cho && s.jung ? String.fromCharCode(0xAC00 + (CHO.indexOf(s.cho) * 21 + JUNG.indexOf(s.jung)) * 28 + JONG.indexOf(s.jong || '')) : (s.cho || s.jung || '');
  function run(seq) {  // 낱자만 이어진 한 덩어리
    let r = '', s = {};
    for (const j of seq) {
      if (isC(j)) {
        if (s.cho && s.jung && !s.jong && JONG.includes(j)) s.jong = j;
        else if (s.jong && J2[s.jong + j]) s.jong = J2[s.jong + j];
        else { r += out(s); s = { cho: j }; }
      } else {
        if (s.cho && !s.jung) s.jung = j;
        else if (s.jung && !s.jong && V2[s.jung + j] && (s.cho || true)) s.jung = V2[s.jung + j];
        else if (s.jong) { const [a, b] = SPLIT[s.jong] || [null, s.jong]; s.jong = a || ''; r += out(s); s = { cho: b, jung: j }; }
        else { r += out(s); s = { jung: j }; }
      }
    }
    return r + out(s);
  }
  // 낱자가 아닌 것(띄어쓰기 · 숫자 · 영문 · 문장부호)이 끼면 거기서 끊고 따로 조합
  function compose(tokens) {
    let r = '', seq = [];
    for (const t of tokens) { if (isC(t) || isV(t)) seq.push(t); else { r += run(seq) + t; seq = []; } }
    return r + run(seq);
  }
  return { compose };
})();
