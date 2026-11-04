import pathlib,sys
p=pathlib.Path(sys.argv[1]); s=p.read_text(encoding='utf-8')
E=[]
def box(x,y,w,h,t,sub='',cls='n',tc=''):
    E.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{cls}"/>')
    if sub:
        E.append(f'<text x="{x+w/2}" y="{y+19}" text-anchor="middle" font-size="13" font-weight="700"{tc}>{t}</text>')
        E.append(f'<text x="{x+w/2}" y="{y+36}" text-anchor="middle" font-size="11" class="t-mute">{sub}</text>')
    else:
        E.append(f'<text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" font-size="13" font-weight="700"{tc}>{t}</text>')
def arrow(d,dash=False): E.append(f'<path d="{d}" class="ln{" dash" if dash else ""}" marker-end="url(#ah2)"/>')
def label(x,y,t,anchor='start',cls=''):
    c=f' class="{cls}"' if cls else ''
    E.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="11"{c}>{t}</text>')
phases=[('안전 모드 이전','soft','n',[('게임 시작','앱을 켜면 바로 메인 화면 · 1:45:00 타이머 시작 · 가이드 빈 칸'),('문제 0 이름 입력','메인 컴퓨터 · 힌트 3단계'),('스토리카드 1','실물 카드 · 폰에 안 뜸'),('문제 1 본인 확인 질문','메인 컴퓨터 · 힌트 없음')]),
 ('안전 모드 · 1부 릴리 안내','lily-band','lily',[('안전 모드 알림','방패가 커지며 등장 + 로딩 막대 · 폰 전체 화면'),('진행 가이드 시작','현재 목표 · 장소 · 할 일'),('알렉스의 승인 확보','문제 2 · 태블릿'),('오펠리아의 승인 확보','문제 3 · 태블릿'),('노아의 승인 확보','문제 4 · 태블릿'),('오펠리아 재방문','문제 5 · 오펠리아 태블릿'),('에바의 승인 확보','문제 6 · 태블릿 · 카드 6'),('릴리의 승인','문제 7 · 메인 컴퓨터 · 카드 7')]),
 ('전환부','soft','n',[('실행자 신원 확인','문제 8 · 메인 컴퓨터 · 카드 8'),('ALONE 입력 · 레버 하강','문제 9 · 메인 컴퓨터 · 카드 9'),('비아 등장','안내자 교체 · 보라 → 주황 · 대사 1001')]),
 ('2부 비아 안내','via-band','via',[('알렉스의 방 2차','문제 10 · 비아 대사 1008'),('오펠리아의 방 2차','문제 11 · 비아 대사 1137'),('노아의 방 2차','문제 12 · 비아 대사 1209'),('에바의 방 2차','문제 13 · 비아 대사 1322'),('릴리의 방 2차','문제 14 · 비아 대사 1432'),('LOVE 입력','문제 15 · 비아 정체 공개 · 카드 15'),('레버 선택','문제 16 · 카드 16')])]
edge_lbl={('문제 1 본인 확인 질문','안전 모드 알림'):'실패',('릴리의 승인','실행자 신원 확인'):'안전 모드 해제',('안전 모드 알림','진행 가이드 시작'):'로딩 끝나면 자동'}
X,W,H=60,260,46
y=20; prev=None; pos={}
for name,bcls,ncls,nodes in phases:
    top=y; y+=34
    for t,sub in nodes:
        if prev:
            py=prev; gap=y-(py+H); arrow(f'M{X+W/2} {py+H} V{y-2}')
            if (prevt,t) in edge_lbl: label(X+W/2+8,py+H+gap/2+4,edge_lbl[(prevt,t)])
        step=78 if (t=='안전 모드 알림') else 64
        box(X,y,W,H,t,sub,ncls); pos[t]=y; prev=y; prevt=t; y+=step if t=='안전 모드 알림' else 64
    E.insert(0,f'<rect x="10" y="{top}" width="360" height="{y-top-8}" rx="12" class="{bcls}"/><text x="24" y="{top+22}" font-size="12" font-weight="700" class="t-mute">{name}</text>')
    y+=12
py=prev; ey=y+10
box(20,ey,160,H,'탈출 엔딩','레버 아래 · 폰 꺼짐','n'); box(200,ey,160,H,'행성 엔딩','레버 위 · 송출 화면 반복','via')
arrow(f'M{X+W/2} {py+H} V{py+H+20} H100 V{ey-2}'); arrow(f'M{X+W/2} {py+H+20} H280 V{ey-2}')
total=ey+H+20
R=420; PW=440
def panel(y0,h,title):
    E.append(f'<rect x="{R-10}" y="{y0}" width="{PW}" height="{h}" rx="12" class="n dashbox"/>')
    E.append(f'<text x="{R+6}" y="{y0+24}" font-size="12" font-weight="700" class="t-mute">{title}</text>')
# 1) 힌트 버튼: 코드 판별을 부마다 나눠서
box(R+10,50,200,H,'메인 화면','타이머 · 진행 가이드','lily')
box(R+10,130,200,H,'코드 입력 화면','입력 칸 · 힌트 보기 · 진행도')
arrow(f'M{R+110} {50+H} V128'); label(R+118,118,'힌트코드 · 스토리코드 앱')
E.append(f'<polygon points="{R+110},206 {R+175},236 {R+110},266 {R+45},236" class="n"/>')
E.append(f'<text x="{R+110}" y="240" text-anchor="middle" font-size="12" font-weight="700">코드 판별</text>')
arrow(f'M{R+110} {130+H} V204'); label(R+118,194,'힌트 보기 또는 진행도')
label(R+186,232,'지금이 1부인지 2부인지도 같이 봄','start','t-mute')
E.append(f'<path d="M{R+45} 236 H{R+20} V{0}" class="ln"/>')  # 줄기 (끝은 아래에서 맞춤)
trunk_i=len(E)-1
def h4(cls,names=('힌트 1','힌트 2','힌트 3','정답')):
    return [(t,'',('inv' if t=='정답' else cls),47) for t in names]
ROWS=[('없는 코드','',[('반응 없음','펼쳐 둔 앞 코드 힌트만 걷힘','n',205)]),
      ('1부 코드','비아 등장 전 문제',h4('lily')),
      ('2부 코드 · 스토리 코드','비아 등장 전에 넣으면',[('반응 없음','1부에는 비아 힌트가 안 뜸','n',205)]),
      ('2부 코드','비아 등장 후 · 문제 10 ~ 15',h4('via')),
      ('문제 16 코드','비아 등장 후',[('대기 1 ~ 6','넣을 때마다 다음 단계','via',120),('심장 소리','6단계 뒤 반복','n',79)]),
      ('스토리 코드','비아 등장 후 · 보너스',[('패턴 입력','','n',95),('카드 13.5','패턴 정답','via',104)])]
ry0=300; step=60
for i,(c,sub,res) in enumerate(ROWS):
    ry=ry0+i*step
    arrow(f'M{R+20} {ry+H/2} H{R+28}')
    box(R+30,ry,160,H,c,sub)
    arrow(f'M{R+190} {ry+H/2} H{R+208}')
    x=R+210
    for t,s2,cls,w in res:
        box(x,ry,w,H,t,s2,cls,' class="t-inv"' if cls=='inv' else ''); x+=w+6
last=ry0+(len(ROWS)-1)*step+H/2
E[trunk_i]=f'<path d="M{R+45} 236 H{R+20} V{last}" class="ln"/>'
ny=ry0+len(ROWS)*step+16
for j,t in enumerate(['힌트는 코드 입력 화면 안, 버튼 줄 아래로 펼쳐짐 · 연 단계는 다시 볼 수 있음',
                      '다음 힌트 버튼으로 한 단계씩 · 정답 보기는 힌트를 다 본 뒤에만',
                      '진행도도 같은 판별 · 맞는 코드면 버튼 자리에 % (힌트를 펼쳐도 남음)',
                      '문제 16은 같은 코드를 넣을 때마다 레버 대기 연출 다음 단계 · 화자 여럿 · 6단계 뒤 심장 소리만',
                      '패턴 오답: 빨간 선 → 초기화',
                      '1부 코드를 2부에 넣으면 지금은 보라 힌트 그대로 (확인 필요)']):
    label(R+10,ny+j*18,t,'start','t-mute')
p1h=ny+5*18+18-20
panel(20,p1h,'힌트코드 · 스토리코드 앱 · 지금 부와 앱에 맞는 코드만 반응')
# 2) 어느 단계에서든
y2=20+p1h+20
panel(y2,224,'어느 단계에서든')
box(R+10,y2+40,200,H,'운영자 채팅','답장 오면 아이콘에 숫자')
box(R+10,y2+100,200,H,'연결 끊김','어느 화면에서든'); box(R+240,y2+100,180,H,'다시 연결','원래 화면으로')
arrow(f'M{R+210} {y2+123} H{R+238}')
box(R+10,y2+160,410,H,'시간 종료','타이머 0:00:00 → 전체 화면 · 문구와 그 뒤 진행 미정')
# 3) 1부에서만 (왼쪽 단계와 점선으로 이음)
y3=y2+244
panel(y3,224,'1부에서만')
for k,(t,s2,node) in enumerate([('목표 완료 화면','승인될 때마다 체크 표시 → 다음 목표','노아의 승인 확보'),
                                 ('완료 목표 다시 보기','목표 창 목록 버튼 → 끝낸 목표 체크 · 현재 목표','오펠리아 재방문')]):
    by=y3+40+k*60; box(R+10,by,410,H,t,s2,'lily')
    arrow(f'M{R+8} {by+H/2} H{390+(k*8)} V{pos[node]+H/2} H{X+W+2}',True)
box(R+10,y3+160,410,H,'지도 팝업','목표 창 방 이름 누름 → 갈 방 하이라이트 · X나 바깥 누르면 닫힘','lily')
total=max(total,y3+244)
svg=(f'<svg viewBox="0 0 870 {total}" role="img" aria-label="힌트폰 전체 순서도. 왼쪽 세로 줄은 게임 진행 순서로 안전 모드 이전, 안전 모드와 1부 릴리 안내, 전환부, 2부 비아 안내, 엔딩. 오른쪽 위는 힌트 버튼의 코드 판별로, 지금 부에 맞는 코드만 반응하고 1부에서 2부 코드나 스토리 코드를 넣으면 반응이 없다. 그 아래는 어느 단계에서든 쓰는 화면과 1부에서만 쓰는 화면.">\n'
 '      <defs><marker id="ah2" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" fill="currentColor"/></marker></defs>\n      '
 +'\n      '.join(E)+'\n    </svg>')
a=s.index('<svg',s.index('<p class="coltitle">순서도</p>')); b=s.index('</svg>',a)+6
s=s[:a]+svg+s[b:]
p.write_text(s,encoding='utf-8'); print('ok',total)
