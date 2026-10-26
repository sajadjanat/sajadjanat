"""Build self-contained GitHub profile SVGs. Run with Python 3, no dependencies."""
from pathlib import Path
import base64
import math
from random import Random
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT = 'Segoe UI,Arial,sans-serif'
REDUCE = '@media(prefers-reduced-motion:reduce){*{animation:none!important}.moving{display:none}}'

def svg(width, height, title, body, defs='', css=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><defs>{defs}</defs><style>{css}{REDUCE}</style>{body}</svg>'''

def write(name, content):
    (ASSETS/name).write_text(content, encoding='utf-8')

# The original raster banner is embedded unchanged; motion is an SVG overlay.
image = base64.b64encode((ASSETS/'orbital-banner.png').read_bytes()).decode('ascii')
header = f'<image width="1200" height="400" preserveAspectRatio="none" xlink:href="data:image/png;base64,{image}"/>'
header += '<g class="moving"><path class="comet" d="M 140 65 l 60 -12" stroke="url(#trail)" stroke-width="2" stroke-linecap="round"/><circle class="beacon" cx="1035" cy="62" r="3" fill="#c9f3ff"/><circle class="signal" cx="1035" cy="62" r="11" fill="none" stroke="#b0e7ff" stroke-width="1"/></g>'
rng = Random(45841783)
for i in range(26):
    x,y = rng.randint(20,1180),rng.randint(10,100)
    header += f'<circle class="spark" cx="{x}" cy="{y}" r="{rng.choice([.7,1,1.3])}" fill="#c8efff" opacity=".3" style="animation-delay:-{i*.37}s"/>'
header_css = '''.spark{animation:twinkle 5s ease-in-out infinite}.beacon{animation:twinkle 4s ease-in-out infinite}.signal{transform-origin:1035px 62px;animation:signal 4s ease-out infinite}.comet{animation:comet 12s ease-in infinite}@keyframes twinkle{0%,100%{opacity:.15}50%{opacity:.9}}@keyframes signal{0%{transform:scale(.4);opacity:.8}80%,100%{transform:scale(2.5);opacity:0}}@keyframes comet{0%,65%{opacity:0;transform:translate(-120px,30px)}68%{opacity:1}85%,100%{opacity:0;transform:translate(600px,-80px)}}'''
write('orbital-header.svg', svg(1200,400,'Sajad Janat — Think deeply. Build useful things.',header,'<linearGradient id="trail"><stop stop-color="#9cdeff" stop-opacity="0"/><stop offset="1" stop-color="#ecfbff"/></linearGradient>',header_css))

PROJECTS = [
    ('gitorbit','GitOrbit','Git workspaces, in one view.','Status, history, diffs, commits & sync.','TypeScript / Developer tools','#79d9ff'),
    ('taskorbit','TaskOrbit','A home for team projects.','Self-hosted. Persian & English.','TypeScript / Docker / Tauri','#ffc78b'),
    ('hotfi','Hotfi','Wi-Fi sharing, simplified.','Windows hotspot, QR & live traffic.','C# / .NET / WPF','#a5e7c7'),
    ('vue-neshan-maps','vue-neshan-maps','Maps that speak your language.','Traffic, clustering & heatmaps.','Vue / Nuxt / TypeScript','#c2cfff'),
]

for theme in ['dark','light']:
    dark = theme == 'dark'
    bg,fg,muted,border = ('#101923','#ecf4fc','#a5b6c9','#2b3c50') if dark else ('#f5f8fd','#15283e','#51647b','#d1dce9')
    for index,(slug,name,line,detail,tech,accent) in enumerate(PROJECTS):
        ink = accent if dark else ['#096d9c','#9a520a','#176a4b','#5949a9'][index]
        defs = f'<radialGradient id="planet" cx="28%" cy="25%"><stop stop-color="{accent}"/><stop offset=".5" stop-color="{ink}"/><stop offset="1" stop-color="#112338"/></radialGradient>'
        body = f'<rect x=".5" y=".5" width="559" height="224" rx="14" fill="{bg}" stroke="{border}"/>'
        body += f'<ellipse cx="485" cy="54" rx="51" ry="16" transform="rotate(-28 485 54)" fill="none" stroke="{ink}" opacity=".45"/><circle cx="485" cy="54" r="26" fill="url(#planet)"/>'
        body += f'<g class="moving" transform="translate(485 54)"><g class="orbit"><circle cx="44" cy="0" r="3" fill="{ink}"/></g></g>'
        body += f'<g font-family="{FONT}"><text x="26" y="49" fill="{fg}" font-size="27" font-weight="650">{escape(name)}</text><text x="26" y="98" fill="{fg}" font-size="21" font-weight="600">{escape(line)}</text><text x="26" y="131" fill="{muted}" font-size="19">{escape(detail)}</text><path d="M 26 157 H 534" stroke="{border}"/><text x="26" y="192" fill="{ink}" font-size="17">{escape(tech)}</text><path d="M 508 183 h 18 m -6 -6 6 6 -6 6" fill="none" stroke="{ink}" stroke-width="2"/></g>'
        write(f'card-{slug}-{theme}.svg',svg(560,225,name+' — '+line+' '+detail+' '+tech,body,defs,'.orbit{animation:orbit 16s linear infinite;transform-origin:0 0}@keyframes orbit{to{transform:rotate(360deg)}}'))

    # Compact native toolbox panel rather than relying on external badge servers.
    items = [('Web','TypeScript / Vue / Nuxt'),('Backend','PHP / Laravel / Python'),('Desktop','C# / .NET / WPF / Tauri'),('Delivery','Docker / Git')]
    body = f'<rect x=".5" y=".5" width="1199" height="189" rx="14" fill="{bg}" stroke="{border}"/>'
    for i,(label,tools) in enumerate(items):
        x = 28+i*300
        if i: body += f'<path d="M {x-15} 34 v 122" stroke="{border}"/>'
        body += f'<g font-family="{FONT}"><text x="{x}" y="62" font-size="23" fill="{fg}" font-weight="600">{label}</text>'
        # Two lines keep the labels readable at typical profile widths.
        split = tools.split(' / ')
        lines = [' / '.join(split[:2]),' / '.join(split[2:])]
        for j,line in enumerate(lines):
            body += f'<text x="{x}" y="{105+j*30}" font-size="21" fill="{muted}">{escape(line)}</text>'
        body += '</g>'
    write(f'toolbox-{theme}.svg',svg(1200,190,'Toolbox: TypeScript, Vue, Nuxt, PHP, Laravel, Python, C#, .NET, WPF, Tauri, Docker, Git',body))

# Orbital scene: labels stay still while small satellites travel along the paths.
rng = Random(45841783)
stars = ''.join(f'<circle class="star" cx="{rng.randint(12,1188)}" cy="{rng.randint(12,388)}" r="{rng.choice([.5,.7,1])}" fill="#dcecff" opacity=".35" style="animation-delay:-{i*.31}s"/>' for i in range(110))
defs = '<radialGradient id="space"><stop stop-color="#102539"/><stop offset="1" stop-color="#0d1117"/></radialGradient><radialGradient id="sun"><stop stop-color="#fff7df"/><stop offset=".25" stop-color="#ffdb9e"/><stop offset=".5" stop-color="#df9a55" stop-opacity=".6"/><stop offset="1" stop-color="#df9a55" stop-opacity="0"/></radialGradient>'
body = '<rect width="1200" height="410" rx="14" fill="url(#space)"/>'+stars
for i,(rx,ry) in enumerate([(155,37),(295,66),(420,96),(550,130)]):
    path = f'M {600-rx} 205 a {rx} {ry} 0 1 0 {rx*2} 0 a {rx} {ry} 0 1 0 {-rx*2} 0'
    body += f'<g transform="rotate(-5 600 205)"><path d="{path}" fill="none" stroke="#8eb9d7" opacity=".3"/><path class="track" d="{path}" fill="none" stroke="#9ce7ff" opacity=".45" stroke-dasharray="2 35" style="animation-duration:{30+i*9}s"/><circle class="moving" r="{3+i*.4}" fill="#c0f1ff"><animateMotion dur="{12+i*6}s" repeatCount="indefinite" path="{path}"/></circle></g>'
body += '<circle class="sun" cx="600" cy="205" r="91" fill="url(#sun)"/><ellipse cx="600" cy="205" rx="65" ry="9" fill="#ffdeb3" opacity=".25"/><circle cx="600" cy="205" r="12" fill="#fff0d2"/>'
positions=[(240,145,35,180,74),(420,290,40,365,367),(850,130,29,894,96),(1010,285,39,870,367)]
for i,((slug,name,line,detail,tech,accent),(x,y,r,tx,ty)) in enumerate(zip(PROJECTS,positions)):
    defs += f'<radialGradient id="p{i}" cx="28%" cy="24%" r="80%"><stop stop-color="{accent}"/><stop offset=".4" stop-color="{["#2467af","#9c522a","#347866","#4765ac"][i]}"/><stop offset="1" stop-color="#070d15"/></radialGradient>'
    anchor='start' if i==2 else 'middle'
    desc=['Git workspaces','Teams & projects','Wi-Fi sharing','Vue & Nuxt maps'][i]
    body += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#p{i})" stroke="{accent}" stroke-opacity=".6"/><path d="M {x-r*.65} {y-r*.15} Q {x} {y-r*.6} {x+r*.8} {y+r*.15}" stroke="{accent}" stroke-opacity=".15" stroke-width="4" fill="none"/>'
    body += f'<g font-family="{FONT}" text-anchor="{anchor}"><text x="{tx}" y="{ty}" fill="#f0f6fc" font-size="23" font-weight="600">{name}</text><text x="{tx}" y="{ty+23}" fill="#9eb6cb" font-size="16">{escape(desc)}</text></g>'
body += '<rect x=".5" y=".5" width="1199" height="409" rx="14" stroke="#273747" fill="none"/>'
css = '.star{animation:twinkle 7s ease-in-out infinite}.track{animation:scan 40s linear infinite}.sun{animation:breathe 8s ease-in-out infinite;transform-origin:600px 205px}@keyframes twinkle{0%,100%{opacity:.15}50%{opacity:.7}}@keyframes scan{to{stroke-dashoffset:-370}}@keyframes breathe{0%,100%{opacity:.75;transform:scale(.94)}50%{opacity:1;transform:scale(1.05)}}'
write('project-orbits-animated.svg',svg(1200,410,'Project constellation — GitOrbit, TaskOrbit, Hotfi, vue-neshan-maps. Animated orbiting satellites.',body,defs,css))
print('Built animated header, animated constellation, 8 project cards, and 2 toolbox themes.')
