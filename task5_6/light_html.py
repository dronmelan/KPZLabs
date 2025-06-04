from abc import ABC, abstractmethod
from typing import List, Optional


class LightNode(ABC):

    @abstractmethod
    def get_outer_html(self) -> str:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass


class LightTextNode(LightNode):

    def __init__(self, text: str):
        self.text = text

    def get_outer_html(self) -> str:
        return self.text

    def get_size(self) -> int:
        return 48 + len(self.text.encode('utf-8'))


class LightElementNode(LightNode):

    BLOCK = "block"
    INLINE = "inline"

    SELF_CLOSING = "self_closing"
    WITH_CLOSING_TAG = "with_closing_tag"

    def __init__(self, tag_name: str, display_type: str = BLOCK,
                 closing_type: str = WITH_CLOSING_TAG, css_classes: List[str] = None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
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

        if self.closing_type == self.SELF_CLOSING:
            return f'<{self.tag_name}{class_attr} />'
        else:
            inner_html = self.get_inner_html()
            return f'<{self.tag_name}{class_attr}>{inner_html}</{self.tag_name}>'

    def get_size(self) -> int:
        size = 120
        size += len(self.tag_name.encode('utf-8'))
        size += len(self.display_type.encode('utf-8'))
        size += len(self.closing_type.encode('utf-8'))
        for css_class in self.css_classes:
            size += len(css_class.encode('utf-8')) + 24
        size += len(self.children) * 8
        for child in self.children:
            size += child.get_size()
        return size