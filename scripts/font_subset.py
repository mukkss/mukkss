import base64
import os

def get_font_face_rule(font_path, font_family="JBMono", weight=400):
    """Reads a font file and returns an @font-face CSS rule with base64 embedded data."""
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
        
    with open(font_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
        
    return (f"@font-face{{font-family:{font_family};font-style:normal;"
            f"font-weight:{weight};font-display:block;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
