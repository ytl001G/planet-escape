R=420; PW=440
def panel(y0,h,title):
    E.append(f'<rect x="{R-10}" y="{y0}" width="{PW}" height="{h}" rx="12" class="n dashbox"/>')
    E.append(f'<text x="{R+6}" y="{y0+24}" font-size="12" font-weight="700" class="t-mute">{title}</text>')
# 1) 힌트 버튼: 코드 판별을 부마다 나눠서
box(R+10,50,200,H,'메인 화면','타이머 · 진행 가이드','lily')
box(R+10,130,200,H,'코드 입력 화면','입력 칸 · 힌트 보기 · 진행도')
arrow(f'M{R+110} {50+H} V128'); label(R+118,118,'힌트 버튼')
E.append(f'<polygon points="{R+110},206 {R+175},236 {R+110},266 {R+45},236" class="n"/>')
E.append(f'<text x="{R+110}" y="240" text-anchor="middle" font-size="12" font-weight="700">코드 판별</text>')
arrow(f'M{R+110} {130+H} V204'); label(R+118,194,'힌트 보기 또는 진행도')
label(R+186,232,'지금이 1부인지 2부인지도 같이 봄','start','t-mute')
E.append(f'<path d="M{R+45} 236 H{R+20} V{0}" class="ln"/>')  # 줄기 (끝은 아래에서 맞춤)
trunk_i=len(E)-1
def h4(cls,names=('힌트 1','힌트 2','힌트 3','정답')):
    return [(t,'',('inv' if t=='정답' else cls),47) for t in names]
ROWS=[('없는 코드','',[('반응 없음','앞 코드 힌트가 펼쳐져 있었으면 그것만 걷힘','n',205)]),
      ('1부 코드','비아 등장 전 문제',h4('lily')),
      ('힌트 없는 코드','문제 1 · 13.5',[('안내만','힌트 자리에 안내 · 진행도는 그대로','n',205)]),
      ('2부 코드 · 스토리 코드','비아 등장 전에 넣으면',[('반응 없음','1부에는 비아 힌트가 안 뜸','n',205)]),
      ('2부 코드','비아 등장 후 · 문제 10 ~ 15',h4('via')),
      ('문제 16 코드','비아 등장 후',h4('via',('음성 1','음성 2','음성 3','음성 4'))),
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
                      '문제 16은 같은 코드를 다시 넣을 때마다 다음 음성 · 4단계 뒤에는 4단계 반복',
                      '패턴 오답: 빨간 선 → 초기화',
                      '1부 코드를 2부에 넣으면 지금은 보라 힌트 그대로 (확인 필요)']):
    label(R+10,ny+j*18,t,'start','t-mute')
p1h=ny+5*18+18-20
panel(20,p1h,'힌트 버튼 · 지금 부에 맞는 코드만 반응')
# 2) 어느 단계에서든
y2=20+p1h+20
panel(y2,224,'어느 단계에서든')
box(R+10,y2+40,200,H,'운영자 채팅','답장 오면 아이콘에 숫자')
box(R+10,y2+100,200,H,'연결 끊김','어느 화면에서든'); box(R+240,y2+100,180,H,'다시 연결','원래 화면으로')
arrow(f'M{R+210} {y2+123} H{R+238}')
box(R+10,y2+160,410,H,'시간 종료','타이머 00:00 → 전체 화면 · 문구와 그 뒤 진행 미정')
# 3) 1부에서만 (왼쪽 단계와 점선으로 이음)
y3=y2+244
panel(y3,164,'1부에서만')
for k,(t,s2,node) in enumerate([('목표 완료 화면','승인될 때마다 체크 표시 → 다음 목표','노아의 승인 확보'),
                                 ('완료 목표 다시 보기','목표 창 목록 버튼 → 끝낸 목표 체크 · 현재 목표','오펠리아 재방문')]):
    by=y3+40+k*60; box(R+10,by,410,H,t,s2,'lily')
    arrow(f'M{R+8} {by+H/2} H{390+(k*8)} V{pos[node]+H/2} H{X+W+2}',True)
