#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg_utils
import theme
import font_subset
from generate_stats import label, WIDTH

def draw_heading(word, font_rule=""):
    FS = 16
    H = 26
    text_end = len(word) * FS * 0.6 + 18
    
    svg = svg_utils.SVG(width=str(WIDTH), height=str(H), fill="none", font_family=theme.MONO)
    css = theme.style()
    if font_rule:
        css = font_rule + "\n" + css
    svg.add(svg_utils.Style(css))

    svg.add(label(0, 18, word, FS, "e-f", font_weight="600"))
    svg.add(svg_utils.Line(x1=f"{text_end:.0f}", y1="12.5", x2=str(WIDTH), y2="12.5", _class="u-s", stroke_width="1"))
    
    return svg.render()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("word", help="The heading text")
    ap.add_argument("out", help="Output file path")
    ap.add_argument("--font", help="Path to woff2 font")
    args = ap.parse_args()
    
    font_rule = ""
    if args.font:
        font_rule = font_subset.get_font_face_rule(args.font, weight=600)
        
    svg_content = draw_heading(args.word, font_rule)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(svg_content)
    print(f"wrote {args.out}")

if __name__ == "__main__":
    main()
