import json, math
CY='#00a6ca'; LC='#4fd1e8'; NV='#002f65'; BG='#011e3c'; MID='#16467e'; FILL='#0a2a52'
def svg(w,h,body,label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">{body}</svg>'
def grid(w,h,step=48,op=.05):
    s=''.join(f'<path d="M{x} 0V{h}"/>' for x in range(0,w+1,step))+''.join(f'<path d="M0 {y}H{w}"/>' for y in range(0,h+1,step))
    return f'<rect width="{w}" height="{h}" fill="{BG}"/><g stroke="#ffffff" stroke-opacity="{op}" stroke-width="1">{s}</g>'
def rack(x,y,w=170,h=300,units=8,stroke=LC,fill=FILL,acc=CY):
    led=acc
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    uh=(h-24)/units
    for i in range(units):
        uy=y+12+i*uh
        o+=f'<rect x="{x+12}" y="{uy+3}" width="{w-24}" height="{uh-6}" rx="3" fill="none" stroke="{stroke}" stroke-opacity=".55" stroke-width="1.5"/>'
        o+=f'<circle cx="{x+26}" cy="{uy+uh/2}" r="3.2" fill="{led if i%3!=1 else "#ffffff"}" fill-opacity="{1 if i%3!=1 else .7}"/>'
        o+=f'<circle cx="{x+38}" cy="{uy+uh/2}" r="3.2" fill="{led}" fill-opacity=".45"/>'
        for k in range(4):
            o+=f'<path d="M{x+w-80+k*14} {uy+uh/2-6}v12" stroke="{stroke}" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>'
    return o
def laptop(x,y,w=200,h=128,stroke=LC,fill=FILL,acc=CY):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    o+=f'<path d="M{x-24} {y+h+6}H{x+w+24}l-14 16H{x-10}z" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
    o+=f'<path d="M{x+18} {y+24}h{w*0.45}M{x+18} {y+40}h{w*0.3}" stroke="{stroke}" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>'
    bars=[0.35,0.55,0.45,0.75,0.6]
    for i,b in enumerate(bars):
        bh=(h-70)*b; o+=f'<rect x="{x+18+i*22}" y="{y+h-16-bh}" width="12" height="{bh}" rx="2" fill="{acc}" fill-opacity="{0.5+i*0.1}"/>'
    o+=f'<path d="M{x+w-70} {y+h-24}l14-18 14 8 22-28" fill="none" stroke="{acc}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    return o
def monitor(x,y,w=160,h=104,stroke=LC,fill=FILL,acc=CY):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    o+=f'<path d="M{x+w/2} {y+h}v22M{x+w/2-34} {y+h+24}h68" stroke="{stroke}" stroke-width="2" stroke-linecap="round"/>'
    o+=f'<rect x="{x+16}" y="{y+18}" width="{w*0.4}" height="{h-36}" rx="4" fill="{acc}" fill-opacity=".25"/>'
    o+=f'<path d="M{x+w*0.55} {y+26}h{w*0.3}M{x+w*0.55} {y+44}h{w*0.22}M{x+w*0.55} {y+62}h{w*0.28}" stroke="{stroke}" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>'
    return o
def switch(x,y,w=220,h=40,stroke=LC,fill=FILL,acc=CY):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    for i in range(8):
        o+=f'<rect x="{x+16+i*20}" y="{y+12}" width="12" height="16" rx="2" fill="none" stroke="{stroke}" stroke-opacity=".6" stroke-width="1.5"/>'
    o+=f'<circle cx="{x+w-22}" cy="{y+h/2}" r="4" fill="{acc}"/>'
    return o
def cloud(x,y,s=1,stroke=LC,fill=FILL):
    d=f'M{x+30*s} {y+70*s}a26 26 0 0 1 4-51.6A38 38 0 0 1 {x+108*s} {y+22*s}a30 30 0 0 1 {28*s} 48z'
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>'
def wire(d,stroke=CY,op=.85,dash=None):
    da=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-opacity="{op}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"{da}/>'
def node(x,y,r=5,c=CY):
    return f'<circle cx="{x}" cy="{y}" r="{r+5}" fill="{c}" fill-opacity=".18"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
logo=json.load(open('logo_dots.json'))
def ring(cx,cy,scale,op=1,cols=(CY,LC)):
    o=''
    for x,y,r,c in logo:
        col=cols[0] if c=='c' else cols[1]
        o+=f'<circle cx="{cx+(x-534)*scale:.1f}" cy="{cy+(y-501)*scale:.1f}" r="{r*scale:.1f}" fill="{col}" fill-opacity="{op}"/>'
    return o
out={}
# A: infrastructure banner
W,H=1440,520
b=grid(W,H)
b+=ring(1350,430,0.16,op=.35,cols=(CY,'#2a6bb0'))
b+=wire('M780 360H860')+wire('M1030 330H1080')+wire('M945 110V92a12 12 0 0 1 12-12H1160')+wire('M1190 300V262')+wire('M1300 320H1350V200a12 12 0 0 0-12-12H1334',op=.6,dash='4 8')
b+=wire('M610 360H700',op=.5,dash='4 8')
b+=cloud(1160,44,1.1)
b+=rack(860,110)+monitor(620,300)+switch(1080,300)+laptop(1110,128)
for p in [(860,360),(780,360),(1080,330),(945,92),(1160,80),(1190,282),(700,360)]: b+=node(*p,r=4)
out['banner-infrastruktur.svg']=svg(W,H,b,'Illustration: Server-Rack, Arbeitsplätze, Netzwerk und Cloud')
# B: world map banner
dots=json.load(open('dots.json'))
H2=520; b=grid(W,H2)
ox=(W-1200)/2
def proj(lon,lat): return ox+(lon+180)/360*1200, (76-lat)/132*520
mg=''
for px,py,lon,lat in dots:
    hi = (-12<=lon<=40 and 35<=lat<=71)
    mg+=f'<circle cx="{ox+px:.0f}" cy="{py:.0f}" r="{2.8 if hi else 2.3}" fill="{LC if hi else "#2a5a94"}" fill-opacity="{0.95 if hi else 0.75}"/>'
b+=mg
hub=proj(9,50)
for lon,lat in [(-95,40),(110,32),(138,-26),(-48,-15),(78,22)]:
    ex,ey=proj(lon,lat); mx=(hub[0]+ex)/2; my=min(hub[1],ey)-120
    b+=wire(f'M{hub[0]:.0f} {hub[1]:.0f}Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f}',stroke=CY,op=.8,dash='2 7')
    b+=node(round(ex),round(ey),r=4,c=CY)
b+=node(round(hub[0]),round(hub[1]),r=6,c=LC)
out['banner-welt.svg']=svg(W,H2,b,'Illustration: Weltkarte aus Punkten mit Verbindungslinien')
# C: network constellation from logo ring
H3=400; b=grid(W,H3)
cx,cy,sc=1080,200,0.3
pts=[(cx+(x-534)*sc, cy+(y-501)*sc) for x,y,r,c in logo]
ext=[(780,70),(820,330),(1380,60),(1360,340),(700,200),(1420,200)]
for i,(ex,ey) in enumerate(ext):
    tx,ty=min(pts,key=lambda p:(p[0]-ex)**2+(p[1]-ey)**2)
    b+=wire(f'M{ex} {ey}L{tx:.0f} {ty:.0f}',stroke=LC,op=.35)
    b+=node(ex,ey,r=4,c=CY if i%2 else LC)
b+=ring(cx,cy,sc,1,(CY,'#3d86d6'))
out['banner-netzwerk.svg']=svg(W,H3,b,'Illustration: ITCoreNet-Punktring als Netzwerk')
# D: tiles (light)
TW,TH=560,360
def tile(body,label):
    bg=f'<rect width="{TW}" height="{TH}" rx="16" fill="#f4f7fa"/>'
    g=''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{NV}" fill-opacity=".12"/>' for x in range(24,TW,24) for y in range(24,TH,24))
    return svg(TW,TH,bg+g+body,label)
L=dict(stroke=NV,fill='#ffffff',acc=CY)
# 01 consulting: board with roadmap
b=f'<rect x="120" y="60" width="320" height="220" rx="12" fill="#ffffff" stroke="{NV}" stroke-width="2.5"/>'
b+=f'<path d="M150 100h120M150 122h80" stroke="{NV}" stroke-opacity=".5" stroke-width="4" stroke-linecap="round"/>'
for i,hh in enumerate([40,62,52,86]):
    b+=f'<rect x="{310+i*28}" y="{170-hh}" width="16" height="{hh}" rx="3" fill="{CY}" fill-opacity="{0.45+i*0.15}"/>'
b+=f'<path d="M160 230H400" stroke="{NV}" stroke-opacity=".25" stroke-width="3" stroke-linecap="round"/>'
for i,c in enumerate([LC,CY,'#0a7fb0',NV]):
    b+=f'<circle cx="{170+i*74}" cy="230" r="10" fill="{c}"/>'
b+=f'<path d="M280 280v34M240 318h80" stroke="{NV}" stroke-width="2.5" stroke-linecap="round"/>'
out['leistung-01-beratung.svg']=tile(b,'Illustration: Roadmap mit Meilensteinen und Kennzahlen')
# 02 infrastructure
b=rack(110,40,150,270,7,**L)+switch(300,250,190,36,**L)+cloud(320,40,1.05,stroke=NV,fill='#ffffff')
b+=wire('M260 268H300',stroke=CY)+wire('M395 250V122',stroke=CY)+wire('M260 90H300a12 12 0 0 0 12-12',stroke=CY,op=.6,dash='4 7')
b+=node(300,268,4)+node(395,122,4)
out['leistung-02-infrastruktur.svg']=tile(b,'Illustration: Server-Rack, Netzwerk-Switch und Cloud')
# 03 hardware lifecycle
b=f'<circle cx="280" cy="180" r="140" fill="none" stroke="{CY}" stroke-width="2.5" stroke-dasharray="10 12"/>'
for ang in (20,140,260):
    a=math.radians(ang); x=280+140*math.cos(a); y=180+140*math.sin(a)
    t=a+math.pi/2; ax=math.cos(t); ay=math.sin(t)
    b+=f'<path d="M{x-ax*12-ay*8:.1f} {y-ay*12+ax*8:.1f}L{x:.1f} {y:.1f}L{x-ax*12+ay*8:.1f} {y-ay*12-ax*8:.1f}" fill="none" stroke="{CY}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
b+=monitor(150,110,150,96,**L)+laptop(300,150,130,84,**L)
out['leistung-03-hardware.svg']=tile(b,'Illustration: Arbeitsplatz-Hardware im Lebenszyklus')
# 04 managed services: gear with loop
def gear(cx,cy,r=52,teeth=8):
    pts=[]
    for i in range(teeth*2):
        a=math.pi*2*i/(teeth*2); rr=r if i%2==0 else r-12
        a1=a-math.pi/(teeth*2)*0.6; a2=a+math.pi/(teeth*2)*0.6
        pts+= [(cx+rr*math.cos(a1),cy+rr*math.sin(a1)),(cx+rr*math.cos(a2),cy+rr*math.sin(a2))]
    d='M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+'z'
    return f'<path d="{d}" fill="#ffffff" stroke="{NV}" stroke-width="2.5" stroke-linejoin="round"/><circle cx="{cx}" cy="{cy}" r="{r*0.38:.0f}" fill="none" stroke="{NV}" stroke-width="2.5"/>'
b=f'<path d="M150 180a130 130 0 0 1 222-92" fill="none" stroke="{CY}" stroke-width="3" stroke-linecap="round"/><path d="M372 88l2-26M372 88l-26-2" stroke="{CY}" stroke-width="3" stroke-linecap="round"/>'
b+=f'<path d="M410 180a130 130 0 0 1-222 92" fill="none" stroke="{NV}" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/><path d="M188 272l-2 26M188 272l26 2" stroke="{NV}" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>'
b+=gear(280,180)
b+=f'<circle cx="352" cy="118" r="22" fill="{CY}"/><path d="M341 118l8 8 14-16" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
out['leistung-04-managed-services.svg']=tile(b,'Illustration: laufende Betreuung als Kreislauf')
for k,v in out.items(): open('out/'+k,'w').write(v)
print({k:len(v)//1024 for k,v in out.items()})
