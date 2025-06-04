from typing import Dict, List
from light_html import LightNode, LightElementNode, LightTextNode


class ElementFlyweight:

    def __init__(self, tag_name: str, display_type: str, closing_type: str):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type

    def get_size(self) -> int:
        return 72 + len(self.tag_name.encode('utf-8')) + \
            len(self.display_type.encode('utf-8')) + \
            len(self.closing_type.encode('utf-8'))


class ElementFlyweightFactory:

    _flyweights: Dict[str, ElementFlyweight] = {}

    @classmethod
    def get_flyweight(cls, tag_name: str, display_type: str, closing_type: str) -> ElementFlyweight:
        key = f"{tag_name}_{display_type}_{closing_type}"
        if key not in cls._flyweights:
            cls._flyweights[key] = ElementFlyweight(tag_name, display_type, closing_type)
        return cls._flyweights[key]

    @classmethod
    def get_flyweights_count(cls) -> int:
        return len(cls._flyweights)

    @classmethod
    def get_total_flyweights_size(cls) -> int:
        return sum(fw.get_size() for fw in cls._flyweights.values())


class LightElementNodeFlyweight(LightNode):

    def __init__(self, tag_name: str, display_type: str = "block",
                 closing_type: str = "with_closing_tag", css_classes: List[str] = None):
        self.flyweight = ElementFlyweightFactory.get_flyweight(tag_name, display_type, closing_type)
        self.css_classes = css_classes or []
        self.children: List[LightNode] = []

    def add_child(self, child: LightNode):
        self.children.append(child)

    def get_children_count(self) -> int:
        return len(self.children)

    def get_inner_html(self) -> str:
        return "".join(child.get_outer_html() for child in self.children)

    def get_outer_html(self) -> str:
        class_attr = f' class="{" ".join(self.css_classes)}"' if self.css_classes else ""

        if self.flyweight.closing_type == "self_closing":
            return f'<{self.flyweight.tag_name}{class_attr} />'
        else:
            inner_html = self.get_inner_html()
            return f'<{self.flyweight.tag_name}{class_attr}>{inner_html}</{self.flyweight.tag_name}>'

    def get_size(self) -> int:
        size = 48
        for css_class in self.css_classes:
            size += len(css_class.encode('utf-8')) + 24
        size += len(self.children) * 8
        for child in self.children:
            size += child.get_size()
        return size