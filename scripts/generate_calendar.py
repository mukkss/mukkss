#!/usr/bin/env python3
import sys
import os
import argparse
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_utils
import theme
from generate_stats import fade, label, WIDTH
from generate_streak import MON

LEFT = 34
RAMP = [" ", ":", "+", "#", "@"]

def draw_year(s):
    FS, LH, COLW = 9.2, 11.0, 2
    CW = FS * 0.6
    pad_l, pad_t = LEFT, 44
    weeks = s["weeks"]
    H = int(pad_t + 7 * LH + 26)

    def level(v):
        for i, cut in enumerate((0, 2, 5, 9)):
            if v <= cut:
                return i
        return 4

    svg = svg_utils.SVG(width=str(WIDTH), height=str(H), fill="none", font_family=theme.MONO)
    svg.add(svg_utils.Style(theme.style()))

    g_title = svg_utils.Group(opacity="0")
    g_title.add(fade(0.10))
    t1 = label(pad_l, 16, "THE YEAR", 9, "m-f")
    t1.attributes["letter-spacing"] = "1.3"
    g_title.add(t1)
    g_title.add(label(pad_l, 32, f"{s['active']} of {sum(len(w) for w in weeks)} days had a contribution", 11))
    svg.add(g_title)

    lx = WIDTH - 6
    g_legend = svg_utils.Group(opacity="0")
    g_legend.add(fade(1.30))
    g_legend.add(label(lx - 78, 32, "less", 9, "m-f", "end"))
    g_legend.add(svg_utils.Text(" ".join(RAMP[1:]), xml__space="preserve", x=str(lx - 72), y="32", _class="d-f", font_size=str(FS)))
    g_legend.add(label(lx, 32, "more", 9, "m-f", "end"))
    svg.add(g_legend)

    for r in range(7):
        chars = []
        for w in weeks:
            day = next((d for d in w if d.get("weekday") == r), None)
            v = day["contributionCount"] if day else 0
            chars.append(RAMP[level(v)] * COLW)
        line = "".join(chars).rstrip()
        if not line:
            continue
            
        y = pad_t + r * LH
        w_px = max(len(line), 1) * CW
        cid = f"ry{r}"
        delay = 0.30 + r * 0.07
        
        clip_path = svg_utils.ClipPath(id=cid)
        clip_rect = svg_utils.Rect(x=str(pad_l), y=str(y), height=str(LH), width="0")
        clip_rect.add(svg_utils.Animate(attributeName="width", _from="0", to=f"{w_px:.1f}", begin=f"{delay:.2f}s", dur="0.40s", fill="freeze"))
        clip_path.add(clip_rect)
        svg.add(clip_path)
        
        safe = svg_utils.escape_xml(line)
        g_row = svg_utils.Group(clip_path=f"url(#{cid})")
        g_row.add(svg_utils.Text(safe, xml__space="preserve", x=str(pad_l), y=f"{y + FS - 0.6:.1f}", _class="d-f", font_size=str(FS)))
        svg.add(g_row)

    for r, lab in ((1, "mon"), (3, "wed"), (5, "fri")):
        svg.add(label(pad_l - 7, pad_t + r * LH + FS - 0.6, lab, 9, "m-f", "end"))

    last_m, last_x = None, -999.0
    base_y = pad_t + 7 * LH + 13
    for i, w in enumerate(weeks):
        m = int(w[0]["date"][5:7])
        x = pad_l + i * COLW * CW
        if m != last_m and i < len(weeks) - 1 and x - last_x >= 34:
            svg.add(label(x, base_y, MON[m - 1], 9, "m-f"))
            last_x = x
        last_m = m

    return svg.render()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/profile.json")
    ap.add_argument("--out", default="assets/stats/calendar.svg")
    args = ap.parse_args()
    
    if not os.path.exists(args.data):
        sys.exit(f"Data file not found: {args.data}. Run fetch_data.py first.")
        
    with open(args.data, "r") as f:
        data = json.load(f)
        
    svg_content = draw_year(data)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg_content)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
