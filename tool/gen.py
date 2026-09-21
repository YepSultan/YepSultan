#!/usr/bin/env python3
"""Generates the animated SVGs for the GitHub profile README.

Run: python3 tool/gen.py   (writes into assets/)
Everything is self-contained SVG + CSS animation, because GitHub renders
README images through a proxy that strips scripts but keeps <style>.
"""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#08090C"
SURFACE = "#111318"
BORDER = "#232833"
TEXT = "#EDEFF4"
MUTED = "#959DAC"
FAINT = "#616A7B"
EMBER = "#FF6B35"
HOT = "#FFB061"
CORE = "#FFE9A8"
COOL = "#5B9BFF"
GOOD = "#4FC58B"
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)
    print("wrote", name, len(svg) // 1024, "KB")


def gear_path(cx, cy, r_out, r_in, teeth, hole):
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step
        for da, r in ((0.0, r_in), (0.12, r_out), (0.38, r_out), (0.5, r_in)):
            ang = a + da * step * 2 * 0.5 + (0 if da < 0.5 else 0)
            ang = a + da * step
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        pts.append((cx + r_in * math.cos(a + step), cy + r_in * math.sin(a + step)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    # hole, drawn counter-clockwise for evenodd
    d += (f" M{cx + hole},{cy} A{hole},{hole} 0 1,0 {cx - hole},{cy}"
          f" A{hole},{hole} 0 1,0 {cx + hole},{cy} Z")
    return d


def flame_path(cx, cy, w, h):
    l, t = cx - w / 2, cy - h / 2

    def P(fx, fy):
        return f"{l + fx * w:.1f},{t + fy * h:.1f}"

    return (f"M{P(.5, 0)} C{P(.62, .22)} {P(.95, .42)} {P(.92, .7)} "
            f"C{P(.9, .9)} {P(.72, 1)} {P(.5, 1)} C{P(.28, 1)} {P(.1, .9)} "
            f"{P(.08, .7)} C{P(.06, .5)} {P(.3, .38)} {P(.36, .2)} "
            f"C{P(.42, .34)} {P(.46, .38)} {P(.5, .0)} Z")


def grid(w, h, step=28, op=0.35):
    return f"""
  <pattern id="grid" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
    <path d="M{step} 0H0V{step}" fill="none" stroke="{BORDER}" stroke-width="0.7" opacity="{op}"/>
  </pattern>
  <pattern id="gridBig" width="{step*5}" height="{step*5}" patternUnits="userSpaceOnUse">
    <path d="M{step*5} 0H0V{step*5}" fill="none" stroke="{BORDER}" stroke-width="1.1" opacity="{op*1.6}"/>
  </pattern>"""


# --------------------------------------------------------------------------
# 1. Hero banner
# --------------------------------------------------------------------------
def banner():
    W, H = 1200, 440
    gx, gy = 945, 205
    gear = gear_path(gx, gy, 128, 104, 14, 44)
    gear2 = gear_path(0, 0, 54, 42, 10, 16)
    flame = flame_path(gx, gy + 3, 46, 58)
    stack = ["SILICON", "LOGIC", "ASM", "C/C++", "KERNEL", "NET", "APPS", "AI"]
    cyc = 8.0
    ticker = []
    x = 70
    for i, s in enumerate(stack):
        ticker.append(
            f'<text x="{x}" y="392" class="tk" style="animation-delay:{i * cyc / len(stack):.2f}s">{s}</text>')
        x += len(s) * 12.2 + 26
        if i < len(stack) - 1:
            ticker.append(f'<text x="{x - 17}" y="392" class="sep">›</text>')

    # binary rain columns on the far right edge area
    rain = []
    import random
    random.seed(7)
    for c in range(26):
        cx = 690 + c * 20 + random.randint(-3, 3)
        dur = random.uniform(5, 11)
        delay = -random.uniform(0, dur)
        bits = "".join(random.choice("01") + "\n" for _ in range(14))
        spans = "".join(
            f'<tspan x="{cx}" dy="18">{b}</tspan>' for b in bits.split())
        rain.append(
            f'<text class="rain" y="-260" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">{spans}</text>')

    ticks = "".join(
        f'<line x1="{gx + 158 * math.cos(math.radians(a)):.1f}" y1="{gy + 158 * math.sin(math.radians(a)):.1f}" '
        f'x2="{gx + (166 if a % 30 else 174) * math.cos(math.radians(a)):.1f}" y2="{gy + (166 if a % 30 else 174) * math.sin(math.radians(a)):.1f}"/>'
        for a in range(0, 360, 6))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sultan: building every layer of the machine">
<defs>{grid(W, H)}
  <radialGradient id="glow" cx="{gx}" cy="{gy}" r="260" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{EMBER}" stop-opacity=".40"/>
    <stop offset=".45" stop-color="{EMBER}" stop-opacity=".10"/>
    <stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig" cx="50%" cy="45%" r="75%">
    <stop offset=".55" stop-color="{BG}" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity=".85"/>
  </radialGradient>
  <linearGradient id="ember" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="{HOT}"/>
  </linearGradient>
  <linearGradient id="title" x1="0" x2="1">
    <stop offset="0" stop-color="{TEXT}"/><stop offset=".6" stop-color="{TEXT}"/>
    <stop offset="1" stop-color="{HOT}"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".55"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{EMBER}" stop-opacity="0"/>
    <stop offset="1" stop-color="{EMBER}" stop-opacity=".16"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10"/></filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
  <clipPath id="typeClip"><rect x="70" y="236" height="40" width="0" class="typer"/></clipPath>
  <clipPath id="titleClip"><text x="66" y="200" class="title">SULTAN</text></clipPath>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .title {{ font-size: 124px; font-weight: 800; letter-spacing: 6px; }}
  .g1 {{ fill: {COOL}; opacity: .75; animation: gl1 3.2s infinite steps(1); }}
  .g2 {{ fill: {EMBER}; opacity: .8; animation: gl2 3.2s infinite steps(1); }}
  @keyframes gl1 {{ 0%,86%,100% {{ transform: translate(0,0); clip-path: inset(0 0 100% 0); }}
    88% {{ transform: translate(-7px,2px); clip-path: inset(20% 0 55% 0); }}
    91% {{ transform: translate(5px,-2px); clip-path: inset(62% 0 12% 0); }}
    94% {{ transform: translate(-3px,0); clip-path: inset(40% 0 38% 0); }} }}
  @keyframes gl2 {{ 0%,86%,100% {{ transform: translate(0,0); clip-path: inset(0 0 100% 0); }}
    87% {{ transform: translate(8px,-1px); clip-path: inset(8% 0 70% 0); }}
    90% {{ transform: translate(-6px,3px); clip-path: inset(50% 0 25% 0); }}
    95% {{ transform: translate(4px,0); clip-path: inset(75% 0 5% 0); }} }}
  .shine {{ animation: shine 5s infinite ease-in-out; }}
  @keyframes shine {{ 0% {{ transform: translateX(-300px); }} 45%,100% {{ transform: translateX(700px); }} }}
  .typer {{ animation: type 9s infinite steps(35); }}
  @keyframes type {{ 0% {{ width: 0; }} 40%,88% {{ width: 530px; }} 100% {{ width: 0; }} }}
  .caret {{ animation: caret 9s infinite steps(35), blink .8s infinite steps(1); }}
  @keyframes caret {{ 0% {{ transform: translateX(0); }} 40%,88% {{ transform: translateX(530px); }} 100% {{ transform: translateX(0); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .spin {{ transform-origin: {gx}px {gy}px; animation: spin 22s linear infinite; }}
  .spinR {{ transform-origin: {gx}px {gy}px; animation: spin 40s linear infinite reverse; }}
  .spin2 {{ animation: spin 9s linear infinite reverse; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .pulse {{ transform-origin: {gx}px {gy}px; animation: pulse 2.6s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity: .75; transform: scale(.96); }} 50% {{ opacity: 1; transform: scale(1.05); }} }}
  .flicker {{ transform-origin: {gx}px {gy + 30}px; animation: flick 1.3s ease-in-out infinite; }}
  @keyframes flick {{ 0%,100% {{ transform: scale(1,1); }} 30% {{ transform: scale(.94,1.06); }} 60% {{ transform: scale(1.04,.95); }} }}
  .orbit {{ transform-origin: {gx}px {gy}px; animation: spin 6s linear infinite; }}
  .orbit2 {{ transform-origin: {gx}px {gy}px; animation: spin 11s linear infinite reverse; }}
  .tk {{ font-size: 17px; font-weight: 700; letter-spacing: 2px; fill: {FAINT}; animation: tk {cyc}s infinite; }}
  @keyframes tk {{ 0% {{ fill: {FAINT}; }} 3% {{ fill: {HOT}; }} 12.5% {{ fill: {EMBER}; }} 20%,100% {{ fill: {FAINT}; }} }}
  .sep {{ font-size: 17px; fill: {BORDER}; }}
  .rain {{ font-size: 13px; fill: {EMBER}; opacity: .10; animation: rain 8s linear infinite; }}
  @keyframes rain {{ to {{ transform: translateY(720px); }} }}
  .scan {{ animation: scan 6s linear infinite; }}
  @keyframes scan {{ 0% {{ transform: translateY(-120px); }} 100% {{ transform: translateY({H}px); }} }}
  .lbl {{ font-size: 11px; letter-spacing: 3px; fill: {FAINT}; }}
  .dot {{ animation: blink 1.6s infinite steps(1); }}
  .sub {{ font-size: 25px; fill: {MUTED}; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#gridBig)"/>
  {''.join(rain)}
  <circle cx="{gx}" cy="{gy}" r="260" fill="url(#glow)" class="pulse"/>

  <!-- gear assembly -->
  <g stroke="{FAINT}" stroke-width="1.2" opacity=".55" class="spinR">{ticks}</g>
  <circle cx="{gx}" cy="{gy}" r="186" fill="none" stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 8" class="spin"/>
  <circle cx="{gx}" cy="{gy}" r="146" fill="none" stroke="url(#ember)" stroke-width="2" stroke-dasharray="120 800" stroke-linecap="round" class="orbit"/>
  <circle cx="{gx}" cy="{gy}" r="200" fill="none" stroke="{COOL}" stroke-width="1.5" stroke-dasharray="40 1200" stroke-linecap="round" opacity=".7" class="orbit2"/>
  <g class="spin">
    <path d="{gear}" fill="url(#ember)" fill-rule="evenodd" filter="url(#blur)" opacity=".55"/>
    <path d="{gear}" fill="{SURFACE}" fill-rule="evenodd" stroke="url(#ember)" stroke-width="3"/>
    <circle cx="{gx}" cy="{gy}" r="80" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
    <g stroke="{BORDER}" stroke-width="2">
      {''.join(f'<line x1="{gx + 48 * math.cos(math.radians(a)):.1f}" y1="{gy + 48 * math.sin(math.radians(a)):.1f}" x2="{gx + 98 * math.cos(math.radians(a)):.1f}" y2="{gy + 98 * math.sin(math.radians(a)):.1f}"/>' for a in range(0, 360, 60))}
    </g>
  </g>
  <g transform="translate({gx + 150},{gy + 150})"><g class="spin2">
    <path d="{gear2}" fill="{SURFACE}" fill-rule="evenodd" stroke="{FAINT}" stroke-width="2"/>
  </g></g>
  <circle cx="{gx}" cy="{gy}" r="42" fill="{BG}" stroke="url(#ember)" stroke-width="2"/>
  <g class="flicker">
    <path d="{flame}" fill="url(#ember)" filter="url(#soft)" opacity=".9"/>
    <path d="{flame}" fill="url(#ember)"/>
    <path d="{flame_path(gx, gy + 14, 20, 28)}" fill="{CORE}" opacity=".9"/>
  </g>

  <!-- title -->
  <text x="70" y="78" class="lbl">SYS://YEPSULTAN <tspan fill="{EMBER}" class="dot">●</tspan> ONLINE</text>
  <text x="66" y="200" class="title g1">SULTAN</text>
  <text x="66" y="200" class="title g2">SULTAN</text>
  <text x="66" y="200" class="title" fill="url(#title)">SULTAN</text>
  <g clip-path="url(#titleClip)"><rect x="0" y="80" width="160" height="140" fill="url(#shine)" class="shine" opacity=".6"/></g>
  <rect x="70" y="216" width="84" height="4" fill="url(#ember)" rx="2"/>
  <g clip-path="url(#typeClip)">
    <text x="70" y="265" class="sub">building every layer of the machine</text>
  </g>
  <rect x="70" y="243" width="13" height="28" fill="{EMBER}" class="caret"/>
  <text x="70" y="320" class="lbl">UNIVERSITY STUDENT  /  FULL-DEPTH ENGINEER IN PROGRESS</text>

  <!-- stack ticker -->
  <line x1="70" y1="358" x2="1130" y2="358" stroke="{BORDER}"/>
  {''.join(ticker)}

  <rect width="{W}" height="120" fill="url(#scan)" class="scan"/>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <!-- corner brackets -->
  <g stroke="{EMBER}" stroke-width="2" fill="none" opacity=".8">
    <path d="M24 56V24H56"/><path d="M{W - 56} 24H{W - 24}V56"/>
    <path d="M24 {H - 56}V{H - 24}H56"/><path d="M{W - 56} {H - 24}H{W - 24}V{H - 56}"/>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
</svg>"""
    write("banner.svg", svg)


# --------------------------------------------------------------------------
# 2. Terminal: whoami
# --------------------------------------------------------------------------
def terminal():
    W = 1200
    lines = [
        ("cmd", "whoami"),
        ("out", "sultan. university student. learning the machine top to bottom."),
        ("cmd", "cat mission.txt"),
        ("out", "hardware -> machine code -> C/C++ -> OS -> networks -> apps -> AI"),
        ("cmd", "ls ~/projects"),
        ("dir", "engineering-base/   study-manager/   uni-tasks/"),
        ("cmd", "./rules --short"),
        ("out", "1. build it first.  2. break it second.  3. no 12-hour courses."),
    ]
    H = 96 + len(lines) * 34 + 40
    total = 16.0
    per = 1.35  # seconds per line
    char_w = 10.2
    prompt = "sultan@base:~$ "
    rows = []
    styles = []
    for i, (kind, txt) in enumerate(lines):
        y = 98 + i * 34
        start = 0.4 + i * per
        typed = kind == "cmd"
        full = (len(prompt) + len(txt)) if typed else len(txt) + 2
        width = full * char_w + 20
        p0 = start / total * 100
        p1 = (start + (0.8 if typed else 0.05)) / total * 100
        styles.append(
            f"@keyframes l{i} {{ 0%,{p0:.2f}% {{ width: 0; }} {p1:.2f}%,94% {{ width: {width:.0f}px; }} 100% {{ width: 0; }} }}"
            f" .l{i} {{ animation: l{i} {total}s infinite {'steps(' + str(len(txt) + len(prompt)) + ')' if typed else 'linear'}; }}")
        rows.append(f'<clipPath id="c{i}"><rect x="40" y="{y - 24}" height="34" width="0" class="l{i}"/></clipPath>')
        if kind == "cmd":
            body = (f'<tspan fill="{GOOD}">sultan@base</tspan><tspan fill="{MUTED}">:</tspan>'
                    f'<tspan fill="{COOL}">~</tspan><tspan fill="{MUTED}">$ </tspan><tspan fill="{TEXT}">{txt}</tspan>')
        elif kind == "dir":
            body = f'<tspan fill="{FAINT}">› </tspan><tspan fill="{COOL}" font-weight="700">{txt}</tspan>'
        else:
            body = f'<tspan fill="{FAINT}">› </tspan><tspan fill="{HOT}">{txt}</tspan>'
        rows.append(f'<text x="44" y="{y}" clip-path="url(#c{i})">{body}</text>')
    last_y = 98 + len(lines) * 34
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="whoami: sultan, university student learning the machine top to bottom">
<defs>{grid(W, H, 24, .25)}
  <linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="{HOT}"/></linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
  text {{ font-family: {MONO}; font-size: 17px; white-space: pre; }}
  {' '.join(styles)}
  .cur {{ animation: blink 1s infinite steps(1); }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .run {{ animation: run 3s linear infinite; }}
  @keyframes run {{ from {{ transform: translateX(-300px); }} to {{ transform: translateX({W}px); }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{SURFACE}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="44" fill="#0C0E12"/>
  <rect y="43" width="300" height="1.5" fill="url(#bar)" class="run"/>
  <circle cx="30" cy="22" r="7" fill="#FF5F57"/><circle cx="54" cy="22" r="7" fill="#FEBC2E"/><circle cx="78" cy="22" r="7" fill="#28C840"/>
  <text x="{W / 2}" y="28" text-anchor="middle" fill="{FAINT}" font-size="13" letter-spacing="2">sultan@base: ~ — zsh — 120×32</text>
  {''.join(rows)}
  <text x="44" y="{last_y}"><tspan fill="{GOOD}">sultan@base</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{COOL}">~</tspan><tspan fill="{MUTED}">$ </tspan></text>
  <rect x="{44 + len(prompt) * char_w:.0f}" y="{last_y - 17}" width="10" height="21" fill="{EMBER}" class="cur"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{BORDER}"/>
</svg>"""
    write("terminal.svg", svg)


# --------------------------------------------------------------------------
# 3. The stack: hardware at the bottom, AI on top, energy climbing up
# --------------------------------------------------------------------------
def stack():
    layers = [
        ("08", "AI", "models, RAG, agents", "Python"),
        ("07", "APPS", "phone + desktop, any screen", "Flutter / Dart"),
        ("06", "NETWORKS", "packets, sockets, protocols", "TCP/IP"),
        ("05", "OPERATING SYSTEMS", "processes, memory, files", "Linux"),
        ("04", "SYSTEMS LANGUAGES", "pointers, memory, speed", "C / C++"),
        ("03", "MACHINE CODE", "registers, instructions", "x86 / ASM"),
        ("02", "DIGITAL LOGIC", "gates, adders, CPUs", "Nand2Tetris"),
        ("01", "HARDWARE", "electrons to transistors", "circuits"),
    ]
    now = {"APPS", "SYSTEMS LANGUAGES"}
    W = 1200
    rowh = 58
    top = 92
    H = top + len(layers) * rowh + 46
    cyc = 6.0
    n = len(layers)
    rows = []
    for i, (num, name, desc, tool) in enumerate(layers):
        y = top + i * rowh
        order = n - 1 - i  # bottom lights first
        delay = order * cyc / n / 1.6
        w = 1040 - (n - 1 - i) * 0  # constant width
        x = 80
        is_now = name in now
        rows.append(f"""
  <g class="row" style="animation-delay:{delay:.2f}s">
    <rect x="{x}" y="{y}" width="{w}" height="{rowh - 12}" rx="8" fill="{SURFACE}" stroke="{EMBER if is_now else BORDER}" stroke-width="{1.6 if is_now else 1}" class="slab" style="animation-delay:{delay:.2f}s"/>
    <rect x="{x}" y="{y}" width="4" height="{rowh - 12}" rx="2" fill="url(#ember)" class="edge" style="animation-delay:{delay:.2f}s"/>
    <text x="{x + 24}" y="{y + 29}" class="num">{num}</text>
    <text x="{x + 70}" y="{y + 30}" class="name">{name}</text>
    <text x="{x + 420}" y="{y + 29}" class="desc">{desc}</text>
    <text x="{x + w - 24}" y="{y + 29}" class="tool" text-anchor="end">{tool}</text>
    {f'<g><rect x="{x + w - 250}" y="{y + 12}" width="92" height="22" rx="11" fill="{EMBER}" fill-opacity=".14" stroke="{EMBER}" stroke-width="1"/><text x="{x + w - 204}" y="{y + 27}" class="nowtxt" text-anchor="middle">BUILDING</text></g>' if is_now else ''}
  </g>""")
    bus_x = 50
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The stack I am learning, from hardware to AI">
<defs>{grid(W, H, 24, .3)}
  <linearGradient id="ember" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="{HOT}"/></linearGradient>
  <linearGradient id="beam" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="{HOT}" stop-opacity="0"/><stop offset=".5" stop-color="{HOT}"/><stop offset="1" stop-color="{HOT}" stop-opacity="0"/>
  </linearGradient>
  <filter id="soft" x="-200%" y="-50%" width="500%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .hd {{ font-size: 13px; letter-spacing: 4px; fill: {FAINT}; }}
  .hd b {{ fill: {EMBER}; }}
  .num {{ font-size: 13px; fill: {FAINT}; }}
  .name {{ font-size: 17px; font-weight: 700; letter-spacing: 2px; fill: {TEXT}; }}
  .desc {{ font-size: 14px; fill: {MUTED}; }}
  .tool {{ font-size: 14px; fill: {HOT}; }}
  .nowtxt {{ font-size: 11px; font-weight: 700; letter-spacing: 2px; fill: {EMBER}; }}
  .edge {{ opacity: .25; animation: edge {cyc}s infinite; }}
  @keyframes edge {{ 0%,100% {{ opacity: .25; }} 8% {{ opacity: 1; }} 30% {{ opacity: .25; }} }}
  .slab {{ animation: slab {cyc}s infinite; }}
  @keyframes slab {{ 0%,100% {{ fill: {SURFACE}; }} 8% {{ fill: #1E1612; }} 30% {{ fill: {SURFACE}; }} }}
  .beam {{ animation: beam {cyc / 1.6:.2f}s cubic-bezier(.5,0,.5,1) infinite; }}
  @keyframes beam {{ from {{ transform: translateY({H}px); }} to {{ transform: translateY(-160px); }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <text x="80" y="54" class="hd">THE STACK <tspan fill="{EMBER}">//</tspan> WHAT I AM LEARNING, BOTTOM UP</text>
  <text x="1120" y="54" class="hd" text-anchor="end">electrons <tspan fill="{EMBER}">→</tspan> intelligence</text>
  <line x1="{bus_x}" y1="{top}" x2="{bus_x}" y2="{top + n * rowh - 12}" stroke="{BORDER}" stroke-width="2"/>
  {''.join(f'<circle cx="{bus_x}" cy="{top + i * rowh + (rowh - 12) / 2}" r="4" fill="{BG}" stroke="{FAINT}" stroke-width="1.5"/><line x1="{bus_x + 4}" y1="{top + i * rowh + (rowh - 12) / 2}" x2="80" y2="{top + i * rowh + (rowh - 12) / 2}" stroke="{BORDER}"/>' for i in range(n))}
  <g class="beam">
    <rect x="{bus_x - 2}" y="0" width="4" height="140" fill="url(#beam)"/>
    <rect x="{bus_x - 6}" y="0" width="12" height="140" fill="url(#beam)" filter="url(#soft)"/>
  </g>
  {''.join(rows)}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
</svg>"""
    write("stack.svg", svg)


# --------------------------------------------------------------------------
# 4. Project cards
# --------------------------------------------------------------------------
def card(fname, title, tag, desc_lines, chips, accent, icon):
    W, H = 590, 250
    per = 2 * (W + H)
    chip_svg = []
    x = 28
    for c in chips:
        w = len(c) * 8.6 + 22
        chip_svg.append(
            f'<rect x="{x}" y="{H - 58}" width="{w:.0f}" height="26" rx="13" fill="{accent}" fill-opacity=".10" stroke="{accent}" stroke-opacity=".5"/>'
            f'<text x="{x + w / 2:.0f}" y="{H - 40}" class="chip" text-anchor="middle">{c}</text>')
        x += w + 8
    desc = "".join(
        f'<text x="28" y="{120 + i * 24}" class="desc">{l}</text>' for i, l in enumerate(desc_lines))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<defs>
  <linearGradient id="a" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{HOT}"/></linearGradient>
  <radialGradient id="g" cx="{W - 70}" cy="60" r="200" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{BORDER}"/></pattern>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .t {{ font-size: 26px; font-weight: 800; fill: {TEXT}; letter-spacing: 1px; }}
  .tag {{ font-size: 11px; letter-spacing: 3px; fill: {accent}; }}
  .desc {{ font-size: 14.5px; fill: {MUTED}; }}
  .chip {{ font-size: 12px; fill: {TEXT}; }}
  .run {{ stroke-dasharray: 160 {per - 160}; animation: run 5s linear infinite; }}
  @keyframes run {{ to {{ stroke-dashoffset: -{per}; }} }}
  .ic {{ transform-origin: {W - 70}px 64px; animation: bob 4s ease-in-out infinite; }}
  @keyframes bob {{ 0%,100% {{ transform: translateY(0) rotate(0); }} 50% {{ transform: translateY(-5px) rotate(4deg); }} }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{SURFACE}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#dots)" opacity=".6"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#g)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.5"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="url(#a)" stroke-width="2.5" stroke-linecap="round" class="run"/>
<text x="28" y="46" class="tag">{tag}</text>
<text x="28" y="84" class="t">{title}</text>
{desc}
<g class="ic">{icon}</g>
{''.join(chip_svg)}
</svg>"""
    write(fname, svg)


def cards():
    cx, cy = 590 - 70, 64
    gear_icon = (f'<path d="{gear_path(cx, cy, 30, 23, 10, 10)}" fill="none" fill-rule="evenodd" stroke="{EMBER}" stroke-width="2.5"/>'
                 f'<path d="{flame_path(cx, cy + 1, 11, 14)}" fill="{HOT}"/>')
    book_icon = (f'<rect x="{cx - 28}" y="{cy - 22}" width="56" height="44" rx="6" fill="none" stroke="{COOL}" stroke-width="2.5"/>'
                 f'<line x1="{cx}" y1="{cy - 22}" x2="{cx}" y2="{cy + 22}" stroke="{COOL}" stroke-width="2.5"/>'
                 f'<path d="M{cx - 20} {cy - 10}h12M{cx - 20} {cy}h12M{cx + 8} {cy - 10}h12M{cx + 8} {cy}h8" stroke="{COOL}" stroke-width="2" stroke-linecap="round"/>'
                 f'<circle cx="{cx + 26}" cy="{cy - 22}" r="7" fill="{HOT}"/>')
    cpp_icon = (f'<text x="{cx}" y="{cy + 12}" text-anchor="middle" font-size="36" font-weight="800" fill="{GOOD}">{{ }}</text>')
    card("card-engineering-base.svg", "Engineering Base", "FLUTTER · ANDROID + LINUX",
         ["Tracker for a whole engineering curriculum:",
          "14 areas, 188 topics, streaks, practice queue,",
          "focus timer, XP. Fully offline, phone + desktop."],
         ["Dart", "Flutter", "Linux", "Android"], EMBER, gear_icon)
    card("card-study-manager.svg", "Study Manager", "FLUTTER · SUPABASE · CLAUDE",
         ["University organiser: weeks, subjects, lectures,",
          "missing work. Inbox sorts dropped files with",
          "Claude. Syncs phone and laptop."],
         ["Flutter", "Supabase", "Postgres", "AI"], COOL, book_icon)
    card("card-uni-tasks.svg", "Uni_tasks24-03", "C++ · UNIVERSITY",
         ["Solved tasks from my university course.",
          "Where the low-level journey started:",
          "loops, arrays, pointers, memory."],
         ["C++", "Algorithms"], GOOD, cpp_icon)


# --------------------------------------------------------------------------
# 5. Divider + footer
# --------------------------------------------------------------------------
def divider():
    W, H = 1200, 40
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="a" x1="0" x2="1">
  <stop offset="0" stop-color="{EMBER}" stop-opacity="0"/><stop offset=".5" stop-color="{HOT}"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/>
</linearGradient></defs>
<style>.m {{ animation: m 4s ease-in-out infinite alternate; }} @keyframes m {{ from {{ transform: translateX(-420px); }} to {{ transform: translateX(420px); }} }}</style>
<line x1="0" y1="20" x2="{W}" y2="20" stroke="{BORDER}" stroke-width="1.5"/>
<g class="m"><rect x="{W / 2 - 180}" y="19" width="360" height="2" fill="url(#a)"/><circle cx="{W / 2}" cy="20" r="4" fill="{HOT}"/></g>
<path d="M{W / 2 - 10} 20l10-10 10 10-10 10z" fill="{BG}" stroke="{EMBER}" stroke-width="1.5"/>
</svg>"""
    write("divider.svg", svg)


def footer():
    W, H = 1200, 170
    bars = []
    for i in range(60):
        x = 20 + i * 19.4
        d = (i * 0.07) % 1.6
        bars.append(f'<rect x="{x:.1f}" y="40" width="9" height="90" rx="3" fill="url(#e)" class="eq" style="animation-delay:-{d:.2f}s"/>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="build it first, break it second">
<defs>
  <linearGradient id="e" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{EMBER}" stop-opacity=".05"/><stop offset="1" stop-color="{EMBER}" stop-opacity=".5"/></linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
  text {{ font-family: {MONO}; }}
  .eq {{ transform-box: fill-box; transform-origin: bottom; animation: eq 1.6s ease-in-out infinite; }}
  @keyframes eq {{ 0%,100% {{ transform: scaleY(.15); }} 50% {{ transform: scaleY(1); }} }}
  .q {{ font-size: 30px; font-weight: 800; fill: {TEXT}; letter-spacing: 2px; }}
  .s {{ font-size: 12px; letter-spacing: 4px; fill: {FAINT}; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {''.join(bars)}
  <rect width="{W}" height="{H}" fill="{BG}" opacity=".35"/>
  <text x="{W / 2}" y="92" class="q" text-anchor="middle">BUILD IT FIRST<tspan fill="{EMBER}">.</tspan> BREAK IT SECOND<tspan fill="{EMBER}">.</tspan></text>
  <text x="{W / 2}" y="126" class="s" text-anchor="middle">THANKS FOR SCROLLING  //  SEE YOU IN THE COMMITS</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
</svg>"""
    write("footer.svg", svg)


if __name__ == "__main__":
    banner()
    terminal()
    stack()
    cards()
    divider()
    footer()
