#!/usr/bin/env python3
"""Render compact, deterministic public architecture SVGs."""
import html,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COLORS={'neutral':('#263445','#9fb3c8'),'control':('#0f3b56','#45d0e8'),'build':('#4b3510','#f5b942'),'deploy':('#123f32','#4ee0a1'),'security':('#45203d','#f078c6')}
ICONS={'user':'<circle cx="0" cy="-7" r="6"/><path d="M-11 12c1-10 21-10 22 0"/>','repo':'<path d="M-12-12h18l6 6v18h-24z"/><path d="M6-12v6h6M-6-3h12M-6 3h12"/>','registry':'<path d="M-12-8l12-6 12 6-12 6zM-12-8v12l12 7 12-7V-8M0-2v13"/>','shield':'<path d="M0-14l12 5v8c0 8-5 13-12 16-7-3-12-8-12-16v-8z"/><path d="M-5 0l4 4 7-9"/>','compute':'<rect x="-14" y="-10" width="28" height="19" rx="2"/><path d="M-7 14h14M0 9v5M-8-4h16M-8 2h10"/>','package':'<path d="M-13-8l13-7 13 7v16L0 15-13 8zM-13-8L0 0l13-8M0 0v15"/>','key':'<circle cx="-6" cy="-3" r="7"/><path d="M0 2l13 13M7 9l4-4M10 12l4-4"/>','server':'<rect x="-14" y="-13" width="28" height="10" rx="2"/><rect x="-14" y="2" width="28" height="10" rx="2"/><circle cx="8" cy="-8" r="1"/><circle cx="8" cy="7" r="1"/>','cloud':'<path d="M-15 7h25c9 0 9-13 1-14-2-9-16-10-20-2-8-2-12 13-6 16z"/>','eye':'<path d="M-16 0c8-12 24-12 32 0-8 12-24 12-32 0z"/><circle cx="0" cy="0" r="5"/>','search':'<circle cx="-3" cy="-3" r="10"/><path d="M5 5l10 10"/>','document':'<path d="M-11-14h14l8 8v20h-22zM3-14v8h8M-5 1h10M-5 7h10"/>','bell':'<path d="M-11 7h22l-3-5v-6c0-12-16-12-16 0v6zM-4 11c2 5 6 5 8 0"/>','storage':'<ellipse cx="0" cy="-9" rx="13" ry="5"/><path d="M-13-9v18c0 7 26 7 26 0V-9M-13 0c0 7 26 7 26 0"/>','check':'<circle cx="0" cy="0" r="14"/><path d="M-7 0l5 6L8-7"/>'}
def esc(x): return html.escape(str(x))
def render(spec):
 width=1600;height=900;cols=spec['columns'];margin=45;gap=22;cw=(width-2*margin-gap*(len(cols)-1))/len(cols);top=130;pos={};p=[]
 p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">')
 p.append(f'<title>{esc(spec["title"])}</title><desc>{esc(spec["description"])}</desc>')
 p.append("""<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" fill="#8da6bf"/></marker><style>text{font-family:Inter,Arial,sans-serif}.title{font-size:30px;font-weight:700;fill:#f5f8fb}.meta{font-size:16px;fill:#9fb3c8}.head{font-size:20px;font-weight:700}.node{fill:#172331;stroke-width:2}.nt{font-size:18px;font-weight:700;fill:#f5f8fb}.ns{font-size:16px;fill:#b8c7d6}.flow{fill:none;stroke:#8da6bf;stroke-width:3;marker-end:url(#arrow)}.badge{fill:#0b1119;stroke:#8da6bf}.bid{font-size:15px;font-weight:700;fill:#fff;text-anchor:middle}.icon{fill:none;stroke:#eaf2f8;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}</style></defs>""")
 p.append(f'<rect width="{width}" height="{height}" fill="#0b1119"/><text x="45" y="55" class="title">{esc(spec["title"])}</text><text x="45" y="88" class="meta">PUBLIC REFERENCE | Logical roles only | Generated from versioned JSON</text>')
 for ci,col in enumerate(cols):
  x=margin+ci*(cw+gap);fill,stroke=COLORS[col['color']];p.append(f'<rect x="{x:.1f}" y="{top}" width="{cw:.1f}" height="630" rx="18" fill="{fill}" fill-opacity=".55" stroke="{stroke}" stroke-width="2"/>');p.append(f'<text x="{x+18:.1f}" y="{top+35}" class="head" fill="{stroke}">{esc(col["title"])}</text>')
  for ni,node in enumerate(col['nodes']):
   y=top+70+ni*165;nx=x+16;nw=cw-32;pos[node['id']]={'col':ci,'cx':nx+nw/2,'cy':y+56,'left':nx,'right':nx+nw,'top':y,'bottom':y+112};p.append(f'<rect class="node" x="{nx:.1f}" y="{y}" width="{nw:.1f}" height="112" rx="12" stroke="{stroke}"/>');p.append(f'<g class="icon" transform="translate({nx+34:.1f} {y+43})">{ICONS[node["icon"]]}</g>');p.append(f'<text x="{nx+62:.1f}" y="{y+41}" class="nt">{esc(node["title"])}</text><text x="{nx+62:.1f}" y="{y+71}" class="ns">{esc(node["subtitle"])}</text>')
 for src,dst,num in spec['flows']:
  a=pos[src];b=pos[dst]
  if abs(a['cx']-b['cx'])<1 and abs(a['cy']-b['cy'])<=165:
   down=b['cy']>a['cy'];sx=a['cx'];sy=a['bottom'] if down else a['top'];ex=b['cx'];ey=b['top'] if down else b['bottom'];bx=sx;by=(sy+ey)/2;path=f'M {sx:.1f} {sy:.1f} V {ey:.1f}'
  elif abs(a['cx']-b['cx'])<1:
   route_x=a['right']+10;sx=a['right'];sy=a['cy'];ex=b['right'];ey=b['cy'];bx=route_x;by=(sy+ey)/2;path=f'M {sx:.1f} {sy:.1f} H {route_x:.1f} V {ey:.1f} H {ex:.1f}'
  elif abs(a['cy']-b['cy'])<1 and abs(a['col']-b['col'])==1:
   right=b['cx']>a['cx'];sx=a['right'] if right else a['left'];ex=b['left'] if right else b['right'];sy=ey=a['cy'];bx=(sx+ex)/2;by=sy;path=f'M {sx:.1f} {sy:.1f} H {ex:.1f}'
  else:
   right=b['cx']>a['cx'];sx=a['right'] if right else a['left'];ex=b['left'] if right else b['right'];sy=a['cy'];ey=b['cy'];lane=765+int(num)*5;bx=(sx+ex)/2;by=lane;path=f'M {sx:.1f} {sy:.1f} V {lane:.1f} H {ex:.1f} V {ey:.1f}'
  p.append(f'<path class="flow" d="{path}"/><circle class="badge" cx="{bx:.1f}" cy="{by:.1f}" r="13"/><text class="bid" x="{bx:.1f}" y="{by+5:.1f}">{num}</text>')
 p.append('<text x="45" y="825" class="meta">Control intent: separate identities, deny by default, immutable promotion, exact evidence, fail-closed publication.</text><text x="45" y="858" class="meta">Excludes live addresses, hostnames, infrastructure IDs, credentials, and operational evidence.</text></svg>');return ''.join(p)+'\n'
def main():
 out=ROOT/'docs/architecture'
 for f in sorted((out/'specs').glob('*.json')):
  target=out/(f.stem+'.svg');target.write_text(render(json.loads(f.read_text())));print(target)
if __name__=='__main__': main()
