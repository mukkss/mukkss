import html

class Element:
    def __init__(self, tag, text="", **kwargs):
        self.tag = tag
        self.text = text
        self.attributes = {}
        for k, v in kwargs.items():
            if v is not None:
                if k == "_from":
                    k = "from"
                elif k == "_class":
                    k = "class"
                else:
                    k = k.replace("__", ":").replace("_", "-")
                self.attributes[k] = v
        self.children = []

    def add(self, *children):
        for child in children:
            if child is not None:
                self.children.append(child)
        return self

    def render(self, indent=""):
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        tag_open = f"<{self.tag} {attrs}>".strip().replace(" >", ">")
        
        if not self.children and not self.text:
            return f"{indent}<{self.tag}{' ' + attrs if attrs else ''}/>"
        
        result = [f"{indent}{tag_open}"]
        if self.text:
            result.append(f"{indent}  {self.text}")
        for child in self.children:
            result.append(child.render(indent + "  "))
        result.append(f"{indent}</{self.tag}>")
        return "\n".join(result)

class SVG(Element):
    def __init__(self, width, height, **kwargs):
        super().__init__("svg", xmlns="http://www.w3.org/2000/svg", width=width, height=height, viewBox=f"0 0 {width} {height}", **kwargs)

class ClipPath(Element):
    def __init__(self, id, **kwargs):
        super().__init__("clipPath", id=id, **kwargs)

class Rect(Element):
    def __init__(self, **kwargs):
        super().__init__("rect", **kwargs)

class Line(Element):
    def __init__(self, **kwargs):
        super().__init__("line", **kwargs)

class Path(Element):
    def __init__(self, **kwargs):
        super().__init__("path", **kwargs)

class Circle(Element):
    def __init__(self, **kwargs):
        super().__init__("circle", **kwargs)

class Text(Element):
    def __init__(self, text, **kwargs):
        super().__init__("text", text=text, **kwargs)

class Animate(Element):
    def __init__(self, **kwargs):
        super().__init__("animate", **kwargs)

class Set(Element):
    def __init__(self, **kwargs):
        super().__init__("set", **kwargs)

class Group(Element):
    def __init__(self, **kwargs):
        super().__init__("g", **kwargs)

class Style(Element):
    def __init__(self, css, **kwargs):
        super().__init__("style", text=css, **kwargs)

def escape_xml(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
