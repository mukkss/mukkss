#!/usr/bin/env python3
import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_utils
import theme

WIDTH = 620
REVEAL = 1.30

def fade(delay, dur=0.45):
    return svg_utils.Animate(attributeName="opacity", _from="0", to="1", begin=f"{delay:.2f}s", dur=f"{dur}s", fill="freeze")

def wipe(cid, x, y, w, h, delay, dur=REVEAL):
    clip = svg_utils.ClipPath(id=cid)
    clip_rect = svg_utils.Rect(x=str(x), y=str(y), height=str(h), width="0")
    clip_rect.add(svg_utils.Animate(attributeName="width", _from="0", to=str(w), begin=f"{delay:.2f}s", dur=f"{dur}s", fill="freeze"))
    clip.add(clip_rect)
    
    cursor = svg_utils.Rect(y=str(y), width="2", height=str(h), _class="d-f", opacity="0")
    cursor.add(svg_utils.Animate(attributeName="x", _from=str(x), to=str(x + w), begin=f"{delay:.2f}s", dur=f"{dur}s", fill="freeze"))
    cursor.add(svg_utils.Set(attributeName="opacity", to="0.55", begin=f"{delay:.2f}s"))
    cursor.add(svg_utils.Set(attributeName="opacity", to="0", begin=f"{delay + dur:.2f}s"))
    
    return clip, cursor

def label(x, y, text, size=11, cls="m-f", anchor="start", font_weight=None):
    kw = {"x": str(x), "y": str(y), "_class": cls, "font_size": str(size)}
    if anchor != "start":
        kw["text_anchor"] = anchor
    if font_weight:
        kw["font_weight"] = font_weight
    return svg_utils.Text(str(text), **kw)

def draw_stats(s):
    H = 148
    weekly = s["weekly"] or [0]
    peak = max(weekly) or 1
    
    svg = svg_utils.SVG(width=str(WIDTH), height=str(H), fill="none", font_family=theme.MONO)
    svg.add(svg_utils.Style(theme.style()))

    g_total = svg_utils.Group(opacity="0")
    g_total.add(fade(0.10))
    g_total.add(label(0, 50, s["total"], 52, "e-f", font_weight="600"))
    g_total.add(label(0, 72, "contributions in the last year", 12))
    svg.add(g_total)
    
    for i, (val, lab) in enumerate([(s["active"], "active days"), (s["best_week"], "best week")]):
        g = svg_utils.Group(opacity="0")
        g.add(fade(0.30 + i * 0.12))
        g.add(label(WIDTH, 30 + i * 40, val, 19, "e-f", "end", "600"))
        g.add(label(WIDTH, 47 + i * 40, lab, 11, "m-f", "end"))
        svg.add(g)

    base, top = H - 10, H - 58
    span = base - top
    step = WIDTH / max(len(weekly) - 1, 1)
    pts = [(i * step, base - (v / peak) * span) for i, v in enumerate(weekly)]
    
    clip, cursor = wipe("rs", 0, top - 6, WIDTH, span + 8, 0.50)
    svg.add(clip)
    
    g_graph = svg_utils.Group(clip_path="url(#rs)")
    
    path_d1 = f"M{pts[0][0]:.1f} {base:.1f}" + "".join(f"L{x:.1f} {y:.1f}" for x, y in pts) + f"L{pts[-1][0]:.1f} {base:.1f}Z"
    g_graph.add(svg_utils.Path(d=path_d1, _class="w"))
    
    path_d2 = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f"L{x:.1f} {y:.1f}" for x, y in pts[1:])
    g_graph.add(svg_utils.Path(d=path_d2, _class="d-s", stroke_width="2", stroke_linejoin="round", stroke_linecap="round"))
    svg.add(g_graph)
    svg.add(cursor)
    
    ex, ey = pts[-1]
    circle = svg_utils.Circle(cx=f"{ex - 2:.1f}", cy=f"{ey:.1f}", r="4.5", _class="e-f r", stroke_width="2", opacity="0")
    circle.add(fade(0.50 + REVEAL, 0.35))
    svg.add(circle)
    
    return svg.render()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/profile.json")
    ap.add_argument("--out", default="assets/stats/hero.svg")
    args = ap.parse_args()
    
    if not os.path.exists(args.data):
        sys.exit(f"Data file not found: {args.data}. Run fetch_data.py first.")
        
    with open(args.data, "r") as f:
        data = json.load(f)
        
    svg_content = draw_stats(data)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg_content)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
