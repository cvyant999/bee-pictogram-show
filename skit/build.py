import os,subprocess,html,sys,re,shutil
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H); sys.path.insert(0,H); from spec import C,PROPS
os.makedirs('img',exist_ok=True)
for c in C:
    i=c[0]
    for k,src,sz in (('p',f'pictograms/{i}.png','620x620'),('s',f'storyboards/{i}.png','1000x1000')):
        if os.path.exists(src) and os.path.getsize(src)>0:
            subprocess.run(['magick',src]+(['-fuzz','12%','-trim','+repage'] if k=='p' else [])+['-resize',sz,'-quality','82',f'img/{k}{i}.jpg'])
scenes={}
for c in C: scenes.setdefault(re.match(r'\d+',c[0]).group(),[]).append(c)
css="""@page{size:A4 landscape;margin:8mm}body{font-family:"Apple SD Gothic Neo",-apple-system,sans-serif;margin:0;color:#111}
.pg{page-break-after:always;height:192mm;display:flex;flex-direction:column}
h1{margin:0;font-size:18pt}.meta{color:#555;font-size:9.5pt;margin:1mm 0 2mm}
.row{display:flex;gap:3mm;flex:0 0 auto}.click{flex:1;border:1px solid #ddd;border-radius:3mm;padding:2mm;display:flex;flex-direction:column;gap:1.5mm}
.imgs{display:flex;gap:2mm;align-items:center}.pic{width:38mm;height:38mm;object-fit:contain}.sb{flex:1;height:42mm;object-fit:contain}
.one .pic{width:62mm;height:62mm}.one .sb{height:68mm}
.lbl{font-weight:700;font-size:10.5pt}.d{font-size:9.5pt}.sh{font-size:9pt;color:#6a1b9a}.chg{font-size:9pt;color:#c62828}
.ph{flex:1;height:40mm;border:2px dashed #bbb;color:#999;display:flex;align-items:center;justify-content:center;font-size:9pt}
.chk{font-size:11pt;margin:2mm 0}.chk span{margin-right:9mm}
.notes{flex:1;border:2px dashed #999;border-radius:3mm;padding:2mm 3mm;color:#999;font-size:9.5pt;background:repeating-linear-gradient(#fff,#fff 8mm,#eee 8mm,#eee 8.3mm)}
table{border-collapse:collapse;font-size:10pt}td,th{border:1px solid #ccc;padding:1.2mm 3mm}th{background:#eee}
.grid{display:grid;grid-template-columns:repeat(7,1fr);gap:1.5mm}.grid div{font-size:7pt;text-align:center}.grid img{width:100%}
ul{margin:1mm 0 0 5mm;padding:0;font-size:10pt}"""
CHG={"1":"투명한 물병 1개 + 잔 1개, 두 장면 사이에 스태프가 보라색 색소를 넣음","2":"아들: 해골 마스크, 서 있는 버전 (바닥 사용 X)","3":"서서 누운 연기 + 유령 그림, '베데스다' 물결 판","4":"바구니 거꾸로 들기 · 오병이어 쟁반 소품","5":"예수님 혼자 물 위 → 배 안의 제자들이 놀람 (베드로 빠지는 장면 삭제: 요한복음에 없음)","6":"손 대신 안대 (X X → O O)","8":"옷 속에 숨긴 뻥튀기를 꺼내 줌","9":"손전등 대신 빛 효과판 + 눈부신 액션","10":"2클릭으로 나눔: 양이 그려진 문 전지 → 예수님이 찢고 나옴","11":"가시덤불 삭제: 양머리 수건 씌워 주고 셋이 V 포즈","12":"흰 천에 싸인 예수님 + 휴지로 눈물 → 살아나신 예수님 (손바닥 점·옆구리 흉터)","13":"예수님 x3 + 선글라스 + '길'·'진리'·'생명' 종이","14":"포도 그림 들기","15":"스태프: 불 끄기 (가능하면)","16":"양: 양머리 수건, 물고기 소품"}
o=[f"<html><head><meta charset=utf-8><style>{css}</style></head><body>"]
o.append(f"<div class=pg><h1>BEE 탤런트쇼: 픽토그램 스킷 v7 (정솔 자매 피드백 반영)</h1><div class=meta>10월 24일(토) · {len(C)}클릭 · 배우 3명(예수님 가운데) + 스태프 1명</div>"
 "<ul><li>'찰칵' 소리마다 3명이 정지. 클릭 사이에는 스태프만 움직여 '기적'을 보여 줌.</li><li>빨간 글씨 = v5에서 바뀐 점. 스크린 위치를 생각해서 동선과 위치를 현장에서 정하기.</li><li>그림은 정솔 자매의 손그림 메모와 실제 소품 사진을 참고해 다시 그림.</li></ul>"
 "<h2 style='font-size:12.5pt;margin:2mm 0 1mm'>소품·의상</h2><table><tr><th>소품</th><th>장면</th><th>준비</th></tr>"+''.join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a,b,c in PROPS)+"</table></div>"
 "<div class=pg><h1>전체 흐름</h1><div class=meta>클릭 순서</div><div class=grid>"+''.join(f"<div><img src='img/p{c[0]}.jpg'><br>{n}. {html.escape(c[2])}</div>" for n,c in enumerate(C,1))+"</div></div>")
n=0
for sc,cl in scenes.items():
    title=re.sub(r'\s*\(\d\)$','',cl[0][2]); cls='row one' if len(cl)==1 else 'row'
    ch=CHG.get(str(int(sc)))
    o.append(f"<div class=pg><h1>{int(sc)}. {html.escape(title)}</h1><div class=meta>{len(cl)}클릭</div>"+(f"<div class=chg>변경: {html.escape(ch)}</div>" if ch else "")+f"<div class='{cls}'>")
    for c in cl:
        n+=1; i,en,t,pose,sh,_=c
        pic=f"<img class=pic src='img/p{i}.jpg'>" if os.path.exists(f'img/p{i}.jpg') else "<div class=ph>생성 실패</div>"
        sb=f"<img class=sb src='img/s{i}.jpg'>" if os.path.exists(f'img/s{i}.jpg') else "<div class=ph>생성 실패</div>"
        o.append(f"<div class=click><div class=lbl>클릭 {n}</div>"+(f"<div class=sh>▶ 스태프 (이 클릭 전): {html.escape(sh)}</div>" if sh else "")+f"<div class=imgs>{pic}{sb}</div><div class=d>{html.escape(pose)}</div></div>")
    o.append("</div><div class=chk><span>☐ 유지</span><span>☐ 수정</span><span>☐ 삭제</span></div><div class=notes>메모 / 스케치…</div></div>")
o.append("</body></html>"); open('review_v7.html','w').write(''.join(o))
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if os.path.exists(CH): subprocess.run([CH,"--headless=new","--disable-gpu","--no-pdf-header-footer","--user-data-dir=/tmp/hc_v7","--virtual-time-budget=20000",f"--print-to-pdf={H}/BEE-skit-v7-review.pdf",f"file://{H}/review_v7.html"],stderr=subprocess.DEVNULL)
# contact sheet
subprocess.run(['magick','montage']+[f'img/p{c[0]}.jpg' for c in C if os.path.exists(f'img/p{c[0]}.jpg')]+['-tile','7x','-geometry','300x300+8+8','-background','white','BEE-skit-v7-overview.jpg'])
# show site assets
W=os.path.join(H,'..','show'); os.makedirs(W+'/p',exist_ok=True)
for f in os.listdir(W+'/p'): os.remove(W+'/p/'+f)
for c in C:
    if os.path.exists(f'img/p{c[0]}.jpg'): shutil.copy(f'img/p{c[0]}.jpg',f'{W}/p/{c[0]}.jpg')
os.makedirs(W+'/s',exist_ok=True)
for c in C:
    if os.path.exists(f'img/s{c[0]}.jpg'): subprocess.run(['magick',f'img/s{c[0]}.jpg','-resize','900x900','-quality','78',f'{W}/s/{c[0]}.jpg'])
import json
sl=json.dumps([{"id":c[0],"t":c[2],"pose":c[3],"staff":c[4]} for c in C],ensure_ascii=False)
import time
open(W+'/index.html','w').write(open(W+'/template.html').read().replace('__SLIDES__',sl).replace('__VER__',str(int(time.time()))))
print(n,len(scenes))
