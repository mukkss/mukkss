#!/usr/bin/env python3
import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_utils
import theme
from generate_stats import fade, wipe, label, WIDTH

LEFT = 34

def hbar(x, y, w, h, cls="d-f", r=3.0):
    if w <= 0.6:
        return svg_utils.Group()
    r = min(r, h / 2.0, w)
    path_d = (f"M{x:.1f} {y:.1f}H{x + w - r:.1f}"
              f"Q{x + w:.1f} {y:.1f} {x + w:.1f} {y + r:.1f}"
              f"V{y + h - r:.1f}Q{x + w:.1f} {y + h:.1f} {x + w - r:.1f} {y + h:.1f}"
              f"H{x:.1f}Z")
    return svg_utils.Path(d=path_d, _class=cls)

def draw_langs(s):
    rows = max(len(s["by_size"]), len(s["by_repo"]), 1)
    H = 26 + rows * 22 + 6
    colw = (WIDTH - LEFT - 30) / 2
    name_w, bar_max = 82, colw - 82 - 44

    svg = svg_utils.SVG(width=str(WIDTH), height=str(H), fill="none", font_family=theme.MONO)
    svg.add(svg_utils.Style(theme.style()))

    groups = [(LEFT, "by bytes", s["by_size"], True),
              (LEFT + colw + 30, "by repos", s["by_repo"], False)]
              
    for gi, (gx, title, data, as_pct) in enumerate(groups):
        g_title = svg_utils.Group(opacity="0")
        g_title.add(fade(0.10 + gi * 0.10))
        g_title.add(label(gx, 12, title.upper(), 9, "m-f", font_weight=None))
        # Modify the Text object manually to add letter-spacing
        g_title.children[1].attributes["letter-spacing"] = "1.3"
        svg.add(g_title)
        
        if not data:
            continue
            
        top = max(v for _, v in data) or 1
        total = sum(v for _, v in data) or 1
        cid = f"rl{gi}"
        
        clip, cursor = wipe(cid, gx + name_w, 20, bar_max, rows * 22, 0.34 + gi * 0.12, 0.95)
        svg.add(clip)
        
        for ri, (name, val) in enumerate(data):
            y = 26 + ri * 22
            shown = f"{val / total * 100:.0f}%" if as_pct else f"{val}"
            
            g_row = svg_utils.Group(opacity="0")
            g_row.add(fade(0.24 + gi * 0.10 + ri * 0.05))
            g_row.add(label(gx, y + 8, name.lower()[:11], 11, "e-f"))
            g_row.add(label(gx + colw - 6, y + 8, shown, 11, "m-f", "end"))
            svg.add(g_row)
            
            g_bar = svg_utils.Group(clip_path=f"url(#{cid})")
            g_bar.add(hbar(gx + name_w, y, bar_max * val / top, 7))
            svg.add(g_bar)
            
        svg.add(cursor)

    return svg.render()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/profile.json")
    ap.add_argument("--out", default="assets/stats/langs.svg")
    args = ap.parse_args()
    
    if not os.path.exists(args.data):
        sys.exit(f"Data file not found: {args.data}. Run fetch_data.py first.")
        
    with open(args.data, "r") as f:
        data = json.load(f)
        
    svg_content = draw_langs(data)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg_content)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
