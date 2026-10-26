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
header += '<g class="moving"><path class="comet" d="M 140 65 l 46 -9" stroke="url(#trail)" stroke-width="1.2" stroke-linecap="round"/></g>'
rng = Random(45841783)
for i in range(18):
    x,y = rng.randint(20,750),rng.randint(10,85)
    header += f'<circle class="spark" cx="{x}" cy="{y}" r="{rng.choice([.5,.7,1])}" fill="#c8efff" opacity=".2" style="animation-delay:-{i*.67}s"/>'
header_css = '''.spark{animation:twinkle 9s ease-in-out infinite}.comet{animation:comet 24s ease-in infinite}@keyframes twinkle{0%,100%{opacity:.12}50%{opacity:.55}}@keyframes comet{0%,75%{opacity:0;transform:translate(-120px,30px)}77%{opacity:.65}88%,100%{opacity:0;transform:translate(600px,-80px)}}'''
write('orbital-header.svg', svg(1200,400,'Sajad Janat — Think deeply. Build useful things.',header,'<linearGradient id="trail"><stop stop-color="#9cdeff" stop-opacity="0"/><stop offset="1" stop-color="#ecfbff"/></linearGradient>',header_css))

PROJECTS = [
    ('gitorbit','GitOrbit','Git workspaces, in one view.','Status, history, diffs, commits & sync.','TypeScript / Developer tools','#79d9ff'),
    ('taskorbit','TaskOrbit','A home for team projects.','Self-hosted. Persian & English.','TypeScript / Docker / Tauri','#ffc78b'),
    ('hotfi','Hotfi','Wi-Fi sharing, simplified.','Windows hotspot, QR & live traffic.','C# / .NET / WPF','#a5e7c7'),
    ('vue-neshan-maps','vue-neshan-maps','Maps that speak your language.','Traffic, clustering & heatmaps.','Vue / Nuxt / TypeScript','#c2cfff'),
]

def planet_art(key, x, y, radius, index, light_x=-.65, light_y=-.65):
    """Textured spheres with an atmosphere and a shared physical light direction."""
    palettes = [('#b3e6ff','#3e83ac','#12263b'),('#e8b488','#9b6545','#34271f'),('#c2dacb','#5b8675','#1d302d'),('#d1e4f3','#678da9','#1b2d43')]
    bright,mid,shade = palettes[index]
    hx,hy = 50+light_x*36,50+light_y*36
    definitions = f'''<radialGradient id="{key}-surface" cx="{hx}%" cy="{hy}%" r="85%"><stop stop-color="{bright}"/><stop offset=".42" stop-color="{mid}"/><stop offset="1" stop-color="{shade}"/></radialGradient>
<radialGradient id="{key}-night" cx="{hx}%" cy="{hy}%" r="82%"><stop offset=".25" stop-color="#02050b" stop-opacity="0"/><stop offset=".64" stop-color="#02050b" stop-opacity=".12"/><stop offset=".88" stop-color="#02050b" stop-opacity=".75"/><stop offset="1" stop-color="#02050b" stop-opacity=".98"/></radialGradient>
<clipPath id="{key}-clip"><circle r="{radius}"/></clipPath>
<filter id="{key}-grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{.055 if index!=2 else .026} {.07 if index!=2 else .22}" numOctaves="3" seed="{index+11}"/><feColorMatrix type="saturate" values="0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="{key}-halo"><feGaussianBlur stdDeviation="{radius*.055}"/></filter>'''
    body = f'<g transform="translate({x} {y})"><circle r="{radius+1}" fill="none" stroke="{bright}" stroke-width="1.8" opacity=".25" filter="url(#{key}-halo)"/><g clip-path="url(#{key}-clip)"><circle r="{radius}" fill="url(#{key}-surface)"/><circle r="{radius}" filter="url(#{key}-grain)" opacity=".36" style="mix-blend-mode:soft-light"/>'
    random = Random(700+index)
    if index == 1:
        for _ in range(22):
            cx,cy,cr = random.uniform(-.85,.85)*radius,random.uniform(-.85,.85)*radius,random.uniform(.035,.13)*radius
            body += f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{cr:.2f}" fill="#46352b" opacity=".38"/><path d="M {cx-cr:.2f} {cy:.2f} a {cr:.2f} {cr:.2f} 0 0 1 {cr*2:.2f} 0" fill="none" stroke="#f4d4b3" stroke-width=".65" opacity=".35"/>'
    elif index == 2:
        for j in range(9):
            yy=(-.85+j*.2)*radius
            body += f'<path d="M {-radius} {yy:.2f} Q 0 {yy+radius*.2:.2f} {radius} {yy-radius*.15:.2f}" fill="none" stroke="{bright if j%2 else shade}" stroke-width="{radius*.09}" opacity=".22"/>'
    else:
        for j in range(7):
            yy=(-.7+j*.23)*radius
            body += f'<path d="M {-radius} {yy:.2f} C {-radius*.2} {yy-radius*.45:.2f} {radius*.1} {yy+radius*.35:.2f} {radius} {yy-radius*.15:.2f}" fill="none" stroke="#e3f4ff" stroke-width="{radius*.06}" opacity=".24"/>'
    body += f'<circle r="{radius}" fill="url(#{key}-night)"/></g><circle r="{radius}" fill="none" stroke="{bright}" stroke-width=".7" opacity=".4"/></g>'
    return definitions,body

for theme in ['dark','light']:
    dark = theme == 'dark'
    bg,fg,muted,border = ('#101923','#ecf4fc','#a5b6c9','#2b3c50') if dark else ('#f5f8fd','#15283e','#51647b','#d1dce9')
    for index,(slug,name,line,detail,tech,accent) in enumerate(PROJECTS):
        ink = accent if dark else ['#096d9c','#9a520a','#176a4b','#5949a9'][index]
        defs,planet = planet_art('planet',493,54,29,index)
        body = f'<rect x=".5" y=".5" width="559" height="224" rx="14" fill="{bg}" stroke="{border}"/>'
        orbit = 'M 442 54 a 51 17 0 1 0 102 0 a 51 17 0 1 0 -102 0'
        body += f'<g transform="rotate(-28 493 54)"><path d="{orbit}" fill="none" stroke="{ink}" opacity=".22"/><circle class="moving" r="1.8" fill="{ink}"><animateMotion dur="24s" repeatCount="indefinite" path="{orbit}"/></circle></g>'+planet
        body += f'<g font-family="{FONT}"><text x="26" y="49" fill="{fg}" font-size="27" font-weight="650">{escape(name)}</text><text x="26" y="98" fill="{fg}" font-size="21" font-weight="600">{escape(line)}</text><text x="26" y="131" fill="{muted}" font-size="19">{escape(detail)}</text><path d="M 26 157 H 534" stroke="{border}"/><text x="26" y="192" fill="{ink}" font-size="17">{escape(tech)}</text><path d="M 508 183 h 18 m -6 -6 6 6 -6 6" fill="none" stroke="{ink}" stroke-width="2"/></g>'
        write(f'card-{slug}-{theme}.svg',svg(560,225,name+' — '+line+' '+detail+' '+tech,body,defs))

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
defs = '<radialGradient id="space"><stop stop-color="#172431"/><stop offset="1" stop-color="#080d14"/></radialGradient><radialGradient id="sun"><stop stop-color="#fff9ee"/><stop offset=".08" stop-color="#fff1d1" stop-opacity=".9"/><stop offset=".22" stop-color="#d7b481" stop-opacity=".32"/><stop offset="1" stop-color="#df9a55" stop-opacity="0"/></radialGradient><radialGradient id="nebula"><stop stop-color="#427390" stop-opacity=".13"/><stop offset="1" stop-color="#142537" stop-opacity="0"/></radialGradient><filter id="soft"><feGaussianBlur stdDeviation="1.6"/></filter>'
system_image=base64.b64encode((ASSETS/'project-system.png').read_bytes()).decode('ascii')
positions=[(252,160,65,180,48),(438,279,60,365,377),(849,150,65,952,48),(1000,282,62,945,377)]
defs += '<clipPath id="scene"><rect width="1200" height="410" rx="14"/></clipPath>'
defs += '<mask id="orbital-depth"><rect width="1200" height="410" fill="white"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="{r+3}" fill="black"/>' for x,y,r,_,_ in positions)+'</mask>'
body = f'<image width="1200" height="410" preserveAspectRatio="none" clip-path="url(#scene)" xlink:href="data:image/png;base64,{system_image}"/>'
body += '<g mask="url(#orbital-depth)">'
for i,(rx,ry) in enumerate([(155,37),(295,66),(420,96),(550,130)]):
    path = f'M {600-rx} 205 a {rx} {ry} 0 1 0 {rx*2} 0 a {rx} {ry} 0 1 0 {-rx*2} 0'
    body += f'<g transform="rotate(-5 600 205)"><path d="{path}" fill="none" stroke="#8eb9d7" opacity=".19"/><path class="track" d="{path}" fill="none" stroke="#9ce7ff" opacity=".16" stroke-dasharray="1 49" style="animation-duration:{60+i*13}s"/><g class="moving"><animateMotion dur="{30+i*11}s" begin="-{i*7}s" repeatCount="indefinite" rotate="auto" path="{path}"/><path d="M -11 0 H -3" stroke="#b2e7ff" stroke-width="1" opacity=".3"/><path d="M -2 -1.5 2 0 -2 1.5 Z" fill="#e4f4ff"/><path d="M -1 -4 V 4" stroke="#91b7d0" stroke-width="1"/></g></g>'
body += '</g><circle class="sun" cx="604" cy="190" r="40" fill="url(#sun)" opacity=".4"/>'
for i,((slug,name,line,detail,tech,accent),(x,y,r,tx,ty)) in enumerate(zip(PROJECTS,positions)):
    anchor='middle'
    desc=['Git workspaces','Teams & projects','Wi-Fi sharing','Vue & Nuxt maps'][i]
    start_y=y-r-8 if ty<y else y+r+8
    end_y=ty+28 if ty<y else ty-17
    body += f'<path d="M {x} {start_y} L {x} {end_y} H {tx}" fill="none" stroke="#91aec4" stroke-width=".8" opacity=".42"/>'
    body += f'<g font-family="{FONT}" text-anchor="{anchor}"><text x="{tx}" y="{ty}" fill="#f0f6fc" font-size="23" font-weight="600">{name}</text><text x="{tx}" y="{ty+23}" fill="#9eb6cb" font-size="16">{escape(desc)}</text></g>'
body += '<rect x=".5" y=".5" width="1199" height="409" rx="14" stroke="#273747" fill="none"/>'
css = '.star{animation:twinkle 11s ease-in-out infinite}.track{animation:scan 70s linear infinite}.sun{animation:breathe 12s ease-in-out infinite;transform-origin:600px 205px}@keyframes twinkle{0%,100%{opacity:.18}50%{opacity:.55}}@keyframes scan{to{stroke-dashoffset:-500}}@keyframes breathe{0%,100%{opacity:.86;transform:scale(.98)}50%{opacity:1;transform:scale(1.02)}}'
write('project-orbits-animated.svg',svg(1200,410,'Project constellation — GitOrbit, TaskOrbit, Hotfi, vue-neshan-maps. Animated orbiting satellites.',body,defs,css))
# A matching still scene for visitors who request reduced motion.
write('project-orbits.svg',svg(1200,410,'Project constellation — GitOrbit, TaskOrbit, Hotfi, vue-neshan-maps.',body,defs,'.moving{display:none}'))
print('Built animated header, animated constellation, 8 project cards, and 2 toolbox themes.')
