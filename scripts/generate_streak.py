#!/usr/bin/env python3
import sys
import os
import argparse
import json
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_utils
import theme
from generate_stats import fade, wipe, label, WIDTH

LEFT = 34
MON = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

def pretty(iso):
    if not iso:
        return ""
    d = date.fromisoformat(iso[:10])
    return f"{MON[d.month - 1]} {d.day}"

def draw_streak(s):
    H = 96
    cells = []
    for k, lab in (("current", "current streak"), ("longest", "longest streak")):
        r = s[k]
        span = f"{pretty(r['start'])} &#8211; {pretty(r['end'])}" if r["length"] else "&#8212;"
        cells.append((r["length"], lab, span))

    svg = svg_utils.SVG(width=str(WIDTH), height=str(H), fill="none", font_family=theme.MONO)
    svg.add(svg_utils.Style(theme.style()))

    mid = WIDTH / 2
    line = svg_utils.Line(x1=f"{mid:.0f}", y1="16", x2=f"{mid:.0f}", y2="80", _class="u-s", stroke_width="1", opacity="0")
    line.add(fade(0.20))
    svg.add(line)

    for i, (val, lab, span) in enumerate(cells):
        x = LEFT if i == 0 else mid + LEFT
        g = svg_utils.Group(opacity="0")
        g.add(fade(0.12 + i * 0.14))
        g.add(label(x, 44, f"{val}", 34, "e-f", font_weight="600"))
        g.add(label(x, 64, lab, 11))
        
        # span might have html entities (&#8211;). Since svg_utils doesn't escape by default (or we handle it manually):
        # We can pass raw text.
        kw = {"x": str(x), "y": str(80), "_class": "m-f", "font_size": "10"}
        g.add(svg_utils.Text(str(span), **kw))
        svg.add(g)

    return svg.render()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/profile.json")
    ap.add_argument("--out", default="assets/stats/streak.svg")
    args = ap.parse_args()
    
    if not os.path.exists(args.data):
        sys.exit(f"Data file not found: {args.data}. Run fetch_data.py first.")
        
    with open(args.data, "r") as f:
        data = json.load(f)
        
    svg_content = draw_streak(data)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg_content)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
